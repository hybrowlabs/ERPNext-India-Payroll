import frappe

def execute():
    data=[
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.651466",
  "name": "Section 16(iii)"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.702379",
  "name": "Section 16(iA)"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.708359",
  "name": "Section 80CCD(2)"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.713210",
  "name": "Section 80E"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.718170",
  "name": "Section 80DD"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.722916",
  "name": "Section 80U"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.727085",
  "name": "Section 10(14)"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.731421",
  "name": "Section 10(13A)"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 99999.0,
  "modified": "2024-12-10 11:58:40.178496",
  "name": "Section 16"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.741525",
  "name": "Section 80D"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.747789",
  "name": "Section 80CCD(1B)"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 150000.0,
  "modified": "2024-12-10 11:54:02.753386",
  "name": "Section 80C"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.758789",
  "name": "Section 80EE"
 },
 {
  "docstatus": 0,
  "doctype": "Employee Tax Exemption Category",
  "is_active": 1,
  "max_amount": 0.0,
  "modified": "2024-12-10 11:54:02.764164",
  "name": "Section 10"
 }
]
    for i in data:
        insert_record(i)

def insert_record(i):

    if not frappe.db.exists("Employee Tax Exemption Category", i["name"]):
        doc=frappe.new_doc("Employee Tax Exemption Category")
        doc.update(i)
        doc.save()






    










