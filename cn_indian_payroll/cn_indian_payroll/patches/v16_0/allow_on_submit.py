import frappe


def execute():

    data = [
        {
            "name": "Employee Tax Exemption Declaration-rented_in_metro_city-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "rented_in_metro_city",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Employee Tax Exemption Declaration-monthly_house_rent-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "monthly_house_rent",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Employee Tax Exemption Declaration-salary_structure_hra-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "salary_structure_hra",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Employee Tax Exemption Declaration-annual_hra_exemption-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "annual_hra_exemption",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Employee Tax Exemption Declaration-monthly_hra_exemption-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "monthly_hra_exemption",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Employee Tax Exemption Declaration-total_declared_amount-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "total_declared_amount",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Employee Tax Exemption Declaration-total_exemption_amount-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "total_exemption_amount",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Employee Tax Exemption Declaration-declarations-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Employee Tax Exemption Declaration",
            "field_name": "declarations",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Salary Structure Assignment-income_tax_slab-allow_on_submit",
            "doctype_or_field": "DocField",
            "doc_type": "Salary Structure Assignment",
            "field_name": "income_tax_slab",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
        },
        {
            "name": "Salary Component-component_type-options",
            "doctype_or_field": "DocField",
            "doc_type": "Salary Component",
            "field_name": "component_type",
            "property": "options",
            "value": "Provident Fund\nProvident Fund Loan\nAdditional Provident Fund\nProfessional Tax\nNPS\nESIC\nLTA",
        },
        {
            "name": "Salary Component-component_type-depends_on",
            "doctype_or_field": "DocField",
            "doc_type": "Salary Component",
            "field_name": "component_type",
            "property": "depends_on",
            "property_type": "Data",
            "value": "",
        },
    ]

    for i in data:
        insert_record(i)


def insert_record(i):
    if not frappe.db.exists("Property Setter", i["name"]):
        doc = frappe.new_doc("Property Setter")
        doc.update(i)
        doc.insert(ignore_permissions=True)
