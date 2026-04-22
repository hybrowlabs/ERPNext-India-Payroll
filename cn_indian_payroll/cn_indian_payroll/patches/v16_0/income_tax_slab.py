import frappe


def execute():

    data = [
        {
            "allow_tax_exemption": 1,
            "currency": "INR",
            "custom_maximum_amount": 60000.0,
            "custom_select_regime": "New Regime",
            "custom_taxable_income_is_less_than": 1200000.0,
            "disabled": 0,
            "docstatus": 1,
            "doctype": "Income Tax Slab",
            "effective_from": "2025-04-01",
            "modified": "2025-04-09 16:27:54.415010",
            "name": "New Regime 25-26",
            "custom_marginal_relief_applicable": 1,
            "custom_maximun_value": 1270000.0,
            "custom_minmum_value": 1200000.0,
            "other_taxes_and_charges": [
                {
                    "custom_is_education_cess": 1,
                    "custom_is_surcharge": 0,
                    "description": "Education Cess",
                    "max_taxable_income": 5000000.0,
                    "min_taxable_income": 0.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 4.0,
                },
                {
                    "custom_is_education_cess": 0,
                    "custom_is_surcharge": 0,
                    "description": "Surcharge 10%",
                    "max_taxable_income": 10000000.0,
                    "min_taxable_income": 5000000.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 10,
                },
                {
                    "custom_is_education_cess": 0,
                    "custom_is_surcharge": 0,
                    "description": "Surcharge 15%",
                    "max_taxable_income": 20000000.0,
                    "min_taxable_income": 10000000.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 15,
                },
                {
                    "custom_is_education_cess": 0,
                    "custom_is_surcharge": 0,
                    "description": "Surcharge 25%",
                    "max_taxable_income": 50000000.0,
                    "min_taxable_income": 20000000.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 25,
                },
            ],
            "slabs": [
                {
                    "condition": "annual_taxable_amount > 1200000",
                    "from_amount": 400001.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 5.0,
                    "to_amount": 800000.0,
                },
                {
                    "condition": "annual_taxable_amount > 1200000",
                    "from_amount": 800001.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 10.0,
                    "to_amount": 1200000.0,
                },
                {
                    "from_amount": 1200001.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 15.0,
                    "to_amount": 1600000.0,
                },
                {
                    "from_amount": 1600001.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 20.0,
                    "to_amount": 2000000.0,
                },
                {
                    "from_amount": 2000001.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 25.0,
                    "to_amount": 2400000.0,
                },
                {
                    "from_amount": 2400000.0,
                    "parent": "New Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 30.0,
                    "to_amount": 0.0,
                },
            ],
            "standard_tax_exemption_amount": 75000.0,
        },
        {
            "allow_tax_exemption": 1,
            "currency": "INR",
            "custom_maximum_amount": 12500.0,
            "custom_select_regime": "Old Regime",
            "custom_taxable_income_is_less_than": 500000.0,
            "disabled": 0,
            "docstatus": 1,
            "doctype": "Income Tax Slab",
            "effective_from": "2025-04-01",
            "modified": "2025-04-15 21:52:55.744863",
            "name": "Old Regime 25-26",
            "other_taxes_and_charges": [
                {
                    "custom_is_education_cess": 1,
                    "custom_is_surcharge": 0,
                    "description": "Education Cess",
                    "max_taxable_income": 5000000.0,
                    "min_taxable_income": 0.0,
                    "parent": "Old Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 4.0,
                },
                {
                    "custom_is_education_cess": 0,
                    "custom_is_surcharge": 0,
                    "description": "Education 10%",
                    "max_taxable_income": 10000000.0,
                    "min_taxable_income": 5000000.0,
                    "parent": "Old Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 10,
                },
                {
                    "custom_is_education_cess": 0,
                    "custom_is_surcharge": 0,
                    "description": "Surcharge 15%",
                    "max_taxable_income": 20000000.0,
                    "min_taxable_income": 10000000.0,
                    "parent": "Old Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 15,
                },
                {
                    "custom_is_education_cess": 0,
                    "custom_is_surcharge": 0,
                    "description": "Surcharge 25%",
                    "max_taxable_income": 50000000.0,
                    "min_taxable_income": 20000000.0,
                    "parent": "Old Regime 25-26",
                    "parentfield": "other_taxes_and_charges",
                    "parenttype": "Income Tax Slab",
                    "percent": 25,
                },
            ],
            "slabs": [
                {
                    "condition": "annual_taxable_amount > 500000",
                    "from_amount": 250000.0,
                    "parent": "Old Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 5.0,
                    "to_amount": 500000.0,
                },
                {
                    "from_amount": 500001.0,
                    "parent": "Old Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 20.0,
                    "to_amount": 1000000.0,
                },
                {
                    "from_amount": 1000001.0,
                    "parent": "Old Regime 25-26",
                    "parentfield": "slabs",
                    "parenttype": "Income Tax Slab",
                    "percent_deduction": 30.0,
                    "to_amount": 0.0,
                },
            ],
            "standard_tax_exemption_amount": 50000.0,
        },
    ]

    for i in data:
        insert_record(i)


def insert_record(i):
    if not frappe.db.exists("Income Tax Slab", i["name"]):
        for company in frappe.db.get_list("Company", fields=["name"]):
            combined_name = f"{i['name']} - ({company['name']})"
            if not frappe.db.exists("Income Tax Slab", combined_name):
                doc = frappe.new_doc("Income Tax Slab")
                doc.company = company["name"]
                doc.name = combined_name
                for key, value in i.items():
                    if key != "company" and key != "name":
                        doc.set(key, value)
                doc.save()
