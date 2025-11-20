import frappe

def execute():


    data=[

        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "30 if (getdate(start_date).month == 12 and custom_state == \"Andhra Pradesh\" and custom_lwf and custom_frequency==\"Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-24 18:28:12.643771",
        "name": "LWF Employee (Andhra Pradesh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Andhra Pradesh)",
        "salary_component_abbr": "LWF AEE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "0.75 if (getdate(start_date).month == 6 and custom_state == \"Delhi\" and custom_lwf and custom_frequency==\"Half-Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-24 18:27:11.572188",
        "name": "LWF Employee (Delhi)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Delhi)",
        "salary_component_abbr": "LWF DEE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "70 if (getdate(start_date).month == 12 and custom_state == \"Andhra Pradesh\" and custom_lwf and custom_frequency==\"Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.804103",
        "name": "LWF Employer (Andhra Pradesh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Andhra Pradesh)",
        "salary_component_abbr": "LWF ARE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "2.25 if (getdate(start_date).month == 6 and custom_state == \"Delhi\" and custom_lwf and custom_frequency==\"Half-Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.795193",
        "name": "LWF Employer (Delhi)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Delhi)",
        "salary_component_abbr": "LWF DER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "12 if (getdate(start_date).month == 6 and custom_state == \"Gujarat\" and custom_lwf and custom_frequency==\"Half-Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.783830",
        "name": "LWF Employer (Gujarat)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Gujarat)",
        "salary_component_abbr": "LWF GER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "6 if (getdate(start_date).month == 6 and custom_state == \"Gujarat\" and custom_lwf and custom_frequency==\"Half-Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-24 18:26:14.323499",
        "name": "LWF Employee (Gujarat)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Gujarat)",
        "salary_component_abbr": "LWF GEE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "20 if (custom_lwf and custom_lwf_state == \"Chandigarh\" and custom_frequency==\"Monthly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.759117",
        "name": "LWF Employer (Chandigarh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Chandigarh)",
        "salary_component_abbr": "LWF C",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "5 if (custom_lwf and custom_lwf_state == \"Chandigarh\" and custom_frequency==\"Monthly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-24 19:11:58.445505",
        "name": "LWF Employee (Chandigarh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Chandigarh)",
        "salary_component_abbr": "LWF CE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "15 if (custom_lwf and getdate(start_date).month == 6 and custom_lwf_state == \"Chattisgarh\" and custom_frequency==\"Half-Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-24 19:18:37.500634",
        "name": "LWF Employee (Chattisgarh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Chattisgarh)",
        "salary_component_abbr": "LWF CC",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "45 if (getdate(start_date).month == 6 and custom_lwf and custom_lwf_state == \"Chattisgarh\" and custom_frequency==\"Half-Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.747630",
        "name": "LWF Employer (Chattisgarh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Chattisgarh)",
        "salary_component_abbr": "LWF CR",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "40 if (getdate(start_date).month == 12 and custom_state == \"Karnataka\" and custom_lwf and custom_frequency==\"Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.735111",
        "name": "LWF Employer (Karnataka)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Karnataka)",
        "salary_component_abbr": "LWF KAE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "20 if (getdate(start_date).month == 12 and custom_state == \"Karnataka\" and custom_lwf and custom_frequency==\"Yearly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-24 19:19:41.088606",
        "name": "LWF Employee (Karnataka)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Karnataka)",
        "salary_component_abbr": "LWF KAEE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "50 if (custom_lwf and custom_lwf_state == \"Kerala\" and custom_frequency==\"Monthly\") else \n8 if (custom_lwf and custom_lwf_state == \"Kerala\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6 ) else \n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.724438",
        "name": "LWF Employer (Kerala)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Kerala)",
        "salary_component_abbr": "LWF KEE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "50 if (custom_lwf and custom_lwf_state == \"Kerala\" and custom_frequency==\"Monthly\") else\n4 if (custom_lwf and custom_lwf_state == \"Kerala\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:31:57.889879",
        "name": "LWF Employee (Kerala)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Kerala)",
        "salary_component_abbr": "LWF KER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "10 if (custom_lwf and custom_lwf_state == \"Madhya Pradesh\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:33:33.442544",
        "name": "LWF Employee (Madhya Pradesh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Madhya Pradesh)",
        "salary_component_abbr": "LWF ME",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "30 if (custom_lwf and custom_lwf_state == \"Madhya Pradesh\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.713575",
        "name": "LWF Employer (Madhya Pradesh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Madhya Pradesh)",
        "salary_component_abbr": "LWF MER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "18 if (custom_lwf and custom_lwf_state == \"Maharashtra\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6 and gross_pay<=3000) else\n36 if (custom_lwf and custom_lwf_state == \"Maharashtra\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6 and gross_pay>3000) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.701800",
        "name": "LWF Employer (Maharashtra)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Maharashtra)",
        "salary_component_abbr": "LWF MHE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "6 if (custom_lwf and custom_lwf_state == \"Maharashtra\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6 and gross_pay<=3000) else\n12 if (custom_lwf and custom_lwf_state == \"Maharashtra\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6 and gross_pay>3000) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:36:44.569242",
        "name": "LWF Employee (Maharashtra)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Maharashtra)",
        "salary_component_abbr": "LWF MHEE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "10 if (custom_lwf and custom_lwf_state == \"Odisha\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:40:32.406518",
        "name": "LWF Employee (Odisha)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Odisha)",
        "salary_component_abbr": "LWF OE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "20 if (custom_lwf and custom_lwf_state == \"Odisha\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.691092",
        "name": "LWF Employer (Odisha)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Odisha)",
        "salary_component_abbr": "LWF OER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "20 if (custom_lwf and custom_lwf_state == \"Punjab\" and custom_frequency==\"Monthly\") else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.682225",
        "name": "LWF Employer (Punjab)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Punjab)",
        "salary_component_abbr": "LWF PE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "5 if (custom_lwf and custom_lwf_state == \"Punjab\" and custom_frequency==\"Monthly\") else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:40:09.867684",
        "name": "LWF Employee (Punjab)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Punjab)",
        "salary_component_abbr": "LWF PER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "20 if (custom_lwf and custom_lwf_state == \"Tamil Nadu\" and custom_frequency==\"Yearly\") else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:41:48.621640",
        "name": "LWF Employee (Tamil Nadu)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Tamil Nadu)",
        "salary_component_abbr": "LWF TNE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "40 if (custom_lwf and custom_lwf_state == \"Tamil Nadu\" and custom_frequency==\"Yearly\") else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.669551",
        "name": "LWF Employer (Tamil Nadu)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Tamil Nadu)",
        "salary_component_abbr": "LWF TNER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "5 if (custom_lwf and custom_lwf_state == \"Telangana\" and custom_frequency==\"Yearly\") else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.656586",
        "name": "LWF Employer (Telangana)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Telangana)",
        "salary_component_abbr": "LWF TER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "2 if (custom_lwf and custom_lwf_state == \"Telangana\" and custom_frequency==\"Yearly\") else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:43:26.699376",
        "name": "LWF Employee (Telangana)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Telangana)",
        "salary_component_abbr": "LWF TERG",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "3 if (custom_lwf and custom_lwf_state == \"West Bengal\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:44:42.595610",
        "name": "LWF Employee (West Bengal)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (West Bengal)",
        "salary_component_abbr": "LWF WE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "15 if (custom_lwf and custom_lwf_state == \"West Bengal\" and custom_frequency==\"Half-Yearly\" and getdate(start_date).month == 6) else\n0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.624214",
        "name": "LWF Employer (West Bengal)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (West Bengal)",
        "salary_component_abbr": "LWF WER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "31 if (custom_lwf and custom_lwf_state == \"Haryana\" and custom_frequency==\"Monthly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-24 18:24:48.448244",
        "name": "LWF Employee (Haryana)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employee (Haryana)",
        "salary_component_abbr": "LWF HE",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 1,

        "disabled": 0,
        "do_not_include_in_total": 1,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "62 if (custom_lwf and custom_lwf_state == \"Haryana\" and custom_frequency==\"Monthly\") else 0\n",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-25 07:46:35.771520",
        "name": "LWF Employer (Haryana)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "LWF Employer (Haryana)",
        "salary_component_abbr": "LWF HER",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },




        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "0 if gross_pay <= 25000 and custom_state == \"Gujarat\" else\r\n200 if custom_state == \"Gujarat\" else\r\n0",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.567976",
        "name": "Professional Tax (Gujarat)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (Gujarat)",
        "salary_component_abbr": "PTG",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": " 0 if gross_pay <= 15000 and custom_state == \"Andhra Pradesh\" else\r\n    150 if 15000 < gross_pay <= 20000 and custom_state == \"Andhra Pradesh\" else\r\n    200 if gross_pay > 20000 and custom_state == \"Andhra Pradesh\" else 0",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.547092",
        "name": "Professional Tax (Andhra Pradesh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (Andhra Pradesh)",
        "salary_component_abbr": "PTAN",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "(0 if gross_pay <= 10000 and custom_state == \"West Bengal\" else \n110 if 10001 <= gross_pay <= 15000 and custom_state == \"West Bengal\" else \n130 if 15001 <= gross_pay <= 25000 and custom_state == \"West Bengal\" else \n150 if 25001 <= gross_pay <= 40000 and custom_state == \"West Bengal\" else \n200 if custom_state == \"West Bengal\" and designation!=\"Apprentice\" else 0)",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.530554",
        "name": "Professional Tax (West Bengal)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (West Bengal)",
        "salary_component_abbr": "PTAN_1",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "0 if custom_state==\"Delhi\" else 0",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.515557",
        "name": "Professional Tax (Delhi)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (Delhi)",
        "salary_component_abbr": "PTD",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "0 if custom_state==\"Uttarakhand\" else 0",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.494158",
        "name": "Professional Tax (Uttarakhand)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (Uttarakhand)",
        "salary_component_abbr": "PTU",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "(0 if ((gender == 'Male' and gross_pay <= 7500) or (gender == 'Female' and gross_pay <= 25000)) else \n175 if (gender == 'Male' and 7500 < gross_pay  <= 10000) else \n200 if ((gender == 'Male' and gross_pay > 10000) or (gender == 'Female' and gross_pay  > 25000)) else \n300 if (getdate(start_date).month == 2 and ((gender == 'Male' and gross_pay > 10000) or (gender == 'Female' and gross_pay > 25000))) else 0\n)if custom_state == \"Maharashtra\" else 0",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.472856",
        "name": "Professional Tax (Maharashtra)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (Maharashtra)",
        "salary_component_abbr": "PTUM",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "1250/6 if custom_state == \"Tamil Nadu\" else 0",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.455167",
        "name": "Professional Tax (Tamil Nadu)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (Tamil Nadu)",
        "salary_component_abbr": "PTUM_1",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        },
        {
        "accounts": [],
        "amount": 0.0,
        "amount_based_on_formula": 1,
        "component_type": "Professional Tax",

        "create_separate_payment_entry_against_benefit_claim": 0,

        "custom_component_sub_type": "Fixed",




        "custom_is_part_of_ctc": 0,







        "custom_sequence": "1",
        "custom_sub_category": "",
        "custom_tax_exemption_applicable_based_on_regime": 0,
        "deduct_full_tax_on_selected_payroll_date": 0,
        "depends_on_payment_days": 0,

        "disabled": 0,
        "do_not_include_in_total": 0,
        "docstatus": 0,
        "doctype": "Salary Component",
        "exempted_from_income_tax": 0,
        "formula": "0 if custom_state==\"Uttar Pradesh\" else 0",
        "is_flexible_benefit": 0,
        "is_income_tax_component": 0,
        "is_tax_applicable": 0,
        "max_benefit_amount": 0.0,
        "modified": "2025-07-26 10:48:11.402035",
        "name": "Professional Tax (Uttar Pradesh)",
        "only_tax_impact": 0,
        "pay_against_benefit_claim": 0,
        "remove_if_zero_valued": 1,
        "round_to_the_nearest_integer": 0,
        "salary_component": "Professional Tax (Uttar Pradesh)",
        "salary_component_abbr": "PTUM_1_1",
        "statistical_component": 0,
        "type": "Deduction",
        "variable_based_on_taxable_salary": 0
        }


    ]

    for i in data:
        insert_record(i)

def insert_record(i):
    if not frappe.db.exists("Salary Component", i["name"]):
        doc = frappe.new_doc("Salary Component")
        doc.update(i)
        doc.save()
