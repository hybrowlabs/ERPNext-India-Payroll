import frappe
from frappe.utils import (
	add_days,
	ceil,
	cint,
	cstr,
	date_diff,
	floor,
	flt,
	formatdate,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	money_in_words,
	rounded,
)
from hrms.payroll.doctype.salary_slip.salary_slip import eval_tax_slab_condition
def override_calculate_tax_by_tax_slab(annual_taxable_earning, tax_slab, eval_globals=None, eval_locals=None):
        eval_locals.update({"annual_taxable_earning": annual_taxable_earning})
        base_tax = 0
        rebate = 0
        other_taxes_and_charges = 0



        # Step 1: Calculate base tax from slabs
        for slab in tax_slab.slabs:
            cond = cstr(slab.condition).strip()
            if cond and not eval_tax_slab_condition(cond, eval_globals, eval_locals):
                continue

            from_amt = slab.from_amount
            to_amt = slab.to_amount or annual_taxable_earning
            rate = slab.percent_deduction * 0.01

            if annual_taxable_earning > from_amt:
                taxable_range = min(annual_taxable_earning, to_amt) - from_amt
                base_tax += taxable_range * rate

        # Step 2: Marginal Relief (Rebate Logic)

        if tax_slab.custom_marginal_relief_applicable and tax_slab.custom_minmum_value and tax_slab.custom_maximun_value:
            if tax_slab.custom_minmum_value < annual_taxable_earning < tax_slab.custom_maximun_value:
                excess_income = annual_taxable_earning - tax_slab.custom_minmum_value
                if base_tax > excess_income:
                    rebate = base_tax - excess_income
                    base_tax -= rebate

        # Step 3: Cess and Other Charges AFTER Rebate
        for d in tax_slab.other_taxes_and_charges:
            if flt(d.min_taxable_income) and flt(d.min_taxable_income) > annual_taxable_earning:
                continue
            if flt(d.max_taxable_income) and flt(d.max_taxable_income) < annual_taxable_earning:
                continue

            charge_percent = flt(d.percent)
            charge = base_tax * charge_percent / 100.0
            other_taxes_and_charges += charge

        final_tax = base_tax + other_taxes_and_charges

        # frappe.msgprint(f"Base Tax: ₹{round(base_tax, 2)}\n"
        #                 f"Rebate: ₹{round(rebate, 2)}\n"
        #                 f"Cess: ₹{round(other_taxes_and_charges, 2)}\n"
        #                 f"Final Tax: ₹{round(final_tax, 2)}")

        return round(final_tax, 2), round(other_taxes_and_charges, 2)
