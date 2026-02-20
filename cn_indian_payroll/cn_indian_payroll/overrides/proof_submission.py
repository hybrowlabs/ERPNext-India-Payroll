from hrms.payroll.doctype.employee_tax_exemption_proof_submission.employee_tax_exemption_proof_submission import (
    EmployeeTaxExemptionProofSubmission,
)
import frappe
from frappe.utils import flt

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from datetime import datetime, timedelta
from datetime import date


class CNEmployeeTaxExemptionProofSubmission(EmployeeTaxExemptionProofSubmission):
    def validate(self):
        super().validate()
        self.set_approved_status_for_auto_component()        
        self.calculate_hra_exemption()
        self.set_total_actual_amount()
        self.get_total_exemption_amount()

        if not self.is_new():
            self.insert_approved_proof_in_history()


    def after_insert(self):
        self.insert_approved_proof_in_history()
    
        # if self.submission_date:
        #     self.update_tax_declaration()

    def on_cancel(self):

        approved_categories = frappe.get_list(
            "POI Approved Category",
            filters={"proof_id": self.name},
            fields=["name"]
        )

        for category in approved_categories:
            frappe.delete_doc("POI Approved Category", category.name, force=1)

        frappe.db.commit()


    def update_tax_declaration(self):
        if len(self.tax_exemption_proofs) > 0:
            tax_component = []
            for component in self.tax_exemption_proofs:
                tax_component.append(
                    {
                        "sub_category": component.exemption_sub_category,
                        "category": component.exemption_category,
                        "max_amount": component.max_amount,
                        "amount": component.amount,
                    }
                )

            hra_component = []
            for hra in self.custom_hra_breakup:
                hra_component.append(
                    {
                        "month": hra.month,
                        "rent_paid": hra.rent_paid,
                        "earned_basic": hra.earned_basic,
                        "hra_received": hra.hra_received,
                        "excess_of_rent_paid": hra.excess_of_rent_paid,
                        "exemption_amount": hra.exemption_amount,
                    }
                )

            get_latest_history = frappe.get_list(
                "Tax Declaration History",
                filters={
                    "employee": self.employee,
                    "posting_date": self.submission_date,
                },
                fields=["*"],
                limit=1,
            )

            if len(get_latest_history) > 0:
                each_doc = frappe.get_doc(
                    "Tax Declaration History", get_latest_history[0].name
                )

                each_doc.rented_in_metro_city = self.rented_in_metro_city
                each_doc.hra_as_per_salary_structure = self.custom_hra_received_annual
                each_doc.annual_hra_exemption = self.custom_annual_hra_exemption
                each_doc.monthly_hra_exemption = self.monthly_hra_exemption

                each_doc.basic_as_per_salary_structure_annual = (
                    self.custom_basic_received_annual
                )
                each_doc.basic_as_per_salary_structure_10 = (
                    self.custom_basic_as_per_salary_structure_10
                )

                each_doc.total_declared_amount = self.total_actual_amount
                each_doc.total_exemption_amount = self.exemption_amount
                each_doc.income_tax = self.custom_tax_regime
                each_doc.monthly_house_rent = self.house_rent_payment_amount
                each_doc.total_80d = self.custom_total_80d

                each_doc.declaration_details = []
                for entry in tax_component:
                    each_doc.append(
                        "declaration_details",
                        {
                            "exemption_sub_category": entry["sub_category"],
                            "exemption_category": entry["category"],
                            "maximum_exempted_amount": entry["max_amount"],
                            "declared_amount": entry["amount"],
                        },
                    )

                each_doc.hra_breakup = []
                for hra_entry in hra_component:
                    each_doc.append(
                        "hra_breakup",
                        {
                            "month": hra_entry["month"],
                            "rent_paid": hra_entry["rent_paid"],
                            "earned_basic": hra_entry["earned_basic"],
                            "hra_received": hra_entry["hra_received"],
                            "excess_of_rent_paid": hra_entry["excess_of_rent_paid"],
                            "exemption_amount": hra_entry["exemption_amount"],
                        },
                    )

                each_doc.save()
                frappe.db.commit()

            else:
                insert_history = frappe.get_doc(
                    {
                        "doctype": "Tax Declaration History",
                        "employee": self.employee,
                        "employee_name": self.employee_name,
                        "income_tax": self.custom_income_tax,
                        "company": self.company,
                        "posting_date": self.submission_date,
                        "payroll_period": self.payroll_period,
                        "total_declared_amount": self.total_actual_amount,
                        "total_exemption_amount": self.exemption_amount,
                        "monthly_house_rent": self.house_rent_payment_amount,
                        "rented_in_metro_city": self.rented_in_metro_city,
                        "hra_as_per_salary_structure": self.custom_hra_received_annual,
                        "annual_hra_exemption": self.custom_annual_hra_exemption,
                        "monthly_hra_exemption": self.monthly_hra_exemption,
                        "basic_as_per_salary_structure_annual": self.custom_basic_received_annual,
                        "basic_as_per_salary_structure_10": self.custom_basic_as_per_salary_structure_10,
                        "declaration_details": [
                            {
                                "exemption_sub_category": entry["sub_category"],
                                "exemption_category": entry["category"],
                                "maximum_exempted_amount": entry["max_amount"],
                                "declared_amount": entry["amount"],
                            }
                            for entry in tax_component
                        ],
                        "hra_breakup": [
                            {
                                "month": hra_entry["month"],
                                "rent_paid": hra_entry["rent_paid"],
                                "earned_basic": hra_entry["earned_basic"],
                                "hra_received": hra_entry["hra_received"],
                                "excess_of_rent_paid": hra_entry["excess_of_rent_paid"],
                                "exemption_amount": hra_entry["exemption_amount"],
                            }
                            for hra_entry in hra_component
                        ],
                    }
                )

                insert_history.insert()
                frappe.db.commit()

    def set_total_actual_amount(self):
        total_declared_amount = 0.0
        for d in self.tax_exemption_proofs:
            total_declared_amount += flt(d.amount)

        self.total_actual_amount = round(total_declared_amount)

    def calculate_hra_exemption(self):
        if self.house_rent_payment_amount:
            get_company = frappe.get_doc("Company", self.company)
            basic_component = get_company.basic_component
            basic_arrears_component = get_company.custom_basic_arrear
            hra_component = get_company.hra_component
            hra_arrears_component = get_company.custom_hra_arrear
            month_count = 0

            ss_assignment = frappe.get_list(
                "Salary Structure Assignment",
                filters={
                    "employee": self.employee,
                    "docstatus": 1,
                    "company": self.company,
                    "custom_payroll_period": self.payroll_period,
                },
                fields=[
                    "name",
                    "from_date",
                    "custom_payroll_period",
                    "salary_structure",
                ],
                order_by="from_date desc",
            )

            if ss_assignment:
                first_assignment = next(iter(ss_assignment))
                first_assignment_date = first_assignment.get("from_date")
                first_assignment_structure = first_assignment.get("salary_structure")

                start_date = ss_assignment[-1].from_date
                if ss_assignment[-1].custom_payroll_period:
                    payroll_period = frappe.get_doc(
                        "Payroll Period", ss_assignment[-1].custom_payroll_period
                    )
                    end_date = payroll_period.end_date
                    month_count = (
                        (end_date.year - start_date.year) * 12
                        + end_date.month
                        - start_date.month
                        + 1
                    )

                    cur_basic_amount = 0
                    cur_basic_arrears_amount = 0
                    cur_hra_arrears_amount = 0
                    cur_hra_amount = 0
                    get_salary_slip = frappe.get_list(
                        "Salary Slip",
                        filters={
                            "employee": self.employee,
                            "docstatus": 1,
                            "company": self.company,
                            "custom_payroll_period": self.payroll_period,
                        },
                        fields=["name"],
                    )
                    if len(get_salary_slip) > 0:
                        ss_slip_month_count = len(get_salary_slip)

                        for salary_slip in get_salary_slip:
                            get_salary_doc = frappe.get_doc(
                                "Salary Slip", salary_slip.name
                            )
                            for component in get_salary_doc.earnings:
                                if component.salary_component == basic_component:
                                    cur_basic_amount += component.amount
                                elif component.salary_component == hra_component:
                                    cur_hra_amount += component.amount
                                elif (
                                    component.salary_component
                                    == basic_arrears_component
                                ):
                                    cur_basic_arrears_amount += component.amount
                                elif (
                                    component.salary_component == hra_arrears_component
                                ):
                                    cur_hra_arrears_amount += component.amount
                    else:
                        ss_slip_month_count = 0
                    futute_month_count = month_count - ss_slip_month_count

                    new_salary_slip = make_salary_slip(
                        source_name=first_assignment_structure,
                        employee=self.employee,
                        print_format="Salary Slip Standard for CTC",
                        posting_date=first_assignment_date,
                        for_preview=1,
                    )
                    future_basic_amount = 0
                    future_hra_amount = 0

                    for new_earning in new_salary_slip.earnings:
                        if new_earning.salary_component == basic_component:
                            future_basic_amount = (
                                new_earning.amount * futute_month_count
                            ) + (cur_basic_amount + cur_basic_arrears_amount)

                        if new_earning.salary_component == hra_component:
                            future_hra_amount = (
                                new_earning.amount * futute_month_count
                            ) + (cur_hra_amount + cur_hra_arrears_amount)

                    self.custom_hra_received_annual = round(future_hra_amount)
                    self.custom_hra_received_monthly = round(
                        future_hra_amount / month_count
                    )

                    
                    self.custom_basic_received_annual = round(future_basic_amount)
                    self.custom_basic_received_monthly = round(
                        future_basic_amount / month_count
                    )
                    percentage_basic = (future_basic_amount * 10) / 100
                    self.custom_basic_as_per_salary_structure_10 = round(
                        percentage_basic
                    )

                    annual_hra_amount = self.house_rent_payment_amount * month_count

                    basic_rule2 = round(annual_hra_amount - percentage_basic)
                    if self.rented_in_metro_city == 0:
                        non_metro_or_metro = (future_basic_amount * 40) / 100
                    elif self.rented_in_metro_city == 1:
                        non_metro_or_metro = (future_basic_amount * 50) / 100

                    final_hra_exemption = round(
                        min(basic_rule2, future_hra_amount, non_metro_or_metro)
                    )

                    # self.custom_rent_paid__10_of_basic_annual = round(basic_rule2)

                    self.custom_annual_hra_exemption = round(final_hra_exemption)
                    self.custom_annual_eligible_amount = round(final_hra_exemption)
                    self.monthly_hra_exemption = round(
                        final_hra_exemption / month_count
                    )

                    self.custom_hra_received = round(future_hra_amount)
                    self.custom_rent_paid__10_of_basic_annual = round(basic_rule2)

                    months = []
                    current_date = start_date

                    while current_date <= end_date:
                        month_name = current_date.strftime("%B")
                        if month_name not in months:
                            months.append(month_name)
                        current_date = (
                            current_date.replace(day=28) + timedelta(days=4)
                        ).replace(day=1)

                    earned_basic = 0
                    if self.rented_in_metro_city == 1:
                        earned_basic = (
                            (self.custom_basic_as_per_salary_structure_10 * 10)
                            * 50
                            / 100
                        )
                    else:
                        earned_basic = (
                            (self.custom_basic_as_per_salary_structure_10 * 10)
                            * 40
                            / 100
                        )

                    percentage = 50 if self.rented_in_metro_city else 40

                    self.custom_50_of_basic_metro = round(
                        future_basic_amount * percentage / 100
                    )

                    self.custom_hra_breakup = []
                    for i in range(len(months)):
                        self.append(
                            "custom_hra_breakup",
                            {
                                "month": months[i],
                                "rent_paid": round(self.house_rent_payment_amount),
                                "hra_received": round(
                                    self.custom_hra_received_annual / month_count
                                ),
                                "earned_basic": round(earned_basic / month_count),
                                "excess_of_rent_paid": round(basic_rule2 / month_count),
                                "exemption_amount": final_hra_exemption / month_count,
                            },
                        )

        else:
            self.custom_annual_hra_exemption = 0
            self.monthly_hra_exemption = 0
            self.custom_hra_received = 0
            self.custom_rent_paid__10_of_basic_annual = 0
            self.custom_50_of_basic_metro = 0
            self.custom_hra_breakup = []
            self.custom_hra_received_annual = 0
            self.custom_hra_received_monthly = 0
            self.custom_basic_received_annual = 0
            self.custom_basic_received_monthly = 0
            self.custom_basic_as_per_salary_structure_10 = 0

   

    
    def before_update_after_submit(self):
        
        self.set_approved_status_for_auto_component()
        self.get_total_exemption_amount()
        self.insert_approved_proof_in_history()
        self.calculate_hra_exemption()
        # self.set_total_exemption_amount()


    def insert_approved_proof_in_history(self):
        if self.tax_exemption_proofs:
            for d in self.tax_exemption_proofs:
                if d.custom_proof_status == "Pending":
                    get_approved_proof = frappe.get_list("POI Approved Category",
                        filters={
                            "employee": self.employee,
                            "exemption_category": d.exemption_category,
                            "exemption_sub_category": d.exemption_sub_category,
                            "payroll_period": self.payroll_period,
                        },
                        fields=["name"]
                    )
                    if not get_approved_proof:
                        approved_doc = frappe.get_doc({
                            "doctype": "POI Approved Category",
                            "employee": self.employee,
                            "exemption_category": d.exemption_category,
                            "exemption_sub_category": d.exemption_sub_category,
                            "declared_amount": d.amount,
                            "max_amount": d.max_amount,
                            "payroll_period": self.payroll_period,
                            "date":self.submission_date,
                            "proof_id": self.name,
                            "attach":d.attach_proof
                        })
                        approved_doc.insert()
                        frappe.db.commit()
                elif d.custom_proof_status == "Rejected":
                    get_approved_proof = frappe.get_list("POI Approved Category",
                        filters={
                            "employee": self.employee,
                            "exemption_category": d.exemption_category,
                            "exemption_sub_category": d.exemption_sub_category,
                            "payroll_period": self.payroll_period,
                        },
                        fields=["name"]
                    )
                    approved_doc = frappe.get_doc("POI Approved Category", get_approved_proof[0].name)
                    if approved_doc.declared_amount != d.amount:
                        approved_doc.declared_amount = d.amount
                        approved_doc.max_amount = d.max_amount
                        approved_doc.date = self.submission_date
                        approved_doc.proof_id = self.name
                        approved_doc.attach = d.attach_proof
                        approved_doc.status = "Pending"
                        approved_doc.save()
                        frappe.db.commit()
                # elif d.custom_proof_status == "Approved":
                #     get_approved_proof = frappe.get_list("POI Approved Category",
                #         filters={
                #             "employee": self.employee,
                #             "exemption_category": d.exemption_category,
                #             "exemption_sub_category": d.exemption_sub_category,
                #             "payroll_period": self.payroll_period,
                #         },
                #         fields=["name"]
                #     )
                #     approved_doc = frappe.get_doc("POI Approved Category", get_approved_proof[0].name)
                #     if approved_doc.custom_proof_status != d.amount:
                        
                #         approved_doc.declared_amount = d.amount
                #         approved_doc.max_amount = d.max_amount
                #         approved_doc.date = self.submission_date
                #         approved_doc.proof_id = self.name
                #         approved_doc.attach = d.attach_proof
                #         approved_doc.status = "Pending"
                #         approved_doc.save()
                #         frappe.db.commit()

        if self.house_rent_payment_amount:
            get_approved_proof = frappe.get_list("POI Approved Category",
                    filters={
                        "employee": self.employee,
                        "category": "HRA",
                        "payroll_period": self.payroll_period,
                    },
                    fields=["name"]
                )
            if not get_approved_proof:
                approved_doc = frappe.get_doc({
                    "doctype": "POI Approved Category",
                    "employee": self.employee,
                    "category": "HRA",
                    "annual_hra_exemption": self.custom_annual_eligible_amount,
                    "monthly_hra_exemption": self.monthly_hra_exemption,
                    "payroll_period": self.payroll_period,
                    "date":self.submission_date,
                    "proof_id": self.name,
                    "hra_attach":self.custom_hra_proof_attach,
                    "hra_paid": self.house_rent_payment_amount,
                    "holder_name": self.custom_name,
                    "pan": self.custom_pan,
                    "address_line1": self.custom_address_title1
                })
                approved_doc.insert()
                frappe.db.commit()
            else:
                approved_doc = frappe.get_doc("POI Approved Category", get_approved_proof[0].name)
                approved_doc.annual_hra_exemption = self.custom_annual_eligible_amount
                approved_doc.monthly_hra_exemption = self.monthly_hra_exemption
                approved_doc.date = self.submission_date
                approved_doc.proof_id = self.name
                approved_doc.hra_attach = self.custom_hra_proof_attach
                approved_doc.save()
                frappe.db.commit()


    def set_approved_status_for_auto_component(self):

        for d in self.tax_exemption_proofs:

            sub_category = frappe.db.get(
                "Employee Tax Exemption Sub Category",
                d.exemption_sub_category,
                
            )

            if sub_category.custom_component_type in ["NPS", "Professional Tax", "Provident Fund"]:
                d.custom_proof_status = "Approved"




    def get_total_exemption_amount(self):

        exemptions = frappe._dict()

        for d in self.tax_exemption_proofs:

            if d.custom_proof_status != "Approved":
                continue

            exemptions.setdefault(d.exemption_category, frappe._dict())

            category_max_amount = exemptions.get(d.exemption_category).max_amount

            if not category_max_amount:
                category_max_amount = frappe.db.get_value(
                    "Employee Tax Exemption Category",
                    d.exemption_category,
                    "max_amount"
                )

                exemptions.get(d.exemption_category).max_amount = category_max_amount


            sub_category_exemption_amount = (
                d.max_amount
                if (d.max_amount and flt(d.amount) > flt(d.max_amount))
                else d.amount
            )


            exemptions.get(d.exemption_category).setdefault(
                "total_exemption_amount", 0.0
            )

            exemptions.get(d.exemption_category).total_exemption_amount += flt(
                sub_category_exemption_amount
            )


            if (
                category_max_amount
                and exemptions.get(d.exemption_category).total_exemption_amount > category_max_amount
            ):
                exemptions.get(d.exemption_category).total_exemption_amount = category_max_amount


        total_exemption_amount = sum(
            flt(d.total_exemption_amount) for d in exemptions.values()
        )

        self.exemption_amount = round(total_exemption_amount + self.custom_annual_hra_exemption)



        # return total_exemption_amount


