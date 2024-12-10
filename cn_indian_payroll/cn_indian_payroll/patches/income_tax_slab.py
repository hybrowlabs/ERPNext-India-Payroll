import frappe

def execute():

    data=[
        {
        "allow_tax_exemption": 1,
        
        "company": "",
        "currency": "INR",
        "custom_maximum_amount": 12500.0,
        "custom_select_regime": "Old Regime",
        "custom_taxable_income_is_less_than": 500000.0,
        "disabled": 0,
        "docstatus": 1,
        "doctype": "Income Tax Slab",
        "effective_from": "2023-01-11",
        
        "name": "Old Regime 24-25",
        "other_taxes_and_charges": [
        {
            "custom_is_education_cess": 0,
            "custom_is_surcharge": 0,
            "description": "Education Cess",
            "max_taxable_income": 5000000.0,
            "min_taxable_income": 0.0,
            "parent": "Old Regime",
            "parentfield": "other_taxes_and_charges",
            "parenttype": "Income Tax Slab",
            "percent": 4.0
        },
        {
            "custom_is_education_cess": 0,
            "custom_is_surcharge": 0,
            "description": "Education Cess + Surcharge",
            "max_taxable_income": 10000000.0,
            "min_taxable_income": 5000000.0,
            "parent": "Old Regime",
            "parentfield": "other_taxes_and_charges",
            "parenttype": "Income Tax Slab",
            "percent": 14.4
        }
        ],
        "slabs": [
        {
            "condition": "annual_taxable_amount > 500000",
            "from_amount": 250000.0,
            "parent": "Old Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 5.0,
            "to_amount": 500000.0
        },
        {
            
            "from_amount": 500000.0,
            "parent": "Old Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 20.0,
            "to_amount": 1000000.0
        },
        {
            
            "from_amount": 1000000.0,
            "parent": "Old Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 30.0,
            "to_amount": 0.0
        }
        ],
        "standard_tax_exemption_amount": 50000.0
        },
        {
        "allow_tax_exemption": 1,
        
        "company": "",
        "currency": "INR",
        "custom_maximum_amount": 25000.0,
        "custom_select_regime": "New Regime",
        "custom_taxable_income_is_less_than": 700000.0,
        "disabled": 0,
        "docstatus": 1,
        "doctype": "Income Tax Slab",
        "effective_from": "2024-04-01",
        
        "name": "New Regime 24-25",
        "other_taxes_and_charges": [
        {
            "custom_is_education_cess": 0,
            "custom_is_surcharge": 0,
            "description": "Education Cess",
            "max_taxable_income": 5000000.0,
            "min_taxable_income": 0.0,
            "parent": "New Regime",
            "parentfield": "other_taxes_and_charges",
            "parenttype": "Income Tax Slab",
            "percent": 4.0
        },
        {
            "custom_is_education_cess": 0,
            "custom_is_surcharge": 0,
            "description": "Education Cess+surcharge",
            "max_taxable_income": 10000000.0,
            "min_taxable_income": 5000000.0,
            "parent": "New Regime",
            "parentfield": "other_taxes_and_charges",
            "parenttype": "Income Tax Slab",
            "percent": 14.4
        }
        ],
        "slabs": [
        {
            "condition": "annual_taxable_amount > 700000",
            "from_amount": 300000.0,
            "parent": "New Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 5.0,
            "to_amount": 700000.0
        },
        {
            "condition": "annual_taxable_amount > 700000",
            "from_amount": 700000.0,
            "parent": "New Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 10.0,
            "to_amount": 1000000.0
        },
        {
           
            "from_amount": 1000000.0,
            "parent": "New Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 15.0,
            "to_amount": 1200000.0
        },
        {
           
            "from_amount": 1200000.0,
            "parent": "New Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 20.0,
            "to_amount": 1500000.0
        },
        {
           
            "from_amount": 1500000.0,
            "parent": "New Regime",
            "parentfield": "slabs",
            "parenttype": "Income Tax Slab",
            "percent_deduction": 30.0,
            "to_amount": 0.0
        }
        ],
        "standard_tax_exemption_amount": 75000.0
        }
        ]

    for i in data:
        insert_record(i)

def insert_record(i):

    if not frappe.db.exists("Income Tax Slab", i["name"]):
        doc=frappe.new_doc("Income Tax Slab")
        doc.update(i)
        doc.save()






    