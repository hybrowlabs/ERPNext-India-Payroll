from hrms.payroll.doctype.employee_tax_exemption_proof_submission.employee_tax_exemption_proof_submission import (
    EmployeeTaxExemptionProofSubmission,
)
import frappe
from frappe.utils import flt

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from datetime import datetime, timedelta
from datetime import date
from datetime import datetime, timedelta
from datetime import date
from frappe.utils import getdate

class CNEmployeeTaxExemptionProofSubmission(EmployeeTaxExemptionProofSubmission):
    def validate(self):
        super().validate()
        self.set_approved_status_for_auto_component()        
        self.calculate_hra_breakup()
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


    def on_trash(self):

        approved_categories = frappe.get_list(
            "POI Approved Category",
            filters={"proof_id": self.name},
            fields=["name"]
        )

        for category in approved_categories:
            frappe.delete_doc("POI Approved Category", category.name, force=1)

        frappe.db.commit()


    def calculate_hra_breakup(self):
        """
        Calculate HRA exemption based on:
        - Previous salary slips (submitted)
        - Current month draft (cur_basic, cur_hra)
        - Future months (projection)
        """
        if not (self.house_rent_payment_amount and self.rented_from_date and self.rented_to_date and self.custom_tax_regime=="Old Regime"):
            self.custom_hra_received_monthly = 0
            self.custom_hra_received_annual = 0
            self.custom_basic_received_annual = 0
            self.custom_basic_received_monthly = 0
            self.custom_basic_as_per_salary_structure = 0

            self.custom_name = None
            self.custom_pan = None
            self.custom_address_title1 = None
            self.custom_address_title2 = None

            self.custom_current_hra = 0
            self.custom_current_basic = 0

            self.monthly_hra_exemption = 0
            self.custom_annual_eligible_amount = 0
            self.custom_annual_hra_exemption = 0
            self.custom_hra_received=0
            self.custom_rent_paid__10_of_basic_annual=0
            self.custom_50_of_basic_metro=0

            return
        # Initialize amounts
        cur_basic = self.custom_current_basic or 0
        cur_hra = self.custom_current_hra or 0
        prev_basic = prev_hra = 0
        future_basic = future_hra = 0

        start_date = getdate(self.rented_from_date)
        end_date = getdate(self.rented_to_date)
        rent_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1

        # Company salary components
        company = frappe.get_doc("Company", self.company)
        basic_comp = company.basic_component
        hra_comp = company.hra_component
        basic_arrear = company.custom_basic_arrear
        hra_arrear = company.custom_hra_arrear

        # Get latest salary structure assignment
        assignments = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "custom_payroll_period": self.payroll_period,
            },
            fields=["*"],
            order_by="from_date desc",
            limit=1
        )

        if not assignments:
            return

        assignment = assignments[0]
        structure = assignment.salary_structure
        assignment_date = assignment.from_date

        # Get payroll period
        payroll_period = frappe.get_doc("Payroll Period", assignment.custom_payroll_period)
        payroll_start = getdate(payroll_period.start_date)
        payroll_end = getdate(payroll_period.end_date)

        # Calculate total months in period
        period_start = max([start_date, payroll_start, getdate(frappe.get_value("Employee", self.employee, "date_of_joining"))])
        num_months = (payroll_end.year - period_start.year) * 12 + (payroll_end.month - period_start.month) + 1

        # Previous salary slips
        prev_slips = frappe.get_list(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "company": self.company,
                "docstatus": 1,
                "custom_payroll_period": self.payroll_period,
                "name": ["!=", self.name]
            },
            fields=["name"]
        )

        for slip in prev_slips:
            doc = frappe.get_doc("Salary Slip", slip.name)
            for e in doc.earnings:
                if e.salary_component in [basic_comp, basic_arrear]:
                    prev_basic += e.amount
                if e.salary_component in [hra_comp, hra_arrear]:
                    prev_hra += e.amount

        # Future projection: remaining months
        future_count = num_months - len(prev_slips) - 1  # exclude current month
        if future_count > 0:
            preview_slip = make_salary_slip(
                source_name=structure,
                employee=self.employee,
                print_format="Salary Slip Standard",
                posting_date=assignment_date,
                for_preview=1
            )
            for e in preview_slip.earnings:
                if e.salary_component in [basic_comp, basic_arrear]:
                    future_basic += e.amount * future_count
                if e.salary_component in [hra_comp, hra_arrear]:
                    future_hra += e.amount * future_count
                # Add current month
                if not cur_basic:
                    if e.salary_component in [basic_comp, basic_arrear]:
                        cur_basic += e.amount
                if not cur_hra:
                    if e.salary_component in [hra_comp, hra_arrear]:
                        cur_hra += e.amount

        # Total annual amounts
        total_basic = cur_basic + prev_basic + future_basic
        total_hra = cur_hra + prev_hra + future_hra



        self.custom_hra_received_annual = round(total_hra)
        self.custom_basic_received_annual = round(total_basic)
        basic_10_percent = round(total_basic * 0.10)
        self.custom_basic_as_per_salary_structure = basic_10_percent

        # Annual HRA exemption calculation
        annual_rent = self.house_rent_payment_amount * rent_months
        basic_rule2 = round(annual_rent - basic_10_percent)
        metro_limit = round(total_basic * 0.5 if self.rented_in_metro_city else total_basic * 0.4)

        final_exemption = round(min(total_hra, basic_rule2, metro_limit))
        self.custom_annual_eligible_amount = final_exemption
        self.custom_annual_hra_exemption=final_exemption
        self.monthly_hra_exemption = round(final_exemption / rent_months)

        # Other fields
        self.custom_hra_received = self.custom_hra_received_annual
        self.custom_rent_paid__10_of_basic_annual = annual_rent - basic_10_percent
        self.custom_50_of_basic_metro = metro_limit


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


   

    
    def before_update_after_submit(self):
        
        self.set_approved_status_for_auto_component()
        self.get_total_exemption_amount()
        self.insert_approved_proof_in_history()
        self.calculate_hra_exemption()
        # self.set_total_exemption_amount()


    

    def insert_approved_proof_in_history(self):

        if not self.tax_exemption_proofs:
            return

        for d in self.tax_exemption_proofs:

            component = frappe.get_doc(
                "Employee Tax Exemption Sub Category",
                d.exemption_sub_category
            )

            if component.custom_component_type not in [
                "NPS",
                "Professional Tax",
                "Provident Fund"
            ]:

                filters = {
                    "employee": self.employee,
                    "exemption_category": d.exemption_category,
                    "exemption_sub_category": d.exemption_sub_category,
                    "payroll_period": self.payroll_period,
                }

                existing_name = frappe.db.get_value(
                    "POI Approved Category",
                    filters,
                    "name"
                )



                values = {
                    "declared_amount": d.amount,
                    "max_amount": d.max_amount,
                    "date": self.submission_date,
                    "proof_id": self.name,
                    "attach": d.attach_proof,
                    "status": "Pending"
                }

                if not existing_name:
                    frappe.get_doc({
                        "doctype": "POI Approved Category",
                        "employee": self.employee,
                        "exemption_category": d.exemption_category,
                        "exemption_sub_category": d.exemption_sub_category,
                        "payroll_period": self.payroll_period,
                        **values
                    }).insert(ignore_permissions=True)

                else:
                    frappe.db.set_value(
                        "POI Approved Category",
                        existing_name,
                        values
                    )


        if self.house_rent_payment_amount:

            hra_name = frappe.db.get_value(
                "POI Approved Category",
                {
                    "employee": self.employee,
                    "category": "HRA",
                    "payroll_period": self.payroll_period,
                },
                "name"
            )

            hra_values = {
                "annual_hra_exemption": self.custom_annual_eligible_amount,
                "monthly_hra_exemption": self.monthly_hra_exemption,
                "date": self.submission_date,
                "proof_id": self.name,
                "hra_attach": self.custom_hra_proof_attach,
                "hra_paid": self.house_rent_payment_amount,
                "holder_name": self.custom_name,
                "pan": self.custom_pan,
                "address_line1": self.custom_address_title1,
                "status": "Pending"
            }

            if not hra_name:
                frappe.get_doc({
                    "doctype": "POI Approved Category",
                    "employee": self.employee,
                    "category": "HRA",
                    "payroll_period": self.payroll_period,
                    **hra_values
                }).insert(ignore_permissions=True)

            else:
                frappe.db.set_value(
                    "POI Approved Category",
                    hra_name,
                    hra_values
                )


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


