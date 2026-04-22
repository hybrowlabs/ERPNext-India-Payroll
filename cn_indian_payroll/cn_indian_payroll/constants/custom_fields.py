"""
All custom fields added by cn_indian_payroll to standard Frappe / ERPNext / HRMS
DocTypes are defined here as plain Python dicts.

Layout convention (mirrors india_compliance):
  CUSTOM_FIELDS = {
      "DocType Name": [ {field_dict}, ... ],
      ("DocType A", "DocType B"): [ {shared_field}, ... ],   # applied to both
  }

Fields are created via `frappe.custom.doctype.custom_field.create_custom_fields`
during `bench install-app` (install.py → setup.py).  They are removed cleanly
during `bench remove-app` (uninstall.py → setup.py).

Only include non-null / non-zero / non-false attributes to keep dicts concise.
"""

# ---------------------------------------------------------------------------
# Helper – month select options (DRY)
# ---------------------------------------------------------------------------
from cn_indian_payroll.cn_indian_payroll.constants import MONTH_NAMES

_MONTH_OPTIONS = "\n".join(MONTH_NAMES)


# ===========================================================================
# Company
# ===========================================================================

COMPANY_FIELDS = [
    {
        "fieldname": "custom_cittdsaddress",
        "label": "CIT(TDS) Address",
        "fieldtype": "Small Text",
        "insert_after": "company_description",
    },
    {
        "fieldname": "custom_company_tan",
        "label": "Company TAN",
        "fieldtype": "Data",
        "insert_after": "date_of_commencement",
    },
    {
        "fieldname": "custom_company_pan",
        "label": "Company PAN",
        "fieldtype": "Data",
        "insert_after": "custom_company_tan",
    },
    {
        "fieldname": "custom_tds_assessment_range",
        "label": "TDS Assessment Range",
        "fieldtype": "Data",
        "insert_after": "custom_company_pan",
    },
    {
        "fieldname": "custom_da_component",
        "label": "DA Component",
        "fieldtype": "Link",
        "options": "Salary Component",
        "insert_after": "hra_component",
    },
    {
        "fieldname": "custom_fiscal_year",
        "label": "Fiscal Year",
        "fieldtype": "Link",
        "options": "Fiscal Year",
        "insert_after": "default_settings",
    },
    {
        "fieldname": "custom_declaration_by_employer",
        "label": "Declaration By Employer",
        "fieldtype": "Section Break",
        "insert_after": "old_parent",
    },
    {
        "fieldname": "custom_declaration",
        "label": "Declaration",
        "fieldtype": "Text",
        "insert_after": "custom_declaration_by_employer",
    },
    {
        "fieldname": "custom_full_name",
        "label": "Full Name",
        "fieldtype": "Data",
        "insert_after": "custom_declaration",
    },
    {
        "fieldname": "custom_designation",
        "label": "Designation",
        "fieldtype": "Data",
        "insert_after": "custom_full_name",
    },
]

# ===========================================================================
# Employee
# ===========================================================================

EMPLOYEE_FIELDS = [
    {
        "fieldname": "custom_uan",
        "label": "UAN Number",
        "fieldtype": "Data",
        "insert_after": "provident_fund_account",
    },
    {
        "fieldname": "custom_esic_number",
        "label": "ESIC Number",
        "fieldtype": "Data",
        "insert_after": "custom_uan",
        "translatable": 1,
    },
]

# ===========================================================================
# Employee Advance
# ===========================================================================

EMPLOYEE_ADVANCE_FIELDS = [
    {
        "fieldname": "custom_advance_type",
        "label": "Advance Type",
        "fieldtype": "Link",
        "options": "Advance Type",
        "insert_after": "column_break_11",
    },
]

# ===========================================================================
# Employee Benefit Claim
# ===========================================================================

EMPLOYEE_BENEFIT_CLAIM_FIELDS = [
    {
        "fieldname": "custom_payroll_period",
        "label": "Payroll Period",
        "fieldtype": "Link",
        "options": "Payroll Period",
        "insert_after": "department",
        "read_only": 1,
    },
]

# ===========================================================================
# Employee Promotion
# ===========================================================================

EMPLOYEE_PROMOTION_FIELDS = [
    {
        "fieldname": "custom_status",
        "label": "Status",
        "fieldtype": "Select",
        "options": "In Planning\nPayroll Configured\nArrears Calculated\nCompleted\nCancelled",
        "insert_after": "company",
        "read_only": 1,
    },
    {
        "fieldname": "custom_additional_salary_date",
        "label": "Additional Salary Date",
        "fieldtype": "Date",
        "insert_after": "custom_status",
    },
    {
        "fieldname": "custom_current_salary_structure_reference",
        "label": "Current Salary Structure Reference",
        "fieldtype": "Link",
        "options": "Salary Structure Assignment",
        "insert_after": "current_ctc",
        "read_only": 1,
    },
    {
        "fieldname": "custom_current_effective_from_date",
        "label": "Current Effective From Date",
        "fieldtype": "Date",
        "insert_after": "custom_current_salary_structure_reference",
        "read_only": 1,
    },
    {
        "fieldname": "custom_current_structure",
        "label": "Current Structure",
        "fieldtype": "Link",
        "options": "Salary Structure",
        "insert_after": "custom_current_effective_from_date",
        "read_only": 1,
    },
    {
        "fieldname": "custom_currency",
        "label": "Currency",
        "fieldtype": "Link",
        "options": "Currency",
        "insert_after": "custom_current_structure",
        "fetch_from": "custom_current_structure.currency",
        "fetch_if_empty": 1,
    },
]

# ===========================================================================
# Employee Tax Exemption Category
# ===========================================================================

EMPLOYEE_TAX_EXEMPTION_CATEGORY_FIELDS = [
    {
        "fieldname": "custom_select_section",
        "label": "Select Section",
        "fieldtype": "Select",
        "options": "\n80 C\n80 D",
        "insert_after": "is_active",
    },
]

# ===========================================================================
# Employee Tax Exemption Declaration
# ===========================================================================

EMPLOYEE_TAX_EXEMPTION_DECLARATION_FIELDS = [
    {
        "fieldname": "custom_posting_date",
        "label": "Posting Date",
        "fieldtype": "Date",
        "insert_after": "company",
        "reqd": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_income_tax",
        "label": "Income Tax",
        "fieldtype": "Link",
        "options": "Income Tax Slab",
        "insert_after": "department",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_salary_structure_assignment",
        "label": "Salary Structure Assignment",
        "fieldtype": "Data",
        "insert_after": "custom_income_tax",
        "hidden": 1,
    },
    {
        "fieldname": "custom_tax_regime",
        "label": "Tax Regime",
        "fieldtype": "Data",
        "insert_after": "custom_salary_structure_assignment",
        "read_only": 1,
        "hidden": 1,
        "allow_on_submit": 1,
        "fetch_from": "custom_income_tax.custom_select_regime",
        "fetch_if_empty": 1,
    },
    {
        "fieldname": "custom_status",
        "label": "Status",
        "fieldtype": "Select",
        "options": "Pending\nApproved",
        "insert_after": "custom_tax_regime",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_section_break_xeu16",
        "fieldtype": "Section Break",
        "insert_after": "section_break_8",
    },
    {
        "fieldname": "custom_basic",
        "label": "Basic as per Salary Structure (Annual)",
        "fieldtype": "Float",
        "insert_after": "salary_structure_hra",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_basic_as_per_salary_structure",
        "label": "Basic as per Salary Structure 10%",
        "fieldtype": "Float",
        "insert_after": "custom_basic",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_check",
        "label": "Check",
        "fieldtype": "Check",
        "insert_after": "custom_basic_as_per_salary_structure",
        "default": "0",
        "hidden": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_address_details",
        "label": "Address Details",
        "fieldtype": "Section Break",
        "insert_after": "monthly_hra_exemption",
    },
    {
        "fieldname": "custom_name",
        "label": "Name",
        "fieldtype": "Data",
        "insert_after": "custom_address_details",
        "depends_on": "monthly_house_rent",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_pan",
        "label": "PAN",
        "fieldtype": "Data",
        "insert_after": "custom_name",
        "depends_on": "monthly_house_rent",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_pkbcf",
        "fieldtype": "Column Break",
        "insert_after": "custom_pan",
    },
    {
        "fieldname": "custom_address_title1",
        "label": "Address Title 1",
        "fieldtype": "Data",
        "insert_after": "custom_column_break_pkbcf",
        "depends_on": "monthly_house_rent",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_address_title2",
        "label": "Address Title 2",
        "fieldtype": "Data",
        "insert_after": "custom_address_title1",
        "depends_on": "monthly_house_rent",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_section_break_pbhti",
        "fieldtype": "Section Break",
        "insert_after": "total_exemption_amount",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_hra_breakup",
        "label": "HRA BreakUp",
        "fieldtype": "Table",
        "options": "HRA Breakup",
        "insert_after": "custom_section_break_pbhti",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_declaration_form_tab",
        "label": "Declaration Form",
        "fieldtype": "Tab Break",
        "insert_after": "custom_hra_breakup",
    },
    {
        "fieldname": "custom_section_break_dulfa",
        "fieldtype": "Section Break",
        "insert_after": "custom_declaration_form_tab",
    },
    {
        "fieldname": "custom_declaration_form",
        "label": "Declaration Form",
        "fieldtype": "HTML",
        "insert_after": "custom_section_break_dulfa",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_declaration_form_data",
        "label": "Declaration Form Data",
        "fieldtype": "JSON",
        "insert_after": "custom_declaration_form",
        "hidden": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_projection",
        "label": "Projection",
        "fieldtype": "Tab Break",
        "insert_after": "custom_declaration_form_data",
    },
    {
        "fieldname": "custom_employee_tax_projection",
        "label": "Employee Tax Projection",
        "fieldtype": "HTML",
        "insert_after": "custom_projection",
    },
    {
        "fieldname": "workflow_state",
        "label": "Workflow State",
        "fieldtype": "Link",
        "options": "Workflow State",
        "hidden": 1,
        "allow_on_submit": 1,
    },
]

# ===========================================================================
# Employee Tax Exemption Proof Submission
# ===========================================================================

EMPLOYEE_TAX_EXEMPTION_PROOF_SUBMISSION_FIELDS = [
    {
        "fieldname": "custom_declaration_id",
        "label": "Declaration ID",
        "fieldtype": "Link",
        "options": "Employee Tax Exemption Declaration",
        "insert_after": "employee_details_tab",
        "hidden": 1,
    },
    {
        "fieldname": "custom_annual_hra_exemption",
        "label": "Annual HRA Exemption",
        "fieldtype": "Float",
        "insert_after": "total_eligible_hra_exemption",
    },
]

# ===========================================================================
# Employee Tax Exemption Sub Category
# ===========================================================================

EMPLOYEE_TAX_EXEMPTION_SUB_CATEGORY_FIELDS = [
    {
        "fieldname": "custom_component_type",
        "label": "Component Type (Exemption Type)",
        "fieldtype": "Select",
        "options": "\nNPS\nProvident Fund\nProfessional Tax",
        "insert_after": "is_active",
        "description": "Select the appropriate component type for tax exemption.",
    },
    {
        "fieldname": "custom_column_break_qgnpy",
        "fieldtype": "Column Break",
        "insert_after": "custom_component_type",
    },
    {
        "fieldname": "custom_sequence",
        "label": "Sequence",
        "fieldtype": "Int",
        "insert_after": "custom_column_break_qgnpy",
        "in_list_view": 1,
        "description": "Controls display order in the Employee Tax Exemption Declaration form.",
    },
    {
        "fieldname": "custom_description",
        "label": "Description",
        "fieldtype": "Small Text",
        "insert_after": "custom_sequence",
        "description": "Shown in the Narration column of the Employee Tax Exemption Declaration form.",
    },
]

# ===========================================================================
# Full and Final Outstanding Statement
# ===========================================================================

FULL_AND_FINAL_OUTSTANDING_STATEMENT_FIELDS = [
    {
        "fieldname": "custom_reference_component",
        "label": "Reference Component",
        "fieldtype": "Link",
        "options": "Salary Component",
        "insert_after": "reference_document",
    },
]

# ===========================================================================
# Income Tax Slab
# ===========================================================================

INCOME_TAX_SLAB_FIELDS = [
    {
        "fieldname": "custom_select_regime",
        "label": "Select Regime",
        "fieldtype": "Select",
        "options": "\nOld Regime\nNew Regime",
        "insert_after": "company",
        "reqd": 1,
    },
    {
        "fieldname": "custom_rebate_under_section_87a",
        "label": "Rebate Under Section 87A",
        "fieldtype": "Section Break",
        "insert_after": "amended_from",
    },
    {
        "fieldname": "custom_taxable_income_is_less_than",
        "label": "Taxable Income Is Less Than",
        "fieldtype": "Float",
        "insert_after": "custom_rebate_under_section_87a",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_maximum_amount",
        "label": "Maximum Amount (Rebate)",
        "fieldtype": "Float",
        "insert_after": "custom_taxable_income_is_less_than",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_tytqa",
        "fieldtype": "Column Break",
        "insert_after": "custom_maximum_amount",
    },
    {
        "fieldname": "custom_marginal_relief_applicable",
        "label": "Marginal Relief Applicable",
        "fieldtype": "Check",
        "insert_after": "custom_column_break_tytqa",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_minmum_value",
        "label": "Minimum Value (Marginal Relief)",
        "fieldtype": "Float",
        "insert_after": "custom_marginal_relief_applicable",
        "depends_on": "custom_marginal_relief_applicable",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_maximun_value",
        "label": "Maximum Value (Marginal Relief)",
        "fieldtype": "Float",
        "insert_after": "custom_minmum_value",
        "depends_on": "custom_marginal_relief_applicable",
        "allow_on_submit": 1,
    },
]

# ===========================================================================
# Income Tax Slab Other Charges (child table)
# ===========================================================================

INCOME_TAX_SLAB_OTHER_CHARGES_FIELDS = [
    {
        "fieldname": "custom_is_education_cess",
        "label": "Is Education Cess",
        "fieldtype": "Check",
        "insert_after": "min_taxable_income",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_is_surcharge",
        "label": "Is Surcharge",
        "fieldtype": "Check",
        "insert_after": "custom_is_education_cess",
        "allow_on_submit": 1,
    },
]

# ===========================================================================
# Leave Encashment
# ===========================================================================

LEAVE_ENCASHMENT_FIELDS = [
    {
        "fieldname": "custom_basic_amount",
        "label": "Basic Amount",
        "fieldtype": "Float",
        "insert_after": "encashment_amount",
        "read_only": 1,
    },
]

# ===========================================================================
# Loan
# ===========================================================================

LOAN_FIELDS = [
    {
        "fieldname": "custom_loan_perquisite_rate_of_interest",
        "label": "Loan Perquisite Rate of Interest",
        "fieldtype": "Float",
        "insert_after": "is_term_loan",
        "depends_on": 'eval:doc.applicant_type=="Employee"',
    },
    {
        "fieldname": "custom_loan_dashboard",
        "label": "",
        "fieldtype": "HTML",
        "insert_after": "amended_from",
    },
]

# ===========================================================================
# Loan Application
# ===========================================================================

LOAN_APPLICATION_FIELDS = [
    {
        "fieldname": "custom_witness_details",
        "label": "Witness Details",
        "fieldtype": "Section Break",
        "insert_after": "amended_from",
    },
    {
        "fieldname": "custom_withness1",
        "label": "Witness 1",
        "fieldtype": "Link",
        "options": "Employee",
        "insert_after": "custom_witness_details",
    },
    {
        "fieldname": "custom_employee_name",
        "label": "Employee Name",
        "fieldtype": "Data",
        "insert_after": "custom_withness1",
        "fetch_from": "custom_withness1.employee_name",
        "fetch_if_empty": 1,
    },
    {
        "fieldname": "custom_column_break_b1e6f",
        "fieldtype": "Column Break",
        "insert_after": "custom_employee_name",
    },
    {
        "fieldname": "custom_withness2",
        "label": "Witness 2",
        "fieldtype": "Link",
        "options": "Employee",
        "insert_after": "custom_column_break_b1e6f",
    },
    {
        "fieldname": "custom_employee_name2",
        "label": "Employee Name",
        "fieldtype": "Data",
        "insert_after": "custom_withness2",
        "fetch_from": "custom_withness2.employee_name",
        "fetch_if_empty": 1,
    },
]

# ===========================================================================
# Loan Product
# ===========================================================================

LOAN_PRODUCT_FIELDS = [
    {
        "fieldname": "custom_loan_perquisite",
        "label": "Loan Perquisite",
        "fieldtype": "Section Break",
        "insert_after": "disabled",
    },
    {
        "fieldname": "custom_loan_perquisite_rate_of_interest",
        "label": "Loan Perquisite Rate of Interest",
        "fieldtype": "Float",
        "insert_after": "custom_loan_perquisite",
    },
    {
        "fieldname": "custom_loan_perquisite_threshold_amount",
        "label": "Loan Perquisite Threshold Amount",
        "fieldtype": "Float",
        "insert_after": "custom_loan_perquisite_rate_of_interest",
    },
]

# ===========================================================================
# Loan Repayment Schedule
# ===========================================================================

LOAN_REPAYMENT_SCHEDULE_FIELDS = [
    {
        "fieldname": "custom_loan_perquisite_rate_of_interest",
        "label": "Loan Perquisite Rate of Interest",
        "fieldtype": "Float",
        "insert_after": "loan_restructure",
        "hidden": 1,
    },
    {
        "fieldname": "custom_loan_perquisite_details",
        "label": "Loan Perquisite Payment Schedule",
        "fieldtype": "Section Break",
        "insert_after": "amended_from",
    },
    {
        "fieldname": "custom_loan_perquisite",
        "label": "Loan Perquisite",
        "fieldtype": "Table",
        "options": "Loan Perquisite Child",
        "insert_after": "custom_loan_perquisite_details",
    },
    {
        "fieldname": "custom_employee",
        "label": "Employee",
        "fieldtype": "Link",
        "options": "Employee",
        "insert_after": "column_break_cplx",
    },
    {
        "fieldname": "custom_employee_name",
        "label": "Employee Name",
        "fieldtype": "Data",
        "insert_after": "custom_employee",
    },
]

# ===========================================================================
# Payroll Correction Child (child table)
# ===========================================================================

PAYROLL_CORRECTION_CHILD_FIELDS = [
    {
        "fieldname": "custom_actual_amount",
        "label": "Actual Amount",
        "fieldtype": "Float",
        "insert_after": "amount",
    },
]

# ===========================================================================
# Payroll Employee Detail (child table)
# ===========================================================================

PAYROLL_EMPLOYEE_DETAIL_FIELDS = [
    {
        "fieldname": "custom_lwp_days",
        "label": "LWP Days",
        "fieldtype": "Float",
        "insert_after": "is_salary_withheld",
    },
]

# ===========================================================================
# Payroll Entry
# ===========================================================================

PAYROLL_ENTRY_FIELDS = [
    {
        "fieldname": "custom_employment_type",
        "label": "Employment Type",
        "fieldtype": "Link",
        "options": "Employment Type",
        "insert_after": "department",
    },
    {
        "fieldname": "workflow_state",
        "label": "Workflow State",
        "fieldtype": "Link",
        "options": "Workflow State",
        "hidden": 1,
        "allow_on_submit": 1,
    },
]

# ===========================================================================
# Repayment Schedule (child table of Loan)
# ===========================================================================

REPAYMENT_SCHEDULE_FIELDS = [
    {
        "fieldname": "custom_deducted",
        "label": "Deducted",
        "fieldtype": "Check",
        "insert_after": "demand_generated",
        "read_only": 1,
        "allow_on_submit": 1,
    },
]

# ===========================================================================
# Salary Component
# ===========================================================================

SALARY_COMPONENT_FIELDS = [
    {
        "fieldname": "custom_component_sub_type",
        "label": "Component Sub Type",
        "fieldtype": "Select",
        "options": "Fixed\nVariable",
        "default": "Fixed",
        "insert_after": "type",
        "reqd": 1,
        "description": (
            "Fixed components are paid every month; Variable components are used "
            "for tax projection in the declaration."
        ),
    },
    {
        "fieldname": "custom_is_part_of_ctc",
        "label": "Is Part of CTC",
        "fieldtype": "Check",
        "insert_after": "disabled",
        "default": "0",
        "description": (
            "When enabled, this component is included in CTC calculations and "
            "visible in the CTC breakup preview."
        ),
    },
    {
        "fieldname": "custom_perquisite",
        "label": "Perquisite",
        "fieldtype": "Check",
        "insert_after": "custom_is_part_of_ctc",
        "default": "0",
        "hidden": 1,
    },
    {
        "fieldname": "custom_tax_exemption_applicable_based_on_regime",
        "label": "Tax Applicable Based on Regime",
        "fieldtype": "Check",
        "insert_after": "custom_perquisite",
        "default": "1",
        "depends_on": 'eval:doc.type=="Earning" && doc.is_tax_applicable',
    },
    {
        "fieldname": "custom_regime",
        "label": "Regime",
        "fieldtype": "Link",
        "options": "Income Tax Regime",
        "insert_after": "custom_tax_exemption_applicable_based_on_regime",
        "depends_on": "custom_tax_exemption_applicable_based_on_regime",
    },
    {
        "fieldname": "custom_component_sequence",
        "label": "Component Sequence",
        "fieldtype": "Int",
        "insert_after": "component_type",
        "description": "Controls component ordering in print formats and reports.",
    },
]

# ===========================================================================
# Salary Detail (child table of Salary Slip)
# ===========================================================================

SALARY_DETAIL_FIELDS = [
    {
        "fieldname": "custom_tax_exemption_applicable_based_on_regime",
        "label": "Tax Exemption Applicable Based on Regime",
        "fieldtype": "Check",
        "insert_after": "deduct_full_tax_on_selected_payroll_date",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_regime",
        "label": "Regime",
        "fieldtype": "Link",
        "options": "Income Tax Regime",
        "insert_after": "custom_tax_exemption_applicable_based_on_regime",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_actual_amount",
        "label": "Actual Amount",
        "fieldtype": "Float",
        "insert_after": "year_to_date",
        "read_only": 1,
        "description": "CTC-based actual value for this component.",
    },
    {
        "fieldname": "custom_arrear_ytd",
        "label": "Total Arrear YTD",
        "fieldtype": "Float",
        "insert_after": "custom_actual_amount",
        "read_only": 1,
        "description": "Sum of arrear component values from all previous salary slips.",
    },
    {
        "fieldname": "custom_total_ytd",
        "label": "Food Coupon Total YTD",
        "fieldtype": "Float",
        "insert_after": "custom_arrear_ytd",
        "read_only": 1,
        "description": "Sum of New Regime component values from all previous salary slips.",
    },
]

# ===========================================================================
# Salary Slip
# ===========================================================================

SALARY_SLIP_FIELDS = [
    # --- Identification / linking ---
    {
        "fieldname": "custom_salary_structure_assignment",
        "label": "Salary Structure Assignment",
        "fieldtype": "Link",
        "options": "Salary Structure Assignment",
        "insert_after": "letter_head",
        "read_only": 1,
    },
    {
        "fieldname": "custom_income_tax_slab",
        "label": "Income Tax Slab",
        "fieldtype": "Link",
        "options": "Income Tax Slab",
        "insert_after": "custom_salary_structure_assignment",
        "read_only": 1,
    },
    {
        "fieldname": "custom_tax_regime",
        "label": "Tax Regime",
        "fieldtype": "Data",
        "insert_after": "custom_income_tax_slab",
        "read_only": 1,
        "hidden": 1,
    },
    {
        "fieldname": "custom_payroll_period",
        "label": "Payroll Period",
        "fieldtype": "Link",
        "options": "Payroll Period",
        "insert_after": "custom_tax_regime",
        "read_only": 1,
    },
    # --- Attendance / LOP ---
    {
        "fieldname": "custom_month",
        "label": "Month",
        "fieldtype": "Select",
        "options": _MONTH_OPTIONS,
        "insert_after": "payroll_frequency",
        "read_only": 1,
        "in_list_view": 1,
    },
    {
        "fieldname": "custom_month_count",
        "label": "Month Count",
        "fieldtype": "Float",
        "insert_after": "exchange_rate",
        "hidden": 1,
    },
    {
        "fieldname": "custom_update_arrear",
        "label": "Update Arrear",
        "fieldtype": "Check",
        "insert_after": "custom_month_count",
        "hidden": 1,
    },
    {
        "fieldname": "custom_f_and_f_updated",
        "label": "F&F Updated",
        "fieldtype": "Check",
        "insert_after": "custom_update_arrear",
        "hidden": 1,
    },
    {
        "fieldname": "custom_total_leave_without_pay",
        "label": "Total Leave Without Pay (Absent + LWP)",
        "fieldtype": "Float",
        "insert_after": "leave_without_pay",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_lop_reversal_days",
        "label": "LOP Reversal Days",
        "fieldtype": "Float",
        "insert_after": "payment_days",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_working_days_exclude_holiday",
        "label": "Working Days (Exclude Holidays)",
        "fieldtype": "Float",
        "insert_after": "custom_lop_reversal_days",
        "read_only": 1,
        "hidden": 1,
    },
    # --- Statutory / totals ---
    {
        "fieldname": "custom_statutory_grosspay",
        "label": "Statutory Gross Pay",
        "fieldtype": "Float",
        "insert_after": "base_gross_year_to_date",
        "read_only": 1,
        "hidden": 1,
    },
    {
        "fieldname": "custom_statutory_year_to_date",
        "label": "Statutory Gross Pay YTD",
        "fieldtype": "Float",
        "insert_after": "custom_statutory_grosspay",
        "read_only": 1,
        "hidden": 1,
    },
    {
        "fieldname": "custom_perquisite_amount",
        "label": "Perquisite Amount",
        "fieldtype": "Float",
        "insert_after": "custom_statutory_year_to_date",
        "read_only": 1,
    },
    {
        "fieldname": "custom_total_deduction_amount",
        "label": "Total Deduction Amount",
        "fieldtype": "Float",
        "insert_after": "base_total_deduction",
        "read_only": 1,
    },
    {
        "fieldname": "custom_loan_amount",
        "label": "Loan Amount",
        "fieldtype": "Float",
        "insert_after": "total_loan_repayment",
    },
    {
        "fieldname": "custom_total_income",
        "label": "Total Income",
        "fieldtype": "Float",
        "insert_after": "base_rounded_total",
        "read_only": 1,
        "hidden": 1,
    },
    {
        "fieldname": "custom_net_pay_amount",
        "label": "Net Pay Amount",
        "fieldtype": "Float",
        "insert_after": "custom_total_income",
        "read_only": 1,
        "hidden": 1,
    },
    {
        "fieldname": "custom_in_words",
        "label": "In Words",
        "fieldtype": "Data",
        "insert_after": "total_in_words",
        "read_only": 1,
        "hidden": 1,
    },
    # --- Tax calculation breakup ---
    {
        "fieldname": "custom_section_break_0mzyc",
        "fieldtype": "Section Break",
        "insert_after": "income_tax_calculation_breakup_section",
    },
    {
        "fieldname": "custom_previous_taxable_earnings",
        "label": "Previous Taxable Earnings",
        "fieldtype": "Float",
        "insert_after": "custom_section_break_0mzyc",
        "read_only": 1,
    },
    {
        "fieldname": "custom_current_taxable_earnings",
        "label": "Current Taxable Earnings",
        "fieldtype": "Float",
        "insert_after": "custom_previous_taxable_earnings",
        "read_only": 1,
    },
    {
        "fieldname": "custom_ctc_taxable_earnings",
        "label": "CTC Taxable Earnings",
        "fieldtype": "Float",
        "insert_after": "custom_current_taxable_earnings",
        "read_only": 1,
    },
    {
        "fieldname": "custom_future_taxable_earnings",
        "label": "Future Taxable Earnings",
        "fieldtype": "Float",
        "insert_after": "custom_ctc_taxable_earnings",
        "read_only": 1,
    },
    {
        "fieldname": "custom_annual_taxable_earnings",
        "label": "Annual Taxable Earnings (CTC - Non Taxable Earnings)",
        "fieldtype": "Float",
        "insert_after": "ctc",
        "read_only": 1,
    },
    {
        "fieldname": "custom_additional_tds_deducted_amount",
        "label": "Additional TDS Deducted Amount",
        "fieldtype": "Float",
        "insert_after": "total_income_tax",
    },
    {
        "fieldname": "custom_section_break_h82fs",
        "fieldtype": "Section Break",
        "insert_after": "custom_additional_tds_deducted_amount",
    },
    {
        "fieldname": "custom_tax_slab",
        "label": "Tax Slab",
        "fieldtype": "Table",
        "options": "Tax Slab",
        "insert_after": "custom_section_break_h82fs",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_section_break_jrfeg",
        "fieldtype": "Section Break",
        "insert_after": "custom_tax_slab",
    },
    {
        "fieldname": "custom_total_income_with_taxable_component",
        "label": "Total Income with Taxable Component",
        "fieldtype": "Float",
        "insert_after": "custom_section_break_jrfeg",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_total_tax_exemption_declaration",
        "label": "Total Tax Exemption Declaration",
        "fieldtype": "Float",
        "insert_after": "custom_total_income_with_taxable_component",
        "read_only": 1,
        "hidden": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_taxable_amount",
        "label": "Taxable Amount",
        "fieldtype": "Float",
        "insert_after": "custom_total_tax_exemption_declaration",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_tax_on_total_income",
        "label": "Tax on Total Income",
        "fieldtype": "Float",
        "insert_after": "custom_taxable_amount",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_uhrea",
        "fieldtype": "Column Break",
        "insert_after": "custom_tax_on_total_income",
    },
    {
        "fieldname": "custom_rebate_under_section_87a",
        "label": "Rebate Under Section 87A",
        "fieldtype": "Float",
        "insert_after": "custom_column_break_uhrea",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_total_amount",
        "label": "Total Amount",
        "fieldtype": "Float",
        "insert_after": "custom_rebate_under_section_87a",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_surcharge",
        "label": "Surcharge",
        "fieldtype": "Float",
        "insert_after": "custom_total_amount",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_education_cess",
        "label": "Education Cess",
        "fieldtype": "Float",
        "insert_after": "custom_surcharge",
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_total_tax_on_income",
        "label": "Total Tax on Income",
        "fieldtype": "Float",
        "insert_after": "custom_education_cess",
        "read_only": 1,
        "allow_on_submit": 1,
    },
]

# ===========================================================================
# Salary Structure Assignment
# ===========================================================================

SALARY_STRUCTURE_ASSIGNMENT_FIELDS = [
    {
        "fieldname": "custom_date_of_joining",
        "label": "Date of Joining",
        "fieldtype": "Date",
        "insert_after": "currency",
        "read_only": 1,
        "allow_on_submit": 1,
        "fetch_from": "employee.date_of_joining",
        "fetch_if_empty": 1,
    },
    {
        "fieldname": "custom_tax_regime",
        "label": "Tax Regime",
        "fieldtype": "Data",
        "insert_after": "income_tax_slab",
        "read_only": 1,
        "hidden": 1,
        "allow_on_submit": 1,
        "fetch_from": "income_tax_slab.custom_select_regime",
        "fetch_if_empty": 1,
    },
    {
        "fieldname": "custom_payroll_period",
        "label": "Payroll Period",
        "fieldtype": "Link",
        "options": "Payroll Period",
        "insert_after": "custom_tax_regime",
        "reqd": 1,
        "allow_on_submit": 1,
    },
    # --- Allowances section ---
    {
        "fieldname": "custom_allowance",
        "label": "Allowance",
        "fieldtype": "Section Break",
        "insert_after": "payroll_cost_centers",
    },
    {
        "fieldname": "custom_column_break_nhjhd",
        "fieldtype": "Column Break",
        "insert_after": "custom_allowance",
    },
    {
        "fieldname": "custom_is_uniform_allowance",
        "label": "Uniform Allowance",
        "fieldtype": "Check",
        "insert_after": "custom_column_break_nhjhd",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_uniform_allowance_value",
        "label": "Uniform Allowance Value (Annual)",
        "fieldtype": "Float",
        "insert_after": "custom_is_uniform_allowance",
        "depends_on": "custom_is_uniform_allowance",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_kgcsp",
        "fieldtype": "Column Break",
        "insert_after": "custom_uniform_allowance_value",
    },
    {
        "fieldname": "custom_is_medical_allowance",
        "label": "Medical Allowance",
        "fieldtype": "Check",
        "insert_after": "custom_column_break_kgcsp",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_medical_allowance_value",
        "label": "Medical Allowance Value (Annual)",
        "fieldtype": "Float",
        "insert_after": "custom_is_medical_allowance",
        "depends_on": "custom_is_medical_allowance",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_st8kt",
        "fieldtype": "Column Break",
        "insert_after": "custom_medical_allowance_value",
    },
    {
        "fieldname": "custom_is_food_coupon",
        "label": "Food Coupon",
        "fieldtype": "Check",
        "insert_after": "custom_column_break_st8kt",
        "allow_on_submit": 1,
    },
    # --- EPF section ---
    {
        "fieldname": "custom_epf",
        "label": "Employees' Provident Fund (EPF)",
        "fieldtype": "Section Break",
        "insert_after": "custom_is_food_coupon",
    },
    {
        "fieldname": "custom_is_epf",
        "label": "EPF",
        "fieldtype": "Check",
        "insert_after": "custom_epf",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_is_eps",
        "label": "EPS",
        "fieldtype": "Check",
        "insert_after": "custom_is_epf",
        "depends_on": "custom_is_epf",
        "allow_on_submit": 1,
        "description": (
            "Employees' Pension Scheme eligibility. Typically applicable when "
            "Basic Wages ≤ ₹15,000 or date of joining ≤ 01-Sep-2014."
        ),
    },
    {
        "fieldname": "custom_column_break_pwobk",
        "fieldtype": "Column Break",
        "insert_after": "custom_is_eps",
    },
    {
        "fieldname": "custom_epf_category",
        "label": "EPF Category",
        "fieldtype": "Select",
        "options": "EPF Actual\nEPF Restricted",
        "default": "EPF Actual",
        "insert_after": "custom_column_break_pwobk",
        "depends_on": "custom_is_epf",
        "description": (
            "EPF Actual: contribution on full Basic. EPF Restricted: contribution capped at ₹1,800/month."
        ),
    },
    {
        "fieldname": "custom_column_break_o4xge",
        "fieldtype": "Column Break",
        "insert_after": "custom_epf_category",
    },
    {
        "fieldname": "custom_pf_account_number",
        "label": "PF Account Number",
        "fieldtype": "Data",
        "insert_after": "custom_column_break_o4xge",
        "depends_on": "custom_is_epf",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_h9jia",
        "fieldtype": "Column Break",
        "insert_after": "custom_pf_account_number",
    },
    {
        "fieldname": "custom_uan",
        "label": "UAN",
        "fieldtype": "Data",
        "insert_after": "custom_column_break_h9jia",
        "depends_on": "custom_is_epf",
        "allow_on_submit": 1,
    },
    # --- NPS section ---
    {
        "fieldname": "custom_nps",
        "label": "National Pension System (NPS)",
        "fieldtype": "Section Break",
        "insert_after": "custom_epf_category",
    },
    {
        "fieldname": "custom_is_nps",
        "label": "NPS",
        "fieldtype": "Check",
        "insert_after": "custom_nps",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_mkp51",
        "fieldtype": "Column Break",
        "insert_after": "custom_is_nps",
    },
    {
        "fieldname": "custom_nps_percentage",
        "label": "NPS Percentage",
        "fieldtype": "Percent",
        "insert_after": "custom_column_break_mkp51",
        "depends_on": "custom_is_nps",
        "description": "Applicable NPS contribution percentage.",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_lcztq",
        "fieldtype": "Column Break",
        "insert_after": "custom_nps_percentage",
    },
    {
        "fieldname": "custom_nps_amount",
        "label": "NPS Amount",
        "fieldtype": "Float",
        "insert_after": "custom_column_break_lcztq",
        "depends_on": "custom_is_nps",
        "allow_on_submit": 1,
    },
    # --- LWF section ---
    {
        "fieldname": "custom_lwf_labour_welfare_fund_",
        "label": "Labour Welfare Fund (LWF)",
        "fieldtype": "Section Break",
        "insert_after": "custom_nps_amount",
    },
    {
        "fieldname": "custom_lwf",
        "label": "LWF",
        "fieldtype": "Check",
        "insert_after": "custom_lwf_labour_welfare_fund_",
        "default": "0",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_iekbu",
        "fieldtype": "Column Break",
        "insert_after": "custom_lwf",
    },
    {
        "fieldname": "custom_lwf_state",
        "label": "LWF State",
        "fieldtype": "Link",
        "options": "India Payroll State",
        "insert_after": "custom_column_break_iekbu",
        "depends_on": "custom_lwf",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_cpoqt",
        "fieldtype": "Column Break",
        "insert_after": "custom_lwf_state",
    },
    {
        "fieldname": "custom_frequency",
        "label": "Frequency",
        "fieldtype": "Link",
        "options": "Frequency",
        "insert_after": "custom_column_break_cpoqt",
        "depends_on": "custom_lwf_state",
        "allow_on_submit": 1,
    },
    # --- Professional Tax section ---
    {
        "fieldname": "custom_section_break_qbdc8",
        "label": "Professional Tax (PT)",
        "fieldtype": "Section Break",
        "insert_after": "custom_frequency",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_state",
        "label": "State",
        "fieldtype": "Link",
        "options": "India Payroll State",
        "insert_after": "custom_section_break_qbdc8",
        "description": "Professional tax is calculated according to the selected state.",
        "allow_on_submit": 1,
    },
    # --- Perquisite section ---
    {
        "fieldname": "custom_perquisite",
        "label": "Perquisite",
        "fieldtype": "Section Break",
        "insert_after": "custom_state",
    },
    {
        "fieldname": "custom__car_perquisite",
        "label": "Car Perquisite",
        "fieldtype": "Check",
        "insert_after": "custom_perquisite",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_cubic_capacity_of_company",
        "label": "Cubic Capacity of Company Car",
        "fieldtype": "Select",
        "options": "Car > 1600 CC\nCar < 1600 CC",
        "insert_after": "custom__car_perquisite",
        "depends_on": "custom__car_perquisite",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_car_perquisite_as_per_rules",
        "label": "Car Perquisite as per Rules (Monthly)",
        "fieldtype": "Float",
        "insert_after": "custom_cubic_capacity_of_company",
        "depends_on": "custom__car_perquisite",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_3ufoi",
        "fieldtype": "Column Break",
        "insert_after": "custom_car_perquisite_as_per_rules",
    },
    {
        "fieldname": "custom_driver_provided_by_company",
        "label": "Driver Provided by Company",
        "fieldtype": "Check",
        "insert_after": "custom_column_break_3ufoi",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_driver_perquisite_as_per_rules",
        "label": "Driver Perquisite as per Rules (Monthly)",
        "fieldtype": "Float",
        "insert_after": "custom_driver_provided_by_company",
        "depends_on": "custom_driver_provided_by_company",
        "allow_on_submit": 1,
    },
    # --- Minimum wages ---
    {
        "fieldname": "custom_minimum_wages",
        "label": "Minimum Wages",
        "fieldtype": "Section Break",
        "insert_after": "payroll_cost_centers",
    },
    {
        "fieldname": "custom_minimum_wages_applicable",
        "label": "Minimum Wages Applicable",
        "fieldtype": "Check",
        "insert_after": "custom_minimum_wages",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_povjt",
        "fieldtype": "Column Break",
        "insert_after": "custom_minimum_wages_applicable",
    },
    {
        "fieldname": "custom_minimum_wages_state",
        "label": "Minimum Wages State",
        "fieldtype": "Link",
        "options": "India Payroll State",
        "insert_after": "custom_column_break_povjt",
        "depends_on": "custom_minimum_wages_applicable",
        "allow_on_submit": 1,
    },
    # --- ESIC section ---
    {
        "fieldname": "custom_esic",
        "label": "Employees' State Insurance (ESIC)",
        "fieldtype": "Section Break",
        "insert_after": "custom_minimum_wages_state",
    },
    {
        "fieldname": "custom_is_esic",
        "label": "ESIC",
        "fieldtype": "Check",
        "insert_after": "custom_esic",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_jsryi",
        "fieldtype": "Column Break",
        "insert_after": "custom_is_esic",
    },
    {
        "fieldname": "custom_esic_applicable_period",
        "label": "ESIC Applicable Period",
        "fieldtype": "Data",
        "insert_after": "custom_column_break_jsryi",
        "depends_on": "custom_is_esic",
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_column_break_aqmss",
        "fieldtype": "Column Break",
        "insert_after": "custom_esic_applicable_period",
    },
    {
        "fieldname": "custom_esic_number",
        "label": "ESIC Number",
        "fieldtype": "Data",
        "insert_after": "custom_column_break_aqmss",
        "depends_on": "custom_is_esic",
        "allow_on_submit": 1,
    },
]

# ===========================================================================
# Additional Salary
# ===========================================================================

ADDITIONAL_SALARY_FIELDS = [
    {
        "fieldname": "custom_payroll_entry",
        "label": "Payroll Entry",
        "fieldtype": "Link",
        "options": "Payroll Entry",
        "insert_after": "department",
        "hidden": 1,
    },
    {
        "fieldname": "custom_lop_reversal",
        "label": "LOP Reversal",
        "fieldtype": "Data",
        "insert_after": "custom_payroll_entry",
        "hidden": 1,
    },
    {
        "fieldname": "custom_lop_reversal_days",
        "label": "LOP Reversal Days",
        "fieldtype": "Float",
        "insert_after": "custom_lop_reversal",
        "hidden": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_salary_appraisal_calculation",
        "label": "Salary Appraisal Calculation",
        "fieldtype": "Data",
        "insert_after": "custom_lop_reversal_days",
        "hidden": 1,
        "allow_on_submit": 1,
    },
    {
        "fieldname": "custom_employee_promotion_id",
        "label": "Employee Promotion ID",
        "fieldtype": "Data",
        "insert_after": "custom_salary_appraisal_calculation",
        "hidden": 1,
    },
]

# ===========================================================================
# Master dict — consumed by setup.py / install.py
# ===========================================================================

CUSTOM_FIELDS: dict = {
    "Additional Salary": ADDITIONAL_SALARY_FIELDS,
    "Company": COMPANY_FIELDS,
    "Employee": EMPLOYEE_FIELDS,
    "Employee Advance": EMPLOYEE_ADVANCE_FIELDS,
    "Employee Benefit Claim": EMPLOYEE_BENEFIT_CLAIM_FIELDS,
    "Employee Promotion": EMPLOYEE_PROMOTION_FIELDS,
    "Employee Tax Exemption Category": EMPLOYEE_TAX_EXEMPTION_CATEGORY_FIELDS,
    "Employee Tax Exemption Declaration": EMPLOYEE_TAX_EXEMPTION_DECLARATION_FIELDS,
    "Employee Tax Exemption Proof Submission": EMPLOYEE_TAX_EXEMPTION_PROOF_SUBMISSION_FIELDS,
    "Employee Tax Exemption Sub Category": EMPLOYEE_TAX_EXEMPTION_SUB_CATEGORY_FIELDS,
    "Full and Final Outstanding Statement": FULL_AND_FINAL_OUTSTANDING_STATEMENT_FIELDS,
    "Income Tax Slab": INCOME_TAX_SLAB_FIELDS,
    "Income Tax Slab Other Charges": INCOME_TAX_SLAB_OTHER_CHARGES_FIELDS,
    "Leave Encashment": LEAVE_ENCASHMENT_FIELDS,
    "Loan": LOAN_FIELDS,
    "Loan Application": LOAN_APPLICATION_FIELDS,
    "Loan Product": LOAN_PRODUCT_FIELDS,
    "Loan Repayment Schedule": LOAN_REPAYMENT_SCHEDULE_FIELDS,
    "Payroll Correction Child": PAYROLL_CORRECTION_CHILD_FIELDS,
    "Payroll Employee Detail": PAYROLL_EMPLOYEE_DETAIL_FIELDS,
    "Payroll Entry": PAYROLL_ENTRY_FIELDS,
    "Repayment Schedule": REPAYMENT_SCHEDULE_FIELDS,
    "Salary Component": SALARY_COMPONENT_FIELDS,
    "Salary Detail": SALARY_DETAIL_FIELDS,
    "Salary Slip": SALARY_SLIP_FIELDS,
    "Salary Structure Assignment": SALARY_STRUCTURE_ASSIGNMENT_FIELDS,
}
