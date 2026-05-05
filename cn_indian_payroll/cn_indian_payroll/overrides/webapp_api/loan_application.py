import frappe


@frappe.whitelist()
def get_loan_product(company=None):

    loan_product_list = frappe.db.get_all(
        "Loan Product",
        filters={"disabled": 0},
        fields=["product_name", "rate_of_interest"]
    )

    return {
        "loan_product": loan_product_list,

    }
