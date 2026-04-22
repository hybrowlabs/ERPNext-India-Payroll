
import frappe
import json




@frappe.whitelist()
def get_salary_component(data=None, component=None):
    try:
        data = json.loads(data)

        salary_component = data.get("salary_component")
        component_type = data.get("type")

        if component and salary_component:
            existing_components = frappe.get_list(
                'Salary Component',
                filters={
                    "name": salary_component,
                    "disabled": 0,
                    "type": data.get("component_type"),
                },
                fields=['*']
            )

            if len(existing_components) > 0:
                get_each_doc = frappe.get_doc("Salary Component", existing_components[0].name)

                get_each_doc.depends_on_payment_days = data.get("depends_on_payment_days")
                get_each_doc.is_tax_applicable = data.get("is_tax_applicable")
                get_each_doc.do_not_include_in_total = data.get("do_not_include_in_total")
                get_each_doc.remove_if_zero_valued = data.get("remove_if_zero_valued")
                get_each_doc.disabled = data.get("disabled")
                get_each_doc.custom_is_part_of_ctc = data.get("is_part_of_ctc")
                get_each_doc.custom_tax_exemption_applicable_based_on_regime = data.get("tax_applicable_based_on_regime")
                get_each_doc.custom_regime = data.get("regime")
                get_each_doc.condition = data.get("condition")
                get_each_doc.formula = data.get("formula")
                get_each_doc.accrual_component = data.get("accrual_component")
                get_each_doc.arrear_component = data.get("arrear_component")
                get_each_doc.is_flexible_benefit = data.get("is_flexible_benefit")
                get_each_doc.payout_method = data.get("payout_method")
                get_each_doc.payout_unclaimed_amount_in_final_payroll_cycle = data.get("payout_unclaimed_amount_in_final_payroll_cycle")

                get_each_doc.save()


                get_abbr_component = frappe.get_list('Salary Component',
                    filters={

                        "disabled":0,

                        "salary_component_abbr":data.get("abbr"),


                        },
                        fields=['*']
                        )

                if len(get_abbr_component)>0:
                    frappe.msgprint("Another component uses same abbr,plz change the abbr")

                else:
                    get_each_doc = frappe.new_doc('Salary Component')
                    get_each_doc.name=data.get("salary_component")
                    get_each_doc.salary_component=data.get("salary_component")
                    get_each_doc.salary_component_abbr=data.get("abbr")
                    get_each_doc.type=data.get("component_type")

                    get_each_doc.depends_on_payment_days=data.get("depends_on_payment_days")
                    get_each_doc.is_tax_applicable=data.get("is_tax_applicable")
                    get_each_doc.do_not_include_in_total=data.get("do_not_include_in_total")
                    get_each_doc.remove_if_zero_valued=data.get("remove_if_zero_valued")
                    get_each_doc.disabled=data.get("disabled")
                    get_each_doc.custom_is_part_of_ctc=data.get("is_part_of_ctc")

                    get_each_doc.custom_tax_exemption_applicable_based_on_regime=data.get("tax_applicable_based_on_regime")
                    get_each_doc.custom_regime=data.get("regime")
                    get_each_doc.accrual_component = data.get("accrual_component")
                    get_each_doc.arrear_component = data.get("arrear_component")
                    get_each_doc.is_flexible_benefit = data.get("is_flexible_benefit")
                    get_each_doc.payout_method = data.get("payout_method")
                    get_each_doc.payout_unclaimed_amount_in_final_payroll_cycle = data.get("payout_unclaimed_amount_in_final_payroll_cycle")



                    get_each_doc.insert()

                    if data.get("visibility_type")=="Fixed":
                        get_library_item = frappe.get_doc('Salary Component Library Item',salary_component)
                        get_library_item.component_added = 1
                        get_library_item.save()
                        frappe.msgprint("Salary Component Added")
                    else:

                        frappe.msgprint("Salary Component Added")


            else:
                get_abbr_component = frappe.get_list('Salary Component',
                    filters={

                        "disabled":0,

                        "salary_component_abbr":data.get("abbr"),


                        },
                        fields=['*']
                        )

                if len(get_abbr_component)>0:
                    frappe.msgprint("Another component uses same abbr,plz change the abbr")

                else:
                    get_each_doc = frappe.new_doc('Salary Component')
                    get_each_doc.name=data.get("salary_component")
                    get_each_doc.salary_component=data.get("salary_component")
                    get_each_doc.salary_component_abbr=data.get("abbr")
                    get_each_doc.type=data.get("component_type")

                    get_each_doc.depends_on_payment_days=data.get("depends_on_payment_days")
                    get_each_doc.is_tax_applicable=data.get("is_tax_applicable")
                    get_each_doc.do_not_include_in_total=data.get("do_not_include_in_total")
                    get_each_doc.remove_if_zero_valued=data.get("remove_if_zero_valued")
                    get_each_doc.custom_is_part_of_gross_pay=data.get("is_part_of_gross_pay")
                    get_each_doc.disabled=data.get("disabled")
                    get_each_doc.custom_is_part_of_ctc=data.get("is_part_of_ctc")
                    get_each_doc.custom_perquisite=data.get("perquisite")
                    get_each_doc.custom_is_accrual=data.get("is_accrual")
                    get_each_doc.custom_is_reimbursement=data.get("reimbursement")

                    get_each_doc.custom_is_part_of_appraisal=data.get("is_part_of_appraisal")
                    get_each_doc.custom_tax_exemption_applicable_based_on_regime=data.get("tax_applicable_based_on_regime")
                    get_each_doc.custom_regime=data.get("regime")
                    get_each_doc.accrual_component = data.get("accrual_component")
                    get_each_doc.arrear_component = data.get("arrear_component")
                    get_each_doc.is_flexible_benefit = data.get("is_flexible_benefit")
                    get_each_doc.payout_method = data.get("payout_method")
                    get_each_doc.payout_unclaimed_amount_in_final_payroll_cycle = data.get("payout_unclaimed_amount_in_final_payroll_cycle")


                    get_each_doc.insert()


                    if data.get("visibility_type")=="Fixed":
                        get_library_item = frappe.get_doc('Salary Component Library Item',salary_component)
                        get_library_item.component_added = 1
                        get_library_item.save()
                        frappe.msgprint("Salary Component Added")
                    else:

                        frappe.msgprint("Salary Component Added")







    except Exception as e:
        frappe.log_error(f"Error in get_salary_component: {e}")
        raise
