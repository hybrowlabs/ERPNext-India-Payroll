import frappe

def on_submit(doc, method):
    insert_form_16(doc)

def insert_form_16(doc):
    frappe.msgprint(f"Inserting Form 16 for proof {doc.name}")


    if not frappe.db.exists("Form 16", {"proof_id": doc.name}):
        form16 = frappe.get_doc({
            "doctype": "Form 16",
            "employee": doc.employee,
            "proof_id": doc.name,
            "currency": "INR",
            "company": doc.company,
            "submission_date": doc.submission_date,
            "payroll_period": doc.payroll_period,
            "total_actual_amount": doc.total_actual_amount,
            "exemption_amount": doc.exemption_amount,
            "house_rent_payment_amount":doc.house_rent_payment_amount,
            "rented_in_metro_city": doc.rented_in_metro_city,
            "monthly_house_rent": doc.monthly_house_rent,
            "total_eligible_hra_exemption": doc.total_eligible_hra_exemption,
            "monthly_eligible_amount": doc.monthly_hra_exemption,
            "annual_hra_exemption": doc.custom_annual_hra_exemption,
        })

        for d in doc.tax_exemption_proofs:
            form16.append("tax_exemption_proofs", {
                "exemption_sub_category": d.exemption_sub_category,
                "exemption_category": d.exemption_category,
                "amount": d.amount,
                "max_amount": d.max_amount,
            })

        form16.insert(ignore_permissions=True)
