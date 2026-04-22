import frappe
from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import (
    EmployeeTaxExemptionDeclaration,
)
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import getdate, flt, add_months
from frappe.utils import flt
from hrms.hr.utils import (
    calculate_annual_eligible_hra_exemption,
    get_total_exemption_amount,
    validate_active_employee,
    validate_duplicate_exemption_for_payroll_period,
    validate_tax_declaration,
)

from datetime import datetime, timedelta
from datetime import date
import json
from dateutil.relativedelta import relativedelta
from frappe import _


class CustomEmployeeTaxExemptionDeclaration(EmployeeTaxExemptionDeclaration):

    def before_save(self):
        self.update_json_data_in_declaration()

    def before_update_after_submit(self):

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

            check_component = frappe.get_doc(
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
            check_component = frappe.get_doc("Employee Tax Exemption Sub Category", subcategory.exemption_sub_category)

            if check_component.custom_component_type == "NPS":
                total_nps = subcategory.amount

            elif check_component.custom_component_type == "Provident Fund":
                total_pf = subcategory.amount

            elif check_component.custom_component_type == "Professional Tax":
                total_pt = subcategory.amount

        form_data = json.loads(self.custom_declaration_form_data or '[]')

        if not form_data:
            for subcategory in self.declarations:
                check_component = frappe.get_doc("Employee Tax Exemption Sub Category", subcategory.exemption_sub_category)

                form_data.append({
                    "id": subcategory.exemption_sub_category,
                    "sub_category": subcategory.exemption_sub_category,
                    "exemption_category": subcategory.exemption_category,
                    "max_amount": subcategory.max_amount,
                    "amount": subcategory.amount,
                    "value": subcategory.amount
                })

        for entry in form_data:
            subcat = entry.get("sub_category") or entry.get("id")

            component_type = frappe.db.get_value(
                "Employee Tax Exemption Sub Category",
                subcat,
                "custom_component_type"
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



   



    def set_total_exemption_amount(self):

        self.total_exemption_amount = flt(
            get_total_exemption_amount(self.declarations),
            self.precision("total_exemption_amount"),
        )
        if self.annual_hra_exemption:
            self.total_exemption_amount = (
                self.total_exemption_amount + self.annual_hra_exemption
            )




    def cancel_declaration_history(self):
        history_data = frappe.db.get_list(
            "Tax Declaration History",
            filters={
                "tax_exemption": self.name,
            },
            fields=["*"],
        )

        if len(history_data) > 0:
            data_doc = frappe.get_doc("Tax Declaration History", history_data[0].name)
            frappe.delete_doc("Tax Declaration History", data_doc.name)

    

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
            history_doc = frappe.get_doc(
                "Tax Declaration History", existing_history[0].name
            )

            for key, value in common_fields.items():
                setattr(history_doc, key, value)

            history_doc.declaration_details = []

            for entry in tax_components:
                history_doc.append("declaration_details", {
                    "exemption_sub_category": entry["sub_category"],
                    "exemption_category": entry["category"],
                    "maximum_exempted_amount": entry["max_amount"],
                    "declared_amount": entry["amount"],
                })

            history_doc.save(ignore_permissions=True)

        else:
            history_doc = frappe.get_doc({
                "doctype": "Tax Declaration History",
                "employee": self.employee,
                "employee_name": self.employee_name,
                "company": self.company,
                "posting_date": self.custom_posting_date,
                "payroll_period": self.payroll_period,
                "tax_exemption": self.name,
                **common_fields,
                "declaration_details": [
                    {
                        "exemption_sub_category": entry["sub_category"],
                        "exemption_category": entry["category"],
                        "maximum_exempted_amount": entry["max_amount"],
                        "declared_amount": entry["amount"],
                    }
                    for entry in tax_components
                ],
            })

            history_doc.insert(ignore_permissions=True)

        frappe.db.commit()



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

        company_doc = frappe.get_doc("Company", self.company)
        basic_component = company_doc.basic_component
        hra_component = company_doc.hra_component

        payroll_period = frappe.get_doc("Payroll Period", self.payroll_period)
        payroll_start = getdate(payroll_period.start_date)
        payroll_end = getdate(payroll_period.end_date)

        if self.custom_start_date and self.custom_end_date:

            start = getdate(self.custom_start_date)
            end = getdate(self.custom_end_date)

            if start.day > 1:
                start = add_months(start.replace(day=1), 1)

            if start > end:
                total_months = 0
            else:
                total_months = (
                    (end.year - start.year) * 12
                    + (end.month - start.month)
                    + 1
                )
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

        self.custom_rent_paid__10_of_basic_annual = round(
            annual_rent - (total_basic * 0.10)
        )

        self.custom_50_of_basic_metro = round(hra_limit)

        self.annual_hra_exemption = round(final_exemption or 0)

        if total_months:
            self.monthly_hra_exemption = round(
                (final_exemption or 0) / total_months
            )
        else:
            self.monthly_hra_exemption = 0