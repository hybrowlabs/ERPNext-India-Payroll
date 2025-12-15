import frappe
from frappe.utils import flt


def get_total_exemption_amount(declarations):
    exemptions = frappe._dict()

    A = B = C = D = E = F = 0

    for d in declarations:
        if d.exemption_category != "Section 80D":
            exemptions.setdefault(d.exemption_category, frappe._dict())
            category = exemptions[d.exemption_category]

            if not category.get("max_amount"):
                category.max_amount = frappe.db.get_value(
                    "Employee Tax Exemption Category",
                    d.exemption_category,
                    "max_amount",
                )

            sub_amount = (
                d.max_amount
                if d.max_amount and flt(d.amount) > flt(d.max_amount)
                else flt(d.amount)
            )

            category.setdefault("total_exemption_amount", 0.0)
            category.total_exemption_amount += sub_amount

            if category.max_amount:
                category.total_exemption_amount = min(
                    category.total_exemption_amount, category.max_amount
                )

        else:
            sub_cat = frappe.get_doc(
                "Employee Tax Exemption Sub Category", d.exemption_sub_category
            )

            amt = flt(d.amount)
            key = sub_cat.custom_80d_type

            if key == "SELF_MEDICAL_BELOW":
                A = amt
            elif key == "SELF_MEDICAL_ABOVE":
                B = amt
            elif key == "PARENT_MEDICAL_BELOW":
                C = amt
            elif key == "PARENT_MEDICAL_ABOVE":
                D = amt
            elif key == "SELF_PREVENTIVE":
                E = amt
            elif key == "PARENT_PREVENTIVE":
                F = amt

    if B > 0:  # Senior citizen exists
        self_cap = 50000
        self_medical = min(B, self_cap)
    else:
        self_cap = 25000
        self_medical = min(A, self_cap)

    self_preventive = min(5000, max(0, self_cap - self_medical), E)

    self_total = self_medical + self_preventive

    if D > 0:  # Any parent senior → whole block senior
        parent_cap = 50000
        parent_medical = min(D, parent_cap)
    else:
        parent_cap = 25000
        parent_medical = min(C, parent_cap)

    parent_preventive = min(5000, max(0, parent_cap - parent_medical), F)

    parent_total = parent_medical + parent_preventive

    total_80d = min(100000, self_total + parent_total)

    exemptions.setdefault("Section 80D", frappe._dict())
    exemptions["Section 80D"].total_exemption_amount = total_80d

    total_exemption_amount = sum(
        flt(d.total_exemption_amount) for d in exemptions.values()
    )

    return total_exemption_amount, total_80d
