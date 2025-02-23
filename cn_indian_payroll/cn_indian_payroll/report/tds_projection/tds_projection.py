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
        order_by="from_date ASC"
    )

    latest_salary_structure = {}
    first_salary_structure = {}

    for structure in salary_structure_assignments:
        employee_id = structure["employee"]
        
        if employee_id not in latest_salary_structure or structure["from_date"] > latest_salary_structure[employee_id]["from_date"]:
            latest_salary_structure[employee_id] = structure

        if employee_id not in first_salary_structure or structure["from_date"] < first_salary_structure[employee_id]["from_date"]:
            first_salary_structure[employee_id] = structure

    unique_salary_structures = list(latest_salary_structure.values())
    first_unique_salary_structures = list(first_salary_structure.values())

    first_employee_details = [
        {
            "employee": item["employee"],
            "from_date": item["from_date"],
            "salary_structure": item["salary_structure"]
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
            as_dict=True
        )

        structure.update(employee)
        
        salary_slips = frappe.get_all(
            "Salary Slip", 
            filters={"employee": structure["employee"], "docstatus": 1}, 
            fields=["name"]
        )

        salary_data = structure.copy()
        slip_count = len(salary_slips)
        total_income = 0  

        if salary_slips:
            for slip in salary_slips:
                salary_slip_doc = frappe.get_doc("Salary Slip", slip["name"])
                for earning in salary_slip_doc.earnings:
                    get_each_component = frappe.get_doc("Salary Component", earning.salary_component)
                    component_sequence = get_each_component.custom_sequence or 9999  

                    if (
                        get_each_component.is_tax_applicable == 1 
                        and get_each_component.type == "Earning" 
                        and get_each_component.custom_tax_exemption_applicable_based_on_regime == 1 
                        and (get_each_component.custom_regime == "All" or get_each_component.custom_regime == "New Regime")
                    ):
                        salary_component = earning.salary_component
                        salary_components[salary_component] = component_sequence
                        salary_data[salary_component] = salary_data.get(salary_component, 0) + earning.amount
                        total_income += earning.amount  

        last_employee_detail = next((d for d in first_employee_details if d["employee"] == structure["employee"]), None)
        
        if last_employee_detail:
            payroll_period_doc = frappe.get_doc("Payroll Period", structure["custom_payroll_period"])
            end_date = payroll_period_doc.end_date
            month_count = (end_date.year - last_employee_detail["from_date"].year) * 12 + (end_date.month - last_employee_detail["from_date"].month) + 1
            
            salary_slip = make_salary_slip(
                source_name=last_employee_detail["salary_structure"],
                employee=structure["employee"],
                print_format='Salary Slip Standard',
                posting_date=last_employee_detail["from_date"],
                for_preview=1,  
            )

            for projection_earning in salary_slip.earnings:
                get_tax_component = frappe.get_doc("Salary Component", projection_earning.salary_component)
                
                if (
                    get_tax_component.is_tax_applicable == 1 
                    and get_tax_component.type == "Earning" 
                    and get_tax_component.custom_tax_exemption_applicable_based_on_regime == 1 
                    and (get_tax_component.custom_regime == "All" or get_tax_component.custom_regime == "New Regime")
                ):
                    salary_component = projection_earning.salary_component
                    projected_income = projection_earning.amount * (month_count - slip_count)
                    salary_data[salary_component] = salary_data.get(salary_component, 0) + projected_income
                    total_income += projected_income 

        start_date = frappe.utils.getdate(payroll_period_doc.start_date)
        
        loan_repayments = frappe.get_list(
            'Loan Repayment Schedule',
            filters={
                'custom_employee': structure["employee"],
                'status': 'Active',
                'docstatus': 1
            },
            fields=['*']
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
            'Employee Tax Exemption Declaration',
            filters={
                'employee': structure["employee"],
                'payroll_period': structure["custom_payroll_period"],
                'docstatus': 1
            },
            fields=['name']
        )

        if declaration:
            get_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration[0].name)
            
            if get_doc.custom_tax_regime == "New Regime":

                get_tax_slab=frappe.get_doc("Income Tax Slab",get_doc.custom_income_tax)
                

                standard_deduction_new = get_tax_slab.standard_tax_exemption_amount or 0
                
                # Parse custom declaration form data
                form_data = json.loads(get_doc.custom_declaration_form_data or '{}')
                nps_deduction = form_data.get("nineNumber", 0)

                # Add deductions to salary data
                salary_data["standard_deduction_new"] = standard_deduction_new
                salary_data["nps_deduction"] = nps_deduction

        final_data.append(salary_data)
    
    return final_data, salary_components


def execute(filters=None):
    columns = [
        {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Data", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 150},
        {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Data", "width": 150},
        {"label": "Effective From Date", "fieldname": "from_date", "fieldtype": "Date", "width": 120},
        {"label": "Joining Date", "fieldname": "custom_date_of_joining", "fieldtype": "Date", "width": 120},
        {"label": "Opted Slab", "fieldname": "custom_tax_regime", "fieldtype": "Data", "width": 120},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 120},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 120},
        {"label": "PAN Number", "fieldname": "pan_number", "fieldtype": "Data", "width": 150},
        {"label": "Personal Email", "fieldname": "personal_email", "fieldtype": "Data", "width": 200},
        {"label": "Company Email", "fieldname": "company_email", "fieldtype": "Data", "width": 200},
    ]
    
    data, salary_components = get_salary_slips(filters)
    
    sorted_components = sorted(salary_components.items(), key=lambda x: x[1])
    for component, _ in sorted_components:
        columns.append({"label": component, "fieldname": component, "fieldtype": "Currency", "width": 120})

    columns.extend([
    {"label": "Loan Perquisite", "fieldname": "loan_perquisite", "fieldtype": "Currency", "width": 150},
    {"label": "Total Income", "fieldname": "total_income", "fieldtype": "Currency", "width": 150},
    {"label": "HRA Exemption", "fieldname": "hra_exemption", "fieldtype": "Currency", "width": 150},

    {"fieldname": "lta","label": "LTA  U/s 10 (5)", "fieldtype": "Currency", "width": 150},
    {"fieldname": "education_allowance_exemption", "label": "Education Allowance Exemption", "fieldtype": "Currency", "width": 120},
    {"fieldname": "hostel_allowance_exemption", "label": "Hostel Allowances Exemption", "fieldtype": "Currency", "width": 120},
    {"fieldname": "uniform_allowance_exemption", "label": "Uniform Allowance Exemption", "fieldtype": "Currency", "width": 120},

    # Standard Deduction Columns
    {"fieldname": "standard_deduction_old", "label": "Standard Deduction Old Regime", "fieldtype": "Currency", "width": 120},
    {"fieldname": "standard_deduction_new", "label": "Standard Deduction New Regime", "fieldtype": "Currency", "width": 120},
    {"fieldname": "tax_on_employment", "label": "Tax on Employment", "fieldtype": "Currency", "width": 120},

    # 80C Columns
    {"label": "Investments In PF(Auto)", "fieldname": "pf_auto", "fieldtype": "Currency", "width": 120},
    {"label": "Pension Scheme Investments & ULIP", "fieldname": "pension_scheme", "fieldtype": "Currency", "width": 120},
    {"label": "Housing Loan Principal Repayment", "fieldname": "housing_loan", "fieldtype": "Currency", "width": 120},
    {"label": "PPF - Public Provident Fund", "fieldname": "ppf", "fieldtype": "Currency", "width": 120},
    {"label": "Home Loan Account Of National Housing Bank", "fieldname": "home_loan", "fieldtype": "Currency", "width": 120},
    {"label": "LIC- Life Insurance Premium Directly Paid By Employee", "fieldname": "lic", "fieldtype": "Currency", "width": 120},
    {"label": "NSC - National Saving Certificate", "fieldname": "nsc", "fieldtype": "Currency", "width": 120},
    {"label": "Mutual Funds - Notified Under Clause 23D Of Section 10", "fieldname": "mutual_fund", "fieldtype": "Currency", "width": 120},
    {"label": "ELSS - Equity Link Saving Scheme Of Mutual Funds", "fieldname": "elss", "fieldtype": "Currency", "width": 120},
    {"fieldname": "tuition", "label": "Tuition Fees For Full Time Education", "fieldtype": "Currency", "width": 120},
    {"fieldname": "fixed_deposit", "label": "Fixed Deposits In Banks (Period As Per Income Tax Guidelines)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "deposit", "label": "5 Years Term Deposit An Account Under Post Office Term Deposit Rules", "fieldtype": "Currency", "width": 120},
    {"fieldname": "others", "label": "Others", "fieldtype": "Currency", "width": 120},

    # 80D Columns
    {"fieldname": "mediclaim_self", "label": "Mediclaim Self, Spouse & Children (Below 60 years)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "mediclaim_self_senior", "label": "Mediclaim Self (Senior Citizen - 60 years & above)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "mediclaim_parents_below", "label": "Mediclaim Parents (Below 60 years)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "mediclaim_parents_senior", "label": "Mediclaim Parents (Senior Citizen - 60 years & above)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "preventive_health_checkup", "label": "Preventive Health Check-up for Parents", "fieldtype": "Currency", "width": 120},
    {"fieldname": "preventive_health_checkup_self", "label": "Preventive Health Check-up", "fieldtype": "Currency", "width": 120},

    # 80DD and Other Columns
    {"fieldname": "medical_treatment_insurance", "label": "Medical treatment / insurance of handicapped dependant", "fieldtype": "Currency", "width": 120},
    {"fieldname": "medical_treatment_disease", "label": "Medical treatment (specified diseases only)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "interest_repayment", "label": "Interest repayment of Loan for higher education", "fieldtype": "Currency", "width": 120},
    {"fieldname": "physical_disabled", "label": "Deduction for Physically Disabled", "fieldtype": "Currency", "width": 120},
    {"fieldname": "donation_80g", "label": "Donation U/S 80G", "fieldtype": "Currency", "width": 120},
    {"fieldname": "nps_deduction", "label": "NPS Deduction U/S 80CCD(2)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "hsg", "label": "First HSG Loan Interest Ded.(80EE)", "fieldtype": "Currency", "width": 120},
    {"fieldname": "nps_contribution", "label": "Contribution in National Pension Scheme", "fieldtype": "Currency", "width": 120},
    {"fieldname": "tax_incentive", "label": "Tax Incentive for Affordable Housing for Ded U/S 80EEA", "fieldtype": "Currency", "width": 120},
    {"fieldname": "tax_incentive_eeb", "label": "Tax Incentives for Electric Vehicles for Ded U/S 80EEB", "fieldtype": "Currency", "width": 120},
    {"fieldname": "dona_political_party", "label": "Donations/contribution made to a political party or an electoral trust", "fieldtype": "Currency", "width": 120},
    {"fieldname": "interest_saving_account", "label": "Interest on deposits in saving account for Ded U/S 80TTA", "fieldtype": "Currency", "width": 120},
    {"fieldname": "interest_fd", "label": "Interest on deposits in saving account for Ded U/S 80TTB", "fieldtype": "Currency", "width": 120},
    {"fieldname": "deduction_80gg", "label": "Deduction U/S 80GG", "fieldtype": "Currency", "width": 120},
    {"fieldname": "regime_80ccg", "label": "Rajiv Gandhi Equity Saving Scheme 80CCG", "fieldtype": "Currency", "width": 120},

    # Final Columns
    {"fieldname": "total_deduction", "label": "Total Deduction/Exemptions", "fieldtype": "Currency", "width": 120},
    {"fieldname": "annual_taxable_income", "label": "Annual Taxable Income", "fieldtype": "Currency", "width": 120},

])
    
    return columns, data
