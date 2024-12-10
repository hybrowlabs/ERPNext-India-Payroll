import frappe

def execute():

    data=[
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 10(14)",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.148302",
            "name": "Uniform Allowance"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 10",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.172722",
            "name": "Driver Salary Allowance"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 10",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.183078",
            "name": "Petrol Allowance"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80EE",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.192868",
            "name": "Interest Paid On Home Loan"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80CCD(1B)",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.202308",
            "name": "Section 80CCD(1B) NPS-Additional Exemption"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80CCD(1B)",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.211250",
            "name": "Section 80CCD(2)-Employer Contribution"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80D",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.220530",
            "name": "Section 80D (Medi-claim for Self Spouse, Children)"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 10",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.231683",
            "name": "Section 80D (Medi Claim for Parents for Senior Citizen)"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 16",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.240702",
            "name": "Profession Tax"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.278985",
            "name": "Life Insurance Premium"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.289123",
            "name": "Public Provident Fund"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.298520",
            "name": "Unit-linked Insurance Plan"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.307700",
            "name": "National Savings Certificates"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.318401",
            "name": "Principal paid on Home Loan"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.330655",
            "name": "ELSS Tax Saving Mutual Fund"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.341466",
            "name": "Children Tuition Fees"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.351638",
            "name": "Sukanya Samriddhi Deposit Scheme"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.361519",
            "name": "5 Year Fixed Deposit in Scheduled Banks"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.372614",
            "name": "Stamp duty & Registration fee on buying house property"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80D",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.383929",
            "name": "Mediclaim Policy for Self, Spouse, Children"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80D",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.396142",
            "name": "Mediclaim Policy for Self, Spouse, Children for Senior Citizen"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80D",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.407845",
            "name": "Mediclaim Policy for Parents"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80D",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.417944",
            "name": "Mediclaim Policy for Parents for Senior Citizen"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80D",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.428933",
            "name": "Preventive Health Check-up"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80D",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.439889",
            "name": "Preventive Health Check-up for Parents"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80CCD(1B)",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.449702",
            "name": "Additional Exemption on Voluntary NPS"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80U",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.461893",
            "name": "Permanent Physical Disability (Self)"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80U",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.472525",
            "name": "Permanent Severe Physical Disability (Self)"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80DD",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.480899",
            "name": "Treatment of Dependent with Disability"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80DD",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.488089",
            "name": "Treatment of Dependent with Severe Disability"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80E",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.500589",
            "name": "Interest paid on Education Loan"
            },
            {
            
            
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 10(13A)",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 18:43:42.520094",
            "name": "House Rent Allowance"
            },
            {
            "custom_component_type": "EPF",
            "custom_salary_component": "Employee Provident Fund",
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80C",
            "is_active": 1,
            "max_amount": 150000.0,
            "modified": "2024-11-13 19:05:39.006843",
            "name": "Employee Provident Fund (Auto)"
            },
            {
            "custom_component_type": "NPS",
            "custom_salary_component": "NPS",
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 80CCD(2)",
            "is_active": 1,
            "max_amount": 0.0,
            "modified": "2024-11-13 19:05:07.329605",
            "name": "NPS Contribution by Employer"
            },
            {
            "custom_component_type": "Professional Tax",
            "custom_salary_component": "Professional Tax (Gujarat)",
            "docstatus": 0,
            "doctype": "Employee Tax Exemption Sub Category",
            "exemption_category": "Section 16",
            "is_active": 1,
            "max_amount": 2400.0,
            "modified": "2024-11-13 19:05:29.256323",
            "name": "Tax on employment (Professional Tax)"
            }
        ]

   
    for i in data:
        insert_record(i)

def insert_record(i):

    if not frappe.db.exists("Employee Tax Exemption Sub Category", i["name"]):
        doc=frappe.new_doc("Employee Tax Exemption Sub Category")
        doc.update(i)
        doc.save()






    