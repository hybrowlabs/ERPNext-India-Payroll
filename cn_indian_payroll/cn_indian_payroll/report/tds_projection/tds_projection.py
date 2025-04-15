import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
import json


def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [1]]}

    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    salary_structure_assignments = frappe.get_all(
        "Salary Structure Assignment",
        filters=conditions,
        fields=["*"],
        order_by="from_date ASC",
    )

    latest_salary_structure = {}
    first_salary_structure = {}

    for structure in salary_structure_assignments:
        employee_id = structure["employee"]

        if (
            employee_id not in latest_salary_structure
            or structure["from_date"]
            > latest_salary_structure[employee_id]["from_date"]
        ):
            latest_salary_structure[employee_id] = structure

        if (
            employee_id not in first_salary_structure
            or structure["from_date"] < first_salary_structure[employee_id]["from_date"]
        ):
            first_salary_structure[employee_id] = structure

    unique_salary_structures = list(latest_salary_structure.values())
    first_unique_salary_structures = list(first_salary_structure.values())

    first_employee_details = [
        {
            "employee": item["employee"],
            "from_date": item["from_date"],
            "salary_structure": item["salary_structure"],
        }
        for item in first_unique_salary_structures
    ]

    salary_components = {}
    final_data = []

    for structure in unique_salary_structures:
        employee = frappe.get_value(
            "Employee",
            structure["employee"],
            ["pan_number", "personal_email", "company_email"],
            as_dict=True,
        )

        structure.update(employee)

        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={"employee": structure["employee"], "docstatus": ["in", [0, 1]]},
            fields=["name"],
        )

        salary_data = structure.copy()
        slip_count = len(salary_slips)
        total_income = 0

        if salary_slips:
            for slip in salary_slips:
                salary_slip_doc = frappe.get_doc("Salary Slip", slip["name"])
                for earning in salary_slip_doc.earnings:
                    get_each_component = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )
                    component_sequence = get_each_component.custom_sequence or 9999

                    if (
                        get_each_component.is_tax_applicable == 1
                        and get_each_component.type == "Earning"
                        and get_each_component.custom_tax_exemption_applicable_based_on_regime
                        == 1
                        and (
                            get_each_component.custom_regime == "All"
                            or get_each_component.custom_regime == "New Regime"
                        )
                    ):
                        salary_component = earning.salary_component
                        salary_components[salary_component] = component_sequence
                        salary_data[salary_component] = (
                            salary_data.get(salary_component, 0) + earning.amount
                        )
                        total_income += earning.amount

        last_employee_detail = next(
            (
                d
                for d in first_employee_details
                if d["employee"] == structure["employee"]
            ),
            None,
        )

        if last_employee_detail:
            payroll_period_doc = frappe.get_doc(
                "Payroll Period", structure["custom_payroll_period"]
            )
            end_date = payroll_period_doc.end_date
            month_count = (
                (end_date.year - last_employee_detail["from_date"].year) * 12
                + (end_date.month - last_employee_detail["from_date"].month)
                + 1
            )

            salary_slip = make_salary_slip(
                source_name=last_employee_detail["salary_structure"],
                employee=structure["employee"],
                print_format="Salary Slip Standard",
                posting_date=last_employee_detail["from_date"],
                for_preview=1,
            )

            for projection_earning in salary_slip.earnings:
                get_tax_component = frappe.get_doc(
                    "Salary Component", projection_earning.salary_component
                )

                if (
                    get_tax_component.is_tax_applicable == 1
                    and get_tax_component.type == "Earning"
                    and get_tax_component.custom_tax_exemption_applicable_based_on_regime
                    == 1
                    and (
                        get_tax_component.custom_regime == "All"
                        or get_tax_component.custom_regime == "New Regime"
                    )
                ):
                    salary_component = projection_earning.salary_component
                    projected_income = projection_earning.amount * (
                        month_count - slip_count
                    )
                    salary_data[salary_component] = (
                        salary_data.get(salary_component, 0) + projected_income
                    )
                    total_income += projected_income

        start_date = frappe.utils.getdate(payroll_period_doc.start_date)

        loan_repayments = frappe.get_list(
            "Loan Repayment Schedule",
            filters={
                "custom_employee": structure["employee"],
                "status": "Active",
                "docstatus": 1,
            },
            fields=["*"],
        )

        loan_perquisite_total = 0
        if loan_repayments:
            for repayment in loan_repayments:
                loan_doc = frappe.get_doc("Loan Repayment Schedule", repayment.name)
                for date in loan_doc.custom_loan_perquisite:
                    payment_date = frappe.utils.getdate(date.payment_date)
                    if start_date <= payment_date <= end_date:
                        loan_perquisite_total += date.perquisite_amount

        salary_data["loan_perquisite"] = loan_perquisite_total
        salary_data["total_income"] = total_income + loan_perquisite_total

        # Fetch Tax Exemption Declaration
        declaration = frappe.get_all(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": structure["employee"],
                "payroll_period": structure["custom_payroll_period"],
                "docstatus": 1,
            },
            fields=["name"],
        )

        if declaration:
            get_doc = frappe.get_doc(
                "Employee Tax Exemption Declaration", declaration[0].name
            )

            if get_doc.custom_tax_regime == "New Regime":
                get_tax_slab = frappe.get_doc(
                    "Income Tax Slab", get_doc.custom_income_tax
                )

                standard_deduction_new = get_tax_slab.standard_tax_exemption_amount or 0

                form_data = json.loads(get_doc.custom_declaration_form_data or "{}")
                nps_deduction = form_data.get("nineNumber", 0)
                total = nps_deduction + standard_deduction_new

                salary_data["standard_deduction_new"] = standard_deduction_new
                salary_data["nps_deduction"] = nps_deduction
                salary_data["total_deduction"] = get_doc.total_exemption_amount

                salary_data["annual_taxable_income"] = max(total_income - total, 0)

            if get_doc.custom_tax_regime == "Old Regime":
                get_tax_slab = frappe.get_doc(
                    "Income Tax Slab", get_doc.custom_income_tax
                )
                standard_deduction_old = get_tax_slab.standard_tax_exemption_amount or 0

                hra_exemption = get_doc.annual_hra_exemption

                form_data = json.loads(get_doc.custom_declaration_form_data or "{}")

                lta_map = form_data.get("twentyeight", 0)
                education_allowance_map = form_data.get("thirteen", 0)
                hostel_allowance_map = form_data.get("twentysix", 0)
                uniform_allowance_map = form_data.get("twentyFour", 0)
                pt_map = form_data.get("nineteenNumber", 0)

                pf_auto_map = form_data.get("pfValue", 0)
                pension_scheme_map = form_data.get("aValue2", 0)
                housing_loan = form_data.get("bValue1", 0)
                ppf = form_data.get("amount4", 0)
                home_loan = form_data.get("dValue1", 0)

                lic = form_data.get("eValue1", 0)
                nsc = form_data.get("fValue1", 0)
                mutual_fund = form_data.get("gValue1", 0)
                elss = form_data.get("hValue1", 0)
                tuition = form_data.get("iValue1", 0)

                fixed_deposit = form_data.get("jValue1", 0)
                deposit = form_data.get("kValue1", 0)
                others = form_data.get("kValue2", 0)

                mediclaim_self = form_data.get("amount", 0)
                mediclaim_self_senior = form_data.get("amount3", 0)
                mediclaim_parents_below = form_data.get("mpAmount3", 0)
                mediclaim_parents_senior = form_data.get("mpAmount4", 0)
                preventive_health_checkup = form_data.get("mp5", 0)
                preventive_health_checkup_self = form_data.get("mpAmount6", 0)

                medical_treatment_insurance = form_data.get("fourValue", 0)
                medical_treatment_disease = form_data.get("fiveNumber", 0)
                interest_repayment = form_data.get("sixNumber", 0)
                physical_disabled = form_data.get("sevenNumber", 0)
                donation_80g = form_data.get("eightNumber", 0)
                nps_deduction = form_data.get("nineNumber", 0)
                hsg = form_data.get("tenNumber", 0)
                nps_contribution = form_data.get("elevenNumber", 0)
                tax_incentive = form_data.get("twelveNumber1", 0)
                tax_incentive_eeb = form_data.get("fifteenNumber", 0)
                dona_political_party = form_data.get("sixteenNumber", 0)
                interest_saving_account = form_data.get("seventeenNumber", 0)
                interest_fd = form_data.get("eighteenNumber", 0)

                deduction_80gg = form_data.get("twentyNumber", 0)
                regime_80ccg = form_data.get("twentyoneNumber", 0)

                total = (
                    regime_80ccg
                    + deduction_80gg
                    + interest_fd
                    + interest_saving_account
                    + nps_deduction
                    + standard_deduction_old
                    + tax_incentive_eeb
                    + tax_incentive
                    + nps_contribution
                    + hsg
                    + donation_80g
                    + physical_disabled
                    + interest_repayment
                    + medical_treatment_disease
                    + medical_treatment_insurance
                    + preventive_health_checkup_self
                    + preventive_health_checkup
                    + mediclaim_parents_senior
                    + mediclaim_parents_below
                    + mediclaim_self_senior
                    + mediclaim_self
                    + deposit
                    + fixed_deposit
                    + tuition
                    + elss
                    + mutual_fund
                    + nsc
                    + lic
                    + home_loan
                    + ppf
                    + housing_loan
                    + pension_scheme_map
                    + pf_auto_map
                    + pt_map
                    + uniform_allowance_map
                    + hostel_allowance_map
                    + education_allowance_map
                    + lta_map
                    + hra_exemption
                )

                salary_data["standard_deduction_old"] = standard_deduction_old
                salary_data["hra_exemption"] = hra_exemption
                salary_data["lta"] = lta_map
                salary_data["education_allowance_exemption"] = education_allowance_map
                salary_data["hostel_allowance_exemption"] = hostel_allowance_map
                salary_data["uniform_allowance_exemption"] = uniform_allowance_map
                salary_data["tax_on_employment"] = pt_map

                salary_data["pf_auto"] = pf_auto_map
                salary_data["pension_scheme"] = pension_scheme_map
                salary_data["housing_loan"] = housing_loan
                salary_data["ppf"] = ppf
                salary_data["home_loan"] = home_loan

                salary_data["lic"] = lic
                salary_data["nsc"] = nsc
                salary_data["mutual_fund"] = mutual_fund
                salary_data["elss"] = elss
                salary_data["tuition"] = tuition
                salary_data["fixed_deposit"] = fixed_deposit
                salary_data["deposit"] = deposit
                salary_data["others"] = others

                salary_data["mediclaim_self"] = mediclaim_self
                salary_data["mediclaim_self_senior"] = mediclaim_self_senior
                salary_data["mediclaim_parents_below"] = mediclaim_parents_below
                salary_data["mediclaim_parents_senior"] = mediclaim_parents_senior
                salary_data["preventive_health_checkup"] = preventive_health_checkup
                salary_data[
                    "preventive_health_checkup_self"
                ] = preventive_health_checkup_self

                salary_data["medical_treatment_insurance"] = medical_treatment_insurance
                salary_data["medical_treatment_disease"] = medical_treatment_disease
                salary_data["interest_repayment"] = interest_repayment
                salary_data["physical_disabled"] = physical_disabled
                salary_data["donation_80g"] = donation_80g

                salary_data["nps_deduction"] = nps_deduction
                salary_data["hsg"] = hsg
                salary_data["nps_contribution"] = nps_contribution
                salary_data["tax_incentive"] = tax_incentive
                salary_data["tax_incentive_eeb"] = tax_incentive_eeb
                salary_data["dona_political_party"] = dona_political_party
                salary_data["interest_saving_account"] = interest_saving_account
                salary_data["interest_fd"] = interest_fd
                salary_data["deduction_80gg"] = deduction_80gg
                salary_data["regime_80ccg"] = regime_80ccg

                salary_data["total_deduction"] = get_doc.total_exemption_amount

                salary_data["annual_taxable_income"] = round(
                    (
                        total_income
                        - standard_deduction_old
                        - get_doc.total_exemption_amount
                    )
                )

        final_data.append(salary_data)

    return final_data, salary_components


def execute(filters=None):
    columns = [
        {
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 120,
        },
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 150},
        {
            "label": "Payroll Period",
            "fieldname": "custom_payroll_period",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Effective From Date",
            "fieldname": "from_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Joining Date",
            "fieldname": "custom_date_of_joining",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Opted Slab",
            "fieldname": "custom_tax_regime",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Designation",
            "fieldname": "designation",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "PAN Number",
            "fieldname": "pan_number",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Personal Email",
            "fieldname": "personal_email",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": "Company Email",
            "fieldname": "company_email",
            "fieldtype": "Data",
            "width": 200,
        },
    ]

    data, salary_components = get_salary_slips(filters)

    # sorted_components = sorted(salary_components.items(), key=lambda x: x[1])
    sorted_components = sorted(
        salary_components.items(),
        key=lambda x: x[1] if isinstance(x[1], (int, float)) else 9999,
    )

    for component, _ in sorted_components:
        columns.append(
            {
                "label": component,
                "fieldname": component,
                "fieldtype": "Currency",
                "width": 120,
            }
        )

    columns.extend(
        [
            {
                "label": "Loan Perquisite",
                "fieldname": "loan_perquisite",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "Total Income",
                "fieldname": "total_income",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "HRA Exemption",
                "fieldname": "hra_exemption",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "fieldname": "lta",
                "label": "LTA  U/s 10 (5)",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "fieldname": "education_allowance_exemption",
                "label": "Education Allowance Exemption",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "hostel_allowance_exemption",
                "label": "Hostel Allowances Exemption",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "uniform_allowance_exemption",
                "label": "Uniform Allowance Exemption",
                "fieldtype": "Currency",
                "width": 120,
            },
            # Standard Deduction Columns
            {
                "fieldname": "standard_deduction_old",
                "label": "Standard Deduction Old Regime",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "standard_deduction_new",
                "label": "Standard Deduction New Regime",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tax_on_employment",
                "label": "Tax on Employment",
                "fieldtype": "Currency",
                "width": 120,
            },
            # 80C Columns
            {
                "label": "Investments In PF(Auto)",
                "fieldname": "pf_auto",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Pension Scheme Investments & ULIP",
                "fieldname": "pension_scheme",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Housing Loan Principal Repayment",
                "fieldname": "housing_loan",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "PPF - Public Provident Fund",
                "fieldname": "ppf",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Home Loan Account Of National Housing Bank",
                "fieldname": "home_loan",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "LIC- Life Insurance Premium Directly Paid By Employee",
                "fieldname": "lic",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "NSC - National Saving Certificate",
                "fieldname": "nsc",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Mutual Funds - Notified Under Clause 23D Of Section 10",
                "fieldname": "mutual_fund",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "ELSS - Equity Link Saving Scheme Of Mutual Funds",
                "fieldname": "elss",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tuition",
                "label": "Tuition Fees For Full Time Education",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "fixed_deposit",
                "label": "Fixed Deposits In Banks (Period As Per Income Tax Guidelines)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "deposit",
                "label": "5 Years Term Deposit An Account Under Post Office Term Deposit Rules",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "others",
                "label": "Others",
                "fieldtype": "Currency",
                "width": 120,
            },
            # 80D Columns
            {
                "fieldname": "mediclaim_self",
                "label": "Mediclaim Self, Spouse & Children (Below 60 years)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "mediclaim_self_senior",
                "label": "Mediclaim Self (Senior Citizen - 60 years & above)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "mediclaim_parents_below",
                "label": "Mediclaim Parents (Below 60 years)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "mediclaim_parents_senior",
                "label": "Mediclaim Parents (Senior Citizen - 60 years & above)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "preventive_health_checkup",
                "label": "Preventive Health Check-up for Parents",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "preventive_health_checkup_self",
                "label": "Preventive Health Check-up",
                "fieldtype": "Currency",
                "width": 120,
            },
            # 80DD and Other Columns
            {
                "fieldname": "medical_treatment_insurance",
                "label": "Medical treatment / insurance of handicapped dependant",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "medical_treatment_disease",
                "label": "Medical treatment (specified diseases only)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "interest_repayment",
                "label": "Interest repayment of Loan for higher education",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "physical_disabled",
                "label": "Deduction for Physically Disabled",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "donation_80g",
                "label": "Donation U/S 80G",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "nps_deduction",
                "label": "NPS Deduction U/S 80CCD(2)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "hsg",
                "label": "First HSG Loan Interest Ded.(80EE)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "nps_contribution",
                "label": "Contribution in National Pension Scheme",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tax_incentive",
                "label": "Tax Incentive for Affordable Housing for Ded U/S 80EEA",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tax_incentive_eeb",
                "label": "Tax Incentives for Electric Vehicles for Ded U/S 80EEB",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "dona_political_party",
                "label": "Donations/contribution made to a political party or an electoral trust",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "interest_saving_account",
                "label": "Interest on deposits in saving account for Ded U/S 80TTA",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "interest_fd",
                "label": "Interest on deposits in saving account for Ded U/S 80TTB",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "deduction_80gg",
                "label": "Deduction U/S 80GG",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "regime_80ccg",
                "label": "Rajiv Gandhi Equity Saving Scheme 80CCG",
                "fieldtype": "Currency",
                "width": 120,
            },
            # Final Columns
            {
                "fieldname": "total_deduction",
                "label": "Total Deduction/Exemptions",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "annual_taxable_income",
                "label": "Annual Taxable Income",
                "fieldtype": "Currency",
                "width": 120,
            },
        ]
    )

    return columns, data
