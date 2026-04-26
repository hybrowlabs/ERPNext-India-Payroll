import json

import frappe
from frappe import _
from frappe.utils import add_months, flt, getdate
from hrms.hr.utils import get_total_exemption_amount
from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import (
    EmployeeTaxExemptionDeclaration,
)
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


class CustomEmployeeTaxExemptionDeclaration(EmployeeTaxExemptionDeclaration):
    def before_save(self):
        self.update_json_data_in_declaration()

    def before_update_after_submit(self):
        if self.flags.ignore_after_submit:
            return

        self.calculate_hra_breakup()
        self.set_max_amount_of_sub_category()
        self.update_tax_declaration()
        self.set_total_declared_amount()
        self.set_total_exemption_amount()

    def on_cancel(self):
        self.cancel_declaration_history()

    def set_max_amount_of_sub_category(self):
        if not self.declarations:
            return

        for subcategory in self.declarations:
            if not subcategory.exemption_sub_category:
                continue

            check_component = frappe.get_cached_doc(
                "Employee Tax Exemption Sub Category", subcategory.exemption_sub_category
            )

            if check_component.max_amount > 0:
                subcategory.max_amount = check_component.max_amount
            if check_component.max_amount == 0:
                subcategory.max_amount = subcategory.amount

    def update_json_data_in_declaration(self):
        total_nps = 0
        total_pf = 0
        total_pt = 0

        for subcategory in self.declarations:
            check_component = frappe.get_cached_doc(
                "Employee Tax Exemption Sub Category", subcategory.exemption_sub_category
            )

            if check_component.custom_component_type == "NPS":
                total_nps = subcategory.amount
            elif check_component.custom_component_type == "Provident Fund":
                total_pf = subcategory.amount
            elif check_component.custom_component_type == "Professional Tax":
                total_pt = subcategory.amount

        form_data = json.loads(self.custom_declaration_form_data or "[]")

        if not form_data:
            for subcategory in self.declarations:
                check_component = frappe.get_cached_doc(
                    "Employee Tax Exemption Sub Category", subcategory.exemption_sub_category
                )

                form_data.append(
                    {
                        "id": subcategory.exemption_sub_category,
                        "sub_category": subcategory.exemption_sub_category,
                        "exemption_category": subcategory.exemption_category,
                        "max_amount": subcategory.max_amount,
                        "amount": subcategory.amount,
                        "value": subcategory.amount,
                    }
                )

        for entry in form_data:
            subcat = entry.get("sub_category") or entry.get("id")

            component_type = frappe.db.get_value(
                "Employee Tax Exemption Sub Category",
                subcat,
                "custom_component_type",
            )

            if component_type == "NPS":
                entry["amount"] = total_nps
                entry["value"] = total_nps
            elif component_type == "Provident Fund":
                entry["amount"] = total_pf
                entry["value"] = total_pf
            elif component_type == "Professional Tax":
                entry["amount"] = total_pt
                entry["value"] = total_pt

        self.custom_declaration_form_data = json.dumps(form_data)

    def validation_on_section10(self):
        validation_sub_categories = []
        component_sub_category = []

        if self.declarations:
            for declaration in self.declarations:
                sub_category_doc = frappe.get_cached_doc(
                    "Employee Tax Exemption Sub Category", declaration.exemption_sub_category
                )
                component_type = sub_category_doc.custom_component_type

                if component_type in [
                    "Uniform Allowance",
                    "Education Allowance",
                    "Gratuity",
                    "Hostel Allowance",
                    "LTA Reimbursement",
                ]:
                    validation_sub_categories.append(component_type)

        ss_assignment = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "company": self.company,
                "custom_payroll_period": self.payroll_period,
            },
            fields=["name", "from_date", "salary_structure"],
            order_by="from_date desc",
            limit=1,
        )

        if not ss_assignment:
            return

        salary_slip_preview = make_salary_slip(
            source_name=ss_assignment[0].salary_structure,
            employee=self.employee,
            print_format="Salary Slip Standard",
            posting_date=ss_assignment[0].from_date,
            for_preview=1,
        )

        if salary_slip_preview:
            for component in salary_slip_preview.earnings:
                salary_component = frappe.get_cached_doc("Salary Component", component.salary_component)
                if salary_component.component_type == "Tax Exemption":
                    sub_category = salary_component.custom_sub_category
                    if sub_category:
                        component_sub_category.append(sub_category.strip())

        unmatched = []
        for declared_sub in validation_sub_categories:
            if declared_sub.strip() not in component_sub_category:
                unmatched.append(declared_sub.strip())

        if unmatched:
            msg = (
                "The following Section 10 components are not part of your salary"
                " (CTC), so you cannot claim exemption for them:<br><br>"
                + "<br>".join(f"<b>{u}</b>" for u in unmatched)
            )
            frappe.throw(_(msg))

    def set_total_exemption_amount(self):
        self.total_exemption_amount = flt(
            get_total_exemption_amount(self.declarations),
            self.precision("total_exemption_amount"),
        )
        if self.annual_hra_exemption:
            self.total_exemption_amount = self.total_exemption_amount + self.annual_hra_exemption

    def cancel_declaration_history(self):
        history_data = frappe.db.get_list(
            "Tax Declaration History",
            filters={
                "tax_exemption": self.name,
            },
            fields=["name"],
        )

        if history_data:
            frappe.delete_doc("Tax Declaration History", history_data[0].name)

    def update_hra_breakup(self):
        if self.monthly_house_rent and self.custom_status in ["Approved"]:
            array = []
            for t1 in self.custom_hra_breakup:
                array.append(
                    {
                        "month": t1.month,
                        "rent_paid": t1.rent_paid,
                        "basic": t1.earned_basic,
                        "hra": t1.hra_received,
                        "basic_excess": t1.exemption_amount,
                        "exception_amount": t1.exemption_amount,
                    }
                )

            get_latest_history = frappe.get_list(
                "Tax Declaration History",
                filters={"employee": self.employee},
                fields=["name"],
                order_by="posting_date desc",
                limit=1,
            )

            if get_latest_history:
                each_doc = frappe.get_doc("Tax Declaration History", get_latest_history[0].name)

                each_doc.monthly_house_rent = self.monthly_house_rent
                each_doc.rented_in_metro_city = self.rented_in_metro_city
                each_doc.hra_as_per_salary_structure = self.salary_structure_hra
                each_doc.annual_hra_exemption = self.annual_hra_exemption
                each_doc.monthly_hra_exemption = self.monthly_hra_exemption

                each_doc.hra_breakup = []

                for entry in array:
                    each_doc.append(
                        "hra_breakup",
                        {
                            "month": entry["month"],
                            "rent_paid": entry["rent_paid"],
                            "earned_basic": entry["basic"],
                            "hra_received": entry["hra"],
                            "excess_of_rent_paid": entry["basic_excess"],
                            "exemption_amount": entry["exception_amount"],
                        },
                    )

                each_doc.save()

    def update_tax_declaration(self):
        if not self.declarations:
            return

        tax_components = [
            {
                "sub_category": d.exemption_sub_category,
                "category": d.exemption_category,
                "max_amount": d.max_amount,
                "amount": d.amount,
            }
            for d in self.declarations
        ]

        common_fields = {
            "rented_in_metro_city": self.rented_in_metro_city,
            "hra_as_per_salary_structure": self.salary_structure_hra,
            "annual_hra_exemption": self.annual_hra_exemption,
            "monthly_hra_exemption": self.monthly_hra_exemption,
            "total_declared_amount": self.total_declared_amount,
            "total_exemption_amount": self.total_exemption_amount,
            "income_tax": self.custom_income_tax,
            "monthly_house_rent": self.monthly_house_rent,
            "basic_as_per_salary_structure_annual": self.custom_basic,
            "basic_as_per_salary_structure_10": self.custom_basic_as_per_salary_structure,
        }

        declaration_rows = [
            {
                "exemption_sub_category": entry["sub_category"],
                "exemption_category": entry["category"],
                "maximum_exempted_amount": entry["max_amount"],
                "declared_amount": entry["amount"],
            }
            for entry in tax_components
        ]

        existing_history = frappe.get_list(
            "Tax Declaration History",
            filters={
                "employee": self.employee,
                "posting_date": self.custom_posting_date,
            },
            fields=["name"],
            limit=1,
        )

        if existing_history:
            history_doc = frappe.get_doc("Tax Declaration History", existing_history[0].name)

            for key, value in common_fields.items():
                setattr(history_doc, key, value)

            history_doc.declaration_details = []

            for entry in declaration_rows:
                history_doc.append("declaration_details", entry)

            history_doc.save(ignore_permissions=True)

        else:
            history_doc = frappe.get_doc(
                {
                    "doctype": "Tax Declaration History",
                    "employee": self.employee,
                    "employee_name": self.employee_name,
                    "company": self.company,
                    "posting_date": self.custom_posting_date,
                    "payroll_period": self.payroll_period,
                    "tax_exemption": self.name,
                    **common_fields,
                    "declaration_details": declaration_rows,
                }
            )

            history_doc.insert(ignore_permissions=True)

    def calculate_hra_breakup(self):
        if not self.monthly_house_rent:
            self.custom_basic_as_per_salary_structure = None
            self.salary_structure_hra = None
            self.custom_basic = None
            self.annual_hra_exemption = None
            self.monthly_hra_exemption = None
            self.custom_hra_received_annual = None
            self.custom_rent_paid__10_of_basic_annual = None
            self.custom_50_of_basic_metro = None
            return

        final_exemption = 0
        annual_rent = 0
        hra_limit = 0

        company_doc = frappe.get_cached_doc("Company", self.company)
        basic_component = company_doc.basic_component
        hra_component = company_doc.hra_component

        if self.custom_start_date and self.custom_end_date:
            start = getdate(self.custom_start_date)
            end = getdate(self.custom_end_date)

            if start.day > 1:
                start = add_months(start.replace(day=1), 1)

            if start > end:
                total_months = 0
            else:
                total_months = (end.year - start.year) * 12 + (end.month - start.month) + 1
        else:
            total_months = 0

        assignments = frappe.get_all(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "company": self.company,
                "custom_payroll_period": self.payroll_period,
            },
            fields=["from_date", "salary_structure"],
            order_by="from_date asc",
        )

        if not assignments:
            return

        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "company": self.company,
                "custom_payroll_period": self.payroll_period,
            },
            fields=["name"],
        )

        processed_months = len(salary_slips)

        actual_basic = 0
        actual_hra = 0

        for ss in salary_slips:
            slip = frappe.get_doc("Salary Slip", ss.name)

            for comp in slip.earnings:
                if comp.salary_component == basic_component:
                    actual_basic += flt(comp.amount)
                elif comp.salary_component == hra_component:
                    actual_hra += flt(comp.amount)

        latest_assignment = assignments[-1]
        future_months = max(0, total_months - processed_months)

        preview_slip = make_salary_slip(
            source_name=latest_assignment.salary_structure,
            employee=self.employee,
            posting_date=latest_assignment.from_date,
            for_preview=1,
        )

        preview_slip.run_method("calculate_net_pay")

        future_basic = 0
        future_hra = 0

        for comp in preview_slip.earnings:
            if comp.salary_component == basic_component:
                future_basic = flt(comp.amount) * future_months
            elif comp.salary_component == hra_component:
                future_hra = flt(comp.amount) * future_months

        total_basic = actual_basic + future_basic
        total_hra = actual_hra + future_hra

        self.custom_basic = round(total_basic)
        self.salary_structure_hra = round(total_hra)
        self.custom_basic_as_per_salary_structure = round(total_basic * 0.10)

        if total_months > 0:
            ten_percent_basic = total_basic * 0.10
            annual_rent = flt(self.monthly_house_rent) * total_months
            rent_minus_basic = annual_rent - ten_percent_basic

            if self.rented_in_metro_city:
                hra_limit = total_basic * 0.50
            else:
                hra_limit = total_basic * 0.40

            final_exemption = min(rent_minus_basic, total_hra, hra_limit)

        self.custom_hra_received_annual = round(total_hra)
        self.custom_rent_paid__10_of_basic_annual = round(annual_rent - (total_basic * 0.10))
        self.custom_50_of_basic_metro = round(hra_limit)
        self.annual_hra_exemption = round(final_exemption or 0)

        if total_months:
            self.monthly_hra_exemption = round((final_exemption or 0) / total_months)
        else:
            self.monthly_hra_exemption = 0
