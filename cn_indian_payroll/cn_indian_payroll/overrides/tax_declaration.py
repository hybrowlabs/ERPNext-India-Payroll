import frappe
from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import (
    EmployeeTaxExemptionDeclaration,
)
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

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
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta


class CustomEmployeeTaxExemptionDeclaration(EmployeeTaxExemptionDeclaration):

    def before_save(self):
        self.update_json_data()
        if self.custom_tax_regime == "Old Regime":
            form_data = json.loads(self.custom_declaration_form_data or "{}")

            for k in self.declarations:
                if k.exemption_sub_category == "Employee Provident Fund (Auto)":
                    form_data["pfValue"] = round(k.amount)

                elif k.exemption_sub_category == "NPS Contribution by Employer":
                    form_data["nineNumber"] = round(k.amount)

                elif k.exemption_sub_category == "Tax on employment (Professional Tax)":
                    form_data["nineteenNumber"] = round(k.amount)

            self.custom_declaration_form_data = json.dumps(form_data)

        if self.custom_tax_regime == "New Regime":
            form_data = json.loads(self.custom_declaration_form_data or "{}")

            for k in self.declarations:
                if k.exemption_sub_category == "NPS Contribution by Employer":
                    form_data["nineNumber"] = round(k.amount)

            self.custom_declaration_form_data = json.dumps(form_data)

    def before_update_after_submit(self):
        self.update_json_data()
        # self.process_form_data()
        # self.mediclaim_condition()

        self.calculate_hra_breakup()
        self.update_tax_declaration()
        self.validation_on_section10()
        self.set_total_declared_amount()
        self.set_total_exemption_amount()



    def update_json_data(self):
        if self.declarations:
            form_data = json.loads(self.custom_declaration_form_data or "{}")

            # Mapping: name → field
            field_map = {
                "Mediclaim Self, Spouse & Children (Below 60 years)": "amount",
                "Mediclaim Self (Senior Citizen - 60 years & above)": "amount3",
                "Parents (Below 60 years)": "mpAmount3",
                "Parents (Senior Citizen - 60 years & above)": "mpAmount4",
                "Preventive Checkup (Self + Family)": "mp5",
                "Preventive Checkup (Parents)": "mpAmount6",
                "Interest Paid On Home Loan": "hlAmount",
                "Investments In PF(Auto)": "pfValue",
                "Pension Scheme Investments & ULIP": "aValue2",
                "Housing Loan Principal Repayment": "bValue1",
                "PPF - Public Provident Fund": "amount4",
                "Home Loan Account Of National Housing Bank": "dValue1",
                "LIC- Life Insurance Premium Directly Paid By Employee": "eValue1",
                "NSC - National Saving Certificate": "fValue1",
                "Mutual Funds - Notified Under Clause 23D Of Section 10": "gValue1",
                "ELSS - Equity Link Saving Scheme Of Mutual Funds": "hValue1",
                "Tuition Fees For Full Time Education": "iValue1",
                "Fixed Deposits In Banks (Period As Per Income Tax Guidelines)": "jValue1",
                "5 Years Term Deposit An Account Under Post Office Term Deposit Rules": "kValue1",
                "Others": "kValue2",
                "(Medical treatment / insurance of handicapped dependant)": "fourValue",
                "Medical treatment (specified diseases only)": "fiveNumber",
                "Interest repayment of Loan for higher education": "sixNumber",
                "Deduction for Physically Disabled": "sevenNumber",
                "Donation U/S 80G": "eightNumber",
                "NPS Deduction U/S 80CCD(2)(Employer NPS deduction)": "nineNumber",
                "First HSG Loan Interest Ded.(80EE)": "tenNumber",
                "Contribution in National Pension Scheme": "elevenNumber",
                "Tax Incentive for Affordable Housing for Ded U/S 80EEA": "twelveNumber1",
                "Tax Incentives for Electric Vehicles for Ded U/S 80EEB": "fifteenNumber",
                "Donations/contribution made to a political party or an electoral trust": "sixteenNumber",
                "Interest on deposits in saving account for Ded U/S 80TTA": "seventeenNumber",
                "Interest on deposits in saving account for Ded U/S 80TTB": "eighteenNumber",
                "P.T. Paid by employee": "nineteenNumber",
                "Deduction U/S 80GG": "twentyNumber",
                "Rajiv Gandhi Equity Saving Scheme 80CCG": "twentyoneNumber",
                "Uniform Allowance": "twentyFour",
                "Education Allowance": "thirteen",
                "Hostel Allowance": "twentysix",
                "Gratuity": "twentyseven",
                "LTA U/s 10 (5)": "twentyeight",
            }

            for row in self.declarations:
                key = field_map.get(row.exemption_sub_category)
                if key:
                    form_data[key] = round(row.amount)

            self.custom_declaration_form_data = json.dumps(form_data)

    def mediclaim_condition(self):
        if self.custom_tax_regime == "Old Regime":
            form_data = json.loads(self.custom_declaration_form_data or "{}")



            name_value = form_data.get("nameValue")
            address_one_value = form_data.get("addressoneValue")
            pan_value = form_data.get("panValue")
            address_two_value = form_data.get("addresstwoValue")
            type_value = form_data.get("typeValue")
            address_three_value = form_data.get("addressThreeValue")

            missing_fields = []
            if not name_value:
                missing_fields.append("Name")
            if not address_one_value:
                missing_fields.append("Address One")
            if not pan_value:
                missing_fields.append("PAN")
            if not address_two_value:
                missing_fields.append("Address Two")
            if not type_value:
                missing_fields.append("Type")
            if not address_three_value:
                missing_fields.append("Address Three")


    # -----------validate section10 components on employee is eligible or not----------------

    def validation_on_section10(self):
        if self.custom_tax_regime != "Old Regime":
            return

        form_data = json.loads(self.custom_declaration_form_data or "{}")

        allowances = {
            "twentyeight": "LTA Allowance",
            "twentysix": "Hostel Allowance",
            "twentyseven": "Gratuity",
            "twentyFour": "Uniform Allowance",
            "thirteen": "Education Allowance",
        }

        selected_allowances = {
            key: value for key, value in allowances.items() if form_data.get(key, 0)
        }
        valid_components = frappe.get_all(
            "Salary Component",
            filters={"component_type": "Tax Exemption", "disabled": 0},
            fields=["name", "custom_sub_category"],
        )
        component_map = {
            comp["custom_sub_category"]: comp["name"] for comp in valid_components
        }

        required_components = {
            category: component_map.get(sub_category)
            for category, sub_category in selected_allowances.items()
        }

        if (
            "Hostel Allowance" in selected_allowances.values()
            and required_components.get("twentysix") is None
        ):
            frappe.throw("You are not allow to define the Hostel Allowance")

        if (
            "LTA Allowance" in selected_allowances.values()
            and required_components.get("twentyeight") is None
        ):
            frappe.throw("You are not allow to define the LTA Allowance")

        if (
            "Uniform Allowance" in selected_allowances.values()
            and required_components.get("twentyFour") is None
        ):
            frappe.throw("You are not allow to define the Uniform Allowance")

        if (
            "Education Allowance" in selected_allowances.values()
            and required_components.get("thirteen") is None
        ):
            frappe.throw("You are not allow to define the Education Allowance")

        if (
            "Gratuity" in selected_allowances.values()
            and required_components.get("twentyseven") is None
        ):
            frappe.throw("You are not allow to define the Gratuity")

        # Fetch latest Salary Structure Assignment
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

        # Generate Salary Slip Preview
        salary_slip_preview = make_salary_slip(
            source_name=ss_assignment[0].salary_structure,
            employee=self.employee,
            print_format="Salary Slip Standard for CTC",
            posting_date=ss_assignment[0].from_date,
            for_preview=1,
        )

        available_components = {
            earning.salary_component for earning in salary_slip_preview.earnings
        }

        for key, component in required_components.items():
            if component and component not in available_components:
                frappe.throw(f"You are not eligible to declare {allowances[key]}")

    def set_total_exemption_amount(self):
        self.total_exemption_amount = flt(
            get_total_exemption_amount(self.declarations),
            self.precision("total_exemption_amount"),
        )
        if self.annual_hra_exemption:
            self.total_exemption_amount = (
                self.total_exemption_amount + self.annual_hra_exemption
            )

    def on_cancel(self):
        self.cancel_declaration_history()

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

    def update_hra_breakup(self):
        if self.monthly_house_rent:
            if self.workflow_state in ["Approved"]:
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
                    fields=["*"],
                    order_by="posting_date desc",
                    limit=1,
                )

                if len(get_latest_history) > 0:
                    each_doc = frappe.get_doc(
                        "Tax Declaration History", get_latest_history[0].name
                    )

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
                    frappe.db.commit()

    def update_tax_declaration(self):
        if self.workflow_state in ["Approved"]:
            if len(self.declarations) > 0:
                tax_component = []
                for component in self.declarations:
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
                        "posting_date": self.custom_posting_date,
                    },
                    fields=["*"],
                    limit=1,
                )

                if len(get_latest_history) > 0:
                    each_doc = frappe.get_doc(
                        "Tax Declaration History", get_latest_history[0].name
                    )

                    each_doc.rented_in_metro_city = self.rented_in_metro_city
                    each_doc.hra_as_per_salary_structure = self.salary_structure_hra
                    each_doc.annual_hra_exemption = self.annual_hra_exemption
                    each_doc.monthly_hra_exemption = self.monthly_hra_exemption
                    each_doc.total_declared_amount = self.total_declared_amount
                    each_doc.total_exemption_amount = self.total_exemption_amount
                    each_doc.income_tax = self.custom_income_tax
                    each_doc.monthly_house_rent = self.monthly_house_rent

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
                            "posting_date": self.custom_posting_date,
                            "payroll_period": self.payroll_period,
                            "tax_exemption": self.name,
                            "total_declared_amount": self.total_declared_amount,
                            "total_exemption_amount": self.total_exemption_amount,
                            "monthly_house_rent": self.monthly_house_rent,
                            "rented_in_metro_city": self.rented_in_metro_city,
                            "hra_as_per_salary_structure": self.salary_structure_hra,
                            "annual_hra_exemption": self.annual_hra_exemption,
                            "monthly_hra_exemption": self.monthly_hra_exemption,
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
                                    "excess_of_rent_paid": hra_entry[
                                        "excess_of_rent_paid"
                                    ],
                                    "exemption_amount": hra_entry["exemption_amount"],
                                }
                                for hra_entry in hra_component
                            ],
                        }
                    )

                    insert_history.insert()
                    frappe.db.commit()

    def insert_declaration_history(self):
        if self.employee:
            declaration_details = []
            hra_breakup = []

            for i in self.declarations:
                declaration_details.append(
                    {
                        "exemption_sub_category": i.exemption_sub_category,
                        "exemption_category": i.exemption_category,
                        "maximum_exempted_amount": i.max_amount,
                        "declared_amount": i.amount,
                    }
                )

            for j in self.custom_hra_breakup:
                hra_breakup.append(
                    {
                        "month": j.month,
                        "rent_paid": j.rent_paid,
                        "earned_basic": j.earned_basic,
                        "hra_received": j.hra_received,
                        "excess_of_rent_paid": j.excess_of_rent_paid,
                        "exemption_amount": j.exemption_amount,
                    }
                )

            insert_doc = frappe.get_doc(
                {
                    "doctype": "Tax Declaration History",
                    "employee": self.employee,
                    "employee_name": self.employee_name,
                    "income_tax": self.custom_income_tax,
                    "company": self.company,
                    "posting_date": frappe.utils.nowdate(),
                    "payroll_period": self.payroll_period,
                    "monthly_house_rent": self.monthly_house_rent,
                    "rented_in_metro_city": self.rented_in_metro_city,
                    "hra_as_per_salary_structure": self.salary_structure_hra,
                    "total_declared_amount": self.total_declared_amount,
                    "annual_hra_exemption": self.annual_hra_exemption,
                    "monthly_hra_exemption": self.monthly_hra_exemption,
                    "total_exemption_amount": self.total_exemption_amount,
                    "tax_exemption": self.name,
                    "declaration_details": declaration_details,
                    "hra_breakup": hra_breakup,
                }
            )

            insert_doc.insert()

    # --------Insert HRA Breakup Table & Annual HRA and Basic----------------

    def calculate_hra_breakup(self):
        if self.monthly_house_rent and self.custom_check == 0:
            get_company = frappe.get_doc("Company", self.company)
            basic_component = get_company.basic_component
            hra_component = get_company.hra_component

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
                            ) + cur_basic_amount

                        if new_earning.salary_component == hra_component:
                            future_hra_amount = (
                                new_earning.amount * futute_month_count
                            ) + cur_hra_amount

                    self.salary_structure_hra = round(future_hra_amount)
                    self.custom_basic = round(future_basic_amount)
                    percentage_basic = (future_basic_amount * 10) / 100
                    self.custom_basic_as_per_salary_structure = round(percentage_basic)

                    annual_hra_amount = self.monthly_house_rent * month_count

                    basic_rule2 = round(annual_hra_amount - percentage_basic)
                    if self.rented_in_metro_city == 0:
                        non_metro_or_metro = (future_basic_amount * 40) / 100
                    elif self.rented_in_metro_city == 1:
                        non_metro_or_metro = (future_basic_amount * 50) / 100

                    final_hra_exemption = round(
                        min(basic_rule2, future_hra_amount, non_metro_or_metro)
                    )

                    self.annual_hra_exemption = round(final_hra_exemption)
                    self.monthly_hra_exemption = round(
                        final_hra_exemption / month_count
                    )

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
                            (self.custom_basic_as_per_salary_structure * 10) * 50 / 100
                        )
                    else:
                        earned_basic = (
                            (self.custom_basic_as_per_salary_structure * 10) * 40 / 100
                        )

                    self.custom_hra_breakup = []
                    for i in range(len(months)):
                        self.append(
                            "custom_hra_breakup",
                            {
                                "month": months[i],
                                "rent_paid": round(annual_hra_amount),
                                "hra_received": round(self.salary_structure_hra),
                                "earned_basic": round(earned_basic),
                                "excess_of_rent_paid": round(basic_rule2),
                                "exemption_amount": final_hra_exemption,
                            },
                        )

        elif self.monthly_house_rent == 0  or self.monthly_house_rent == None and self.custom_check == 0:
            self.custom_basic_as_per_salary_structure = None
            self.salary_structure_hra = None
            self.custom_basic = None
            self.custom_hra_breakup = []
            self.annual_hra_exemption = None
            self.monthly_hra_exemption = None
        elif self.monthly_house_rent == 0  or self.monthly_house_rent == None and self.custom_check == 1:
            self.custom_basic_as_per_salary_structure = None
            self.salary_structure_hra = None
            self.custom_basic = None
            self.custom_hra_breakup = []
            self.annual_hra_exemption = None
            self.monthly_hra_exemption = None

    def process_form_data(self):
        if self.custom_tax_regime == "Old Regime":
            if self.custom_status in ["Approved", "Pending"]:
                form_data = json.loads(self.custom_declaration_form_data or "{}")

                # Extract numbers from the form data
                numbers = [
                    {
                        "field": "amount",
                        "name": "Mediclaim Self, Spouse & Children (Below 60 years)",
                    },
                    {
                        "field": "amount3",
                        "name": "Mediclaim Self (Senior Citizen - 60 years & above)",
                    },
                    {"field": "mpAmount3", "name": "Parents (Below 60 years)"},
                    {
                        "field": "mpAmount4",
                        "name": "Parents (Senior Citizen - 60 years & above)",
                    },
                    {"field": "mp5", "name": "Preventive Checkup (Self + Family)"},
                    {"field": "mpAmount6", "name": "Preventive Checkup (Parents)"},
                    # ... (other fields not related to 80D)
                    {"field": "hlAmount", "name": "Interest Paid On Home Loan"},
                    {"field": "pfValue", "name": "Investments In PF(Auto)"},
                    {"field": "aValue2", "name": "Pension Scheme Investments & ULIP"},
                    {"field": "bValue1", "name": "Housing Loan Principal Repayment"},
                    {"field": "amount4", "name": "PPF - Public Provident Fund"},
                    {
                        "field": "dValue1",
                        "name": "Home Loan Account Of National Housing Bank",
                    },
                    {"field": "eValue1", "name": "LIC- Life Insurance Premium Directly Paid By Employee"},
                    {"field": "fValue1", "name": "NSC - National Saving Certificate"},
                    {
                        "field": "gValue1",
                        "name": "Mutual Funds - Notified Under Clause 23D Of Section 10",
                    },
                    {
                        "field": "hValue1",
                        "name": "ELSS - Equity Link Saving Scheme Of Mutual Funds",
                    },
                    {"field": "iValue1", "name": "Tuition Fees For Full Time Education"},
                    {"field": "jValue1", "name": "Fixed Deposits In Banks (Period As Per Income Tax Guidelines)"},
                    {
                        "field": "kValue1",
                        "name": "5 Years Term Deposit An Account Under Post Office Term Deposit Rules",
                    },
                    {"field": "kValue2", "name": "Others"},
                    {
                        "field": "fourValue",
                        "name": "(Medical treatment / insurance of handicapped dependant)",
                    },
                    {
                        "field": "fiveNumber",
                        "name": "Medical treatment (specified diseases only)",
                    },
                    {"field": "sixNumber", "name": "Interest repayment of Loan for higher education"},
                    {
                        "field": "sevenNumber",
                        "name": "Deduction for Physically Disabled",
                    },
                    {"field": "eightNumber", "name": "Donation U/S 80G"},
                    {"field": "nineNumber", "name": "NPS Deduction U/S 80CCD(2)(Employer NPS deduction)"},
                    {
                        "field": "tenNumber",
                        "name": "First HSG Loan Interest Ded.(80EE)",
                    },
                    {
                        "field": "elevenNumber",
                        "name": "Contribution in National Pension Scheme",
                    },
                    {
                        "field": "twelveNumber1",
                        "name": "Tax Incentive for Affordable Housing for Ded U/S 80EEA",
                    },
                    {
                        "field": "fifteenNumber",
                        "name": "Tax Incentives for Electric Vehicles for Ded U/S 80EEB",
                    },
                    {
                        "field": "sixteenNumber",
                        "name": "Donations/contribution made to a political party or an electoral trust",
                    },
                    {
                        "field": "seventeenNumber",
                        "name": "Interest on deposits in saving account for Ded U/S 80TTA",
                    },
                    {
                        "field": "eighteenNumber",
                        "name": "Interest on deposits in saving account for Ded U/S 80TTB",
                    },
                    {"field": "nineteenNumber", "name": "P.T. Paid by employee"},
                    {"field": "twentyNumber", "name": "Deduction U/S 80GG"},
                    {
                        "field": "twentyoneNumber",
                        "name": "Rajiv Gandhi Equity Saving Scheme 80CCG",
                    },
                    {"field": "twentyFour", "name": "Uniform Allowance"},
                    {"field": "thirteen", "name": "Education Allowance"},
                    {"field": "twentysix", "name": "Hostel Allowance"},
                    {"field": "twentyseven", "name": "Gratuity"},
                    {"field": "twentyeight", "name": "LTA U/s 10 (5)"},
                ]

                mediclaim_self_below = float(form_data.get("amount", 0))  # A
                mediclaim_self_above = float(form_data.get("amount3", 0))  # B
                mediclaim_parent_below = float(form_data.get("mpAmount3", 0))  # C
                mediclaim_parent_above = float(form_data.get("mpAmount4", 0))  # D
                heal_self = float(form_data.get("mp5", 0))  # E
                heal_parent = float(form_data.get("mpAmount6", 0))  # F

                limit_self_below = 25000
                limit_self_above = 50000
                limit_parent_below = 25000
                limit_parent_above = 50000
                limit_health_checkup_total = 5000

                eligible_self_below = min(mediclaim_self_below, limit_self_below)  # A
                eligible_self_above = min(mediclaim_self_above, limit_self_above)  # B
                eligible_parent_below = min(
                    mediclaim_parent_below, limit_parent_below
                )  # C
                eligible_parent_above = min(
                    mediclaim_parent_above, limit_parent_above
                )  # D

                eligible_heal_self = min(
                    heal_self,
                    limit_self_below - eligible_self_below,
                    limit_self_above - eligible_self_above,
                )
                eligible_heal_parent = min(
                    heal_parent,
                    limit_parent_below - eligible_parent_below,
                    limit_parent_above - eligible_parent_above,
                )

                total_health_checkup = eligible_heal_self + eligible_heal_parent
                if total_health_checkup > limit_health_checkup_total:
                    if eligible_heal_self >= limit_health_checkup_total:
                        eligible_heal_self = limit_health_checkup_total
                        eligible_heal_parent = 0
                    else:
                        eligible_heal_parent = (
                            limit_health_checkup_total - eligible_heal_self
                        )

                form_data["amount"] = eligible_self_below
                form_data["amount3"] = eligible_self_above
                form_data["mpAmount3"] = eligible_parent_below
                form_data["mpAmount4"] = eligible_parent_above
                form_data["mp5"] = eligible_heal_self
                form_data["mpAmount6"] = eligible_heal_parent

                declarations = []
                for item in numbers:
                    value = float(form_data.get(item["field"], 0))

                    if value <= 0:
                        continue

                    get_doc1 = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={"is_active": 1, "name": item["name"]},
                        fields=["name", "exemption_category", "max_amount"],
                    )

                    if get_doc1:
                        declarations.append(
                            {
                                "exemption_sub_category": get_doc1[0].name,
                                "exemption_category": get_doc1[0].exemption_category,
                                "max_amount": get_doc1[0].max_amount,
                                "amount": value,
                            }
                        )

                self.declarations = []
                for row in declarations:
                    self.append("declarations", row)


        if self.custom_tax_regime == "New Regime":
            if self.custom_status in ["Approved", "Pending"]:
                form_data = json.loads(self.custom_declaration_form_data or "{}")

                numbers = [
                    {"field": "nineNumber", "name": "NPS Deduction U/S 80CCD(2)(Employer NPS deduction)"},
                ]

                sub_category, category, max_amount, declared_amount = [], [], [], []

                for item in numbers:
                    value = form_data.get(item["field"], 0)
                    if value > 0:
                        get_doc1 = frappe.get_list(
                            "Employee Tax Exemption Sub Category",
                            filters={"is_active": 1, "name": item["name"]},
                            fields=["name", "exemption_category", "max_amount"],
                        )

                        if get_doc1:
                            sub_category.append(get_doc1[0].name)
                            category.append(get_doc1[0].exemption_category)
                            max_amount.append(get_doc1[0].max_amount)
                            declared_amount.append(value)

                self.declarations = []
                for i in range(len(sub_category)):
                    self.append(
                        "declarations",
                        {
                            "exemption_sub_category": sub_category[i],
                            "exemption_category": category[i],
                            "max_amount": max_amount[i],
                            "amount": declared_amount[i],
                        },
                    )
