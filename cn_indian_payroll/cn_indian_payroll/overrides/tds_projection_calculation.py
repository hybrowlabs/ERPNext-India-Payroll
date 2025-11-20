import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from datetime import datetime
from frappe import _
import json
from dateutil.relativedelta import relativedelta




@frappe.whitelist()
def calculate_tds_projection(doc):
    if isinstance(doc, str):
        doc = frappe._dict(json.loads(doc))

    current_taxable_earnings_old_regime = 0
    current_taxable_earnings_new_regime = 0
    future_taxable_earnings_old_regime = 0
    future_taxable_earnings_new_regime = 0
    loan_perquisite_component=None
    loan_perquisite_amount=0
    pt_amount=0
    pf_amount=0
    nps_amount=0

    old_regime_standard_value = 0
    new_regime_standard_value = 0

    hra_exemptions = 0

    eighty_c_maximum_limit = 0

    old_regime_annual_taxable_income=0
    new_regime_annual_taxable_income=0

    month_count=0
    num_months=0

    if doc.get('employee'):
        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": doc.get('employee'),
                "docstatus": 1,
                "custom_payroll_period": doc.get('payroll_period'),
            },
            fields=["*"],
            order_by="from_date desc",
        )

        if latest_salary_structure:
            assignment = latest_salary_structure[0]
            employee=frappe.get_doc("Employee", assignment.employee)
            get_payroll_period = frappe.get_doc("Payroll Period", assignment.custom_payroll_period)

            effective_start_date = assignment.from_date
            payroll_end_date = get_payroll_period.end_date
            payroll_start_date = get_payroll_period.start_date
            doj = employee.date_of_joining

            start_candidates = [d for d in [effective_start_date, payroll_start_date, doj] if d]
            start = max(datetime.strptime(str(d), "%Y-%m-%d").date() if isinstance(d, str) else d for d in start_candidates)
            end = datetime.strptime(str(payroll_end_date), "%Y-%m-%d").date() if isinstance(payroll_end_date, str) else payroll_end_date

            num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1


            loan_repayments = frappe.db.get_list(
                "Loan Repayment Schedule",
                filters={
                    "custom_employee": doc.get('employee'),
                    "status": "Active",
                    "docstatus": 1,
                },
                fields=["*"],
            )

            if loan_repayments:
                loan_perquisite_component="Loan Perquisite"
                for repayment in loan_repayments:
                    get_each_perquisite = frappe.get_doc(
                        "Loan Repayment Schedule", repayment.name
                    )
                    if len(get_each_perquisite.custom_loan_perquisite) > 0:
                        for date in get_each_perquisite.custom_loan_perquisite:
                            payment_date = frappe.utils.getdate(
                                date.payment_date
                            )
                            if payroll_start_date <= payment_date <= payroll_end_date:
                                loan_perquisite_amount += date.perquisite_amount

            else:
                loan_perquisite_component="Loan Perquisite"
                loan_perquisite_amount=0

        get_exemption_category = frappe.get_list(
            "Employee Tax Exemption Category",
            filters={
                "custom_select_section": "80 C",

                "is_active": 1,
            },
            fields=["*"],
        )
        if get_exemption_category:
            eighty_c_maximum_limit = get_exemption_category[0].max_amount



        if doc.get('custom_tax_regime') == "Old Regime" and doc.get('monthly_house_rent'):
            hra_exemptions = doc.get('annual_hra_exemption')


        latest_tax_slab_old_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company": doc.get('company'),
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "Old Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_old_regime:
            old_regime_standard_value = latest_tax_slab_old_regime[0].standard_tax_exemption_amount

        latest_tax_slab_new_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company": doc.get('company'),
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "New Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_new_regime:
            new_regime_standard_value = latest_tax_slab_new_regime[0].standard_tax_exemption_amount




        get_all_salary_slip = frappe.get_list(
            "Salary Slip",
            filters={
                "employee": doc.get('employee'),
                "custom_payroll_period": doc.get('payroll_period'),
                "docstatus": ["in", [0,1]],
            },
            fields=["*"],
            order_by="end_date desc",
        )
        if len(get_all_salary_slip)==0:
            current_taxable_earnings_old_regime = 0
            current_taxable_earnings_new_regime = 0


            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=doc.get('employee'),
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
                )
            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    if not earning.additional_salary:

                        earning_component_data = frappe.get_doc(
                            "Salary Component", earning.salary_component
                        )

                        if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):

                            future_taxable_earnings_old_regime += earning.amount * (
                                num_months
                            )
                            future_taxable_earnings_new_regime += earning.amount * (
                                num_months
                            )


                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "Old Regime"
                                and earning_component_data.custom_component_sub_type== "Fixed"

                            ):
                                future_taxable_earnings_old_regime += earning.amount * (
                                num_months
                            )


                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "New Regime"
                                and earning_component_data.custom_component_sub_type== "Fixed"

                            ):

                                future_taxable_earnings_new_regime += earning.amount * (
                                    num_months
                                )

                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "All"
                                and earning_component_data.custom_component_sub_type== "Fixed"
                                and earning_component_data.component_type =="NPS"


                            ):
                            nps_amount+=earning.amount*(num_months)

                    else:

                        earning_component_data = frappe.get_doc(
                            "Salary Component", earning.salary_component
                        )

                        if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):

                            future_taxable_earnings_old_regime += earning.amount
                            future_taxable_earnings_new_regime += earning.amount


                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "Old Regime"
                                and earning_component_data.custom_component_sub_type== "Fixed"

                            ):
                                future_taxable_earnings_old_regime += earning.amount



                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "New Regime"
                                and earning_component_data.custom_component_sub_type== "Fixed"

                            ):

                                future_taxable_earnings_new_regime += earning.amount

                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "All"
                                and earning_component_data.custom_component_sub_type== "Fixed"
                                and earning_component_data.component_type =="NPS"


                            ):
                            nps_amount+=earning.amount


                for deduction in salary_slip_preview.deductions:
                    if not deduction.additional_salary:
                        deduction_component_data = frappe.get_doc(
                            "Salary Component", deduction.salary_component
                        )
                        if (
                                deduction_component_data.component_type =="Professional Tax"
                                and deduction_component_data.custom_component_sub_type== "Fixed"

                            ):
                            pt_amount+=deduction.amount*(num_months)

                        if (
                                deduction_component_data.component_type =="Provident Fund"
                                and deduction_component_data.custom_component_sub_type== "Fixed"

                            ):

                            pf_amount+=deduction.amount*(num_months)
                    else:
                        deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                        )
                        if (
                                deduction_component_data.component_type =="Professional Tax"
                                and deduction_component_data.custom_component_sub_type== "Fixed"

                            ):
                            pt_amount+=deduction.amount

                        if (
                                deduction_component_data.component_type =="Provident Fund"
                                and deduction_component_data.custom_component_sub_type== "Fixed"

                            ):

                            pf_amount+=deduction.amount


        else:

            month_count=get_all_salary_slip[0].custom_month_count
            for slip in get_all_salary_slip:
                get_each_sslip= frappe.get_doc("Salary Slip", slip.name)
                for earning in get_each_sslip.earnings:
                    earning_component_data = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )

                    if (
                        earning_component_data.is_tax_applicable == 1
                        and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                        and earning_component_data.custom_regime == "All"


                    ):
                        current_taxable_earnings_old_regime += earning.amount
                        current_taxable_earnings_new_regime += earning.amount




                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "Old Regime"


                        ):
                            current_taxable_earnings_old_regime += earning.amount



                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "New Regime"


                        ):

                            current_taxable_earnings_new_regime += earning.amount



                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"

                            and earning_component_data.component_type =="NPS"


                        ):
                        nps_amount+=earning.amount

                for deduction in get_each_sslip.deductions:
                    deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if (
                            deduction_component_data.component_type =="Professional Tax"


                        ):
                        pt_amount+=deduction.amount

                    if (
                            deduction_component_data.component_type =="Provident Fund"


                        ):

                        pf_amount+=deduction.amount

            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=doc.get('employee'),
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
                )
            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    if not earning.additional_salary:

                        earning_component_data = frappe.get_doc(
                            "Salary Component", earning.salary_component
                        )

                        if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):

                            future_taxable_earnings_old_regime += earning.amount * (
                                month_count
                            )
                            future_taxable_earnings_new_regime += earning.amount * (
                                month_count
                            )


                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "Old Regime"
                                and earning_component_data.custom_component_sub_type== "Fixed"

                            ):
                                future_taxable_earnings_old_regime += earning.amount * (
                                month_count
                            )


                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "New Regime"
                                and earning_component_data.custom_component_sub_type== "Fixed"

                            ):

                                future_taxable_earnings_new_regime += earning.amount * (
                                    month_count
                                )

                        if (
                                earning_component_data.is_tax_applicable == 1
                                and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                                and earning_component_data.custom_regime == "All"
                                and earning_component_data.custom_component_sub_type== "Fixed"
                                and earning_component_data.component_type =="NPS"


                            ):
                            nps_amount+=earning.amount*(month_count)


                for deduction in salary_slip_preview.deductions:
                    if not deduction.additional_salary:
                        deduction_component_data = frappe.get_doc(
                            "Salary Component", deduction.salary_component
                        )
                        if (
                                deduction_component_data.component_type =="Professional Tax"
                                and deduction_component_data.custom_component_sub_type== "Fixed"

                            ):
                            pt_amount+=deduction.amount*(month_count)

                        if (
                                deduction_component_data.component_type =="Provident Fund"
                                and deduction_component_data.custom_component_sub_type== "Fixed"

                            ):

                            pf_amount+=deduction.amount*(month_count)


        pf_max_amount=min(eighty_c_maximum_limit, pf_amount)



        if doc.get('custom_tax_regime') == "Old Regime" :
            total_new_regime_deductions = nps_amount
            total_old_regime_deductions = (doc.get('total_exemption_amount')-(pt_amount))
        if doc.get('custom_tax_regime') == "New Regime" :
            total_new_regime_deductions = doc.get('total_exemption_amount')
            total_old_regime_deductions = pf_max_amount + pt_amount + nps_amount



        old_regime_annual_taxable_income = max(
            round(current_taxable_earnings_old_regime + future_taxable_earnings_old_regime + loan_perquisite_amount)
            - round(pt_amount)
            - old_regime_standard_value
            - round(total_old_regime_deductions),
            0
        )

        new_regime_annual_taxable_income = max(
            round(current_taxable_earnings_new_regime + future_taxable_earnings_new_regime + loan_perquisite_amount)
            - new_regime_standard_value
            - round(total_new_regime_deductions),
            0
        )

        employee = doc.get("employee")
        company = doc.get("company")
        payroll_period = doc.get("payroll_period")
        old_annual_slab = old_regime_annual_taxable_income or 0
        new_annual_slab = new_regime_annual_taxable_income or 0

        slab_result = slab_calculation(
            employee=employee,
            company=company,
            payroll_period=payroll_period,
            old_annual_slab=old_annual_slab,
            new_annual_slab=new_annual_slab
        )



        return {
                "num_months": num_months if num_months else 0,
                "month_count": month_count if month_count else 0,
                "current_taxable_earnings_old_regime":round(current_taxable_earnings_old_regime),
                "current_taxable_earnings_new_regime":round(current_taxable_earnings_new_regime),
                "future_taxable_earnings_new_regime":round(future_taxable_earnings_new_regime),
                "future_taxable_earnings_old_regime":round(future_taxable_earnings_old_regime),
                "loan_perquisite_component":loan_perquisite_component,
                "loan_perquisite_amount":round(loan_perquisite_amount),
                "total_taxable_earnings_old_regime": round(current_taxable_earnings_old_regime + future_taxable_earnings_old_regime + loan_perquisite_amount),
                "total_taxable_earnings_new_regime": round(current_taxable_earnings_new_regime + future_taxable_earnings_new_regime + loan_perquisite_amount),
                "pt_amount":round(pt_amount),
                "old_regime_standard_value": old_regime_standard_value,
                "new_regime_standard_value": new_regime_standard_value,
                "hra_exemptions": hra_exemptions,
                "total_old_regime_deductions": round(total_old_regime_deductions),
                "total_new_regime_deductions": round(total_new_regime_deductions),
                "old_regime_annual_taxable_income": round(old_regime_annual_taxable_income),
                "new_regime_annual_taxable_income": round(new_regime_annual_taxable_income),
                "old_regime_from_amounts": slab_result.get("from_amount"),
                "old_regime_to_amounts": slab_result.get("to_amount"),
                "old_regime_percentages": slab_result.get("percentage"),
                "old_regime_tax_per_slab": slab_result.get("total_value"),
                "old_regime_total_tax": slab_result.get("total_sum"),
                "old_regime_rebate_limit": slab_result.get("rebate"),
                "old_regime_max_amount": slab_result.get("max_amount"),
                "old_regime_rebate_amount": slab_result.get("old_rebate_value"),
                "old_regime_surcharge": slab_result.get("old_surcharge_m"),
                "old_regime_education_cess": slab_result.get("old_education_cess"),
                "new_regime_from_amounts": slab_result.get("from_amount_new"),
                "new_regime_to_amounts": slab_result.get("to_amount_new"),
                "new_regime_percentages": slab_result.get("percentage_new"),
                "new_regime_tax_per_slab": slab_result.get("total_value_new"),
                "new_regime_total_tax": slab_result.get("total_sum_new"),
                "new_regime_rebate_limit": slab_result.get("rebate_new"),
                "new_regime_max_amount": slab_result.get("max_amount_new"),
                "new_regime_marginal_relief_min": slab_result.get("new_regime_marginal_relief_min_value"),
                "new_regime_marginal_relief_max": slab_result.get("new_regime_marginal_relief_max_value"),
                "old_regime_marginal_relief_min": slab_result.get("old_regime_marginal_relief_min_value"),
                "old_regime_marginal_relief_max": slab_result.get("old_regime_marginal_relief_max_value"),
                "new_regime_rebate_amount": slab_result.get("new_rebate_value"),
                "new_regime_surcharge": slab_result.get("new_surcharge_m"),
                "new_regime_education_cess": slab_result.get("new_education_cess"),
                "total_tax_already_paid": slab_result.get("tax_already_paid")



                }

@frappe.whitelist()
def slab_calculation(
    employee, company, payroll_period, old_annual_slab, new_annual_slab
):
    old_annual_slab = float(old_annual_slab)
    new_annual_slab = float(new_annual_slab)

    latest_tax_slab = frappe.get_list(
        "Income Tax Slab",
        filters={
            "company": company,
            "docstatus": 1,
            "disabled": 0,
            "custom_select_regime": "Old Regime",
        },
        fields=["*"],
        order_by="effective_from DESC",
        limit=1,
    )

    if latest_tax_slab:
        for slab in latest_tax_slab:
            income_doc = frappe.get_doc("Income Tax Slab", slab.name)

            total_value = []
            from_amount = []
            to_amount = []
            percentage = []
            difference = []
            total_array = []

            total_sum = 0
            old_rebate_value = 0
            old_surcharge_m = 0
            old_education_cess = 0

            old_regime_marginal_relief_min_value = 0
            old_regime_marginal_relief_max_value = 0


            old_rebate = income_doc.custom_taxable_income_is_less_than
            old_max_amount = income_doc.custom_maximum_amount

            if (
                income_doc.custom_marginal_relief_applicable
                and income_doc.custom_minmum_value
                and income_doc.custom_maximun_value
            ):
                old_regime_marginal_relief_min_value = income_doc.custom_minmum_value
                old_regime_marginal_relief_max_value = income_doc.custom_maximun_value

            if old_annual_slab > old_rebate:
                # Store all slab details in a structured list
                for i in income_doc.slabs:
                    total_array.append(
                        {
                            "from": i.from_amount,
                            "to": i.to_amount,
                            "percent": i.percent_deduction,
                        }
                    )

                # Iterate through the slabs to calculate tax
                for slab in total_array:
                    if slab["to"] == 0.0:  # Upper limit not defined
                        if round(old_annual_slab) >= slab["from"]:
                            taxable_amount = round(old_annual_slab) - slab["from"]

                            tax_percent = slab["percent"]
                            tax_amount = round((taxable_amount * tax_percent) / 100)

                            remaining_slabs = [
                                s for s in total_array if s["from"] < slab["from"]
                            ]
                            for rem_slab in remaining_slabs:
                                from_amount.append(rem_slab["from"])
                                to_amount.append(rem_slab["to"])
                                percentage.append(rem_slab["percent"])
                                difference.append(rem_slab["to"] - rem_slab["from"])
                                total_value.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount.append(slab["from"])
                            to_amount.append(slab["to"])
                            percentage.append(tax_percent)
                            difference.append(taxable_amount)
                            total_value.append(tax_amount)

                    else:  # Standard slab range
                        if slab["from"] <= round(old_annual_slab) <= slab["to"]:
                            taxable_amount = round(old_annual_slab) - slab["from"]
                            tax_percent = slab["percent"]
                            tax_amount = round((taxable_amount * tax_percent) / 100)

                            # Process lower slabs
                            remaining_slabs = [
                                s for s in total_array if s["from"] < slab["from"]
                            ]
                            for rem_slab in remaining_slabs:
                                from_amount.append(rem_slab["from"])
                                to_amount.append(rem_slab["to"])
                                percentage.append(rem_slab["percent"])
                                difference.append(rem_slab["to"] - rem_slab["from"])
                                total_value.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount.append(slab["from"])
                            to_amount.append(slab["to"])
                            percentage.append(tax_percent)
                            difference.append(taxable_amount)
                            total_value.append(tax_amount)

                total_sum = sum(total_value)

                final_value = 0
                if (
                    income_doc.custom_marginal_relief_applicable
                    and income_doc.custom_minmum_value
                    and income_doc.custom_maximun_value
                ):
                    if (
                        income_doc.custom_minmum_value
                        < old_annual_slab
                        < income_doc.custom_maximun_value
                    ):
                        old_rebate_value = total_sum - (
                            old_annual_slab - income_doc.custom_minmum_value
                        )
                        final_value = total_sum - old_rebate_value

                        old_education_cess = final_value * 4 / 100

                    else:
                        if old_annual_slab < old_rebate:
                            old_rebate_value = total_sum

                        else:
                            old_rebate_value = 0

                        if old_annual_slab > 5000000:
                            old_surcharge_m = round((total_sum * 10) / 100)
                            old_education_cess = round(
                                (old_surcharge_m + total_sum) * 4 / 100
                            )

                        else:
                            old_surcharge_m = 0
                            old_education_cess = round((0 + total_sum) * 4 / 100)
                else:
                    if old_annual_slab < old_rebate:
                        old_rebate_value = total_sum

                    else:
                        old_rebate_value = 0

                    if old_annual_slab > 5000000:
                        old_surcharge_m = round((total_sum * 10) / 100)
                        old_education_cess = round(
                            (old_surcharge_m + total_sum) * 4 / 100
                        )

                    else:
                        old_surcharge_m = 0
                        old_education_cess = round((0 + total_sum) * 4 / 100)
            else:
                old_rebate_value = 0
                old_surcharge_m = 0
                old_education_cess = 0

    latest_tax_slab_new = frappe.get_list(
        "Income Tax Slab",
        filters={
            "company": company,
            "docstatus": 1,
            "disabled": 0,
            "custom_select_regime": "New Regime",
        },
        fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
        order_by="effective_from DESC",
        limit=1,
    )

    if latest_tax_slab_new:
        for slab_new in latest_tax_slab_new:
            income_doc_new = frappe.get_doc("Income Tax Slab", slab_new.name)

            # Initialize Lists
            total_value_new = []
            from_amount_new = []
            to_amount_new = []
            percentage_new = []
            difference_new = []
            total_array_new = []

            total_sum_new = 0  # Initialize early to avoid UnboundLocalError
            new_rebate_value = 0
            new_surcharge_m = 0
            new_education_cess = 0

            new_regime_marginal_relief_min_value = 0
            new_regime_marginal_relief_max_value = 0

            # Retrieve Exemption & Maximum Values
            new_rebate = income_doc_new.custom_taxable_income_is_less_than
            new_max_amount = income_doc_new.custom_maximum_amount

            if (
                income_doc_new.custom_marginal_relief_applicable
                and income_doc_new.custom_minmum_value
                and income_doc_new.custom_maximun_value
            ):
                new_regime_marginal_relief_min_value = (
                    income_doc_new.custom_minmum_value
                )
                new_regime_marginal_relief_max_value = (
                    income_doc_new.custom_maximun_value
                )

            if new_annual_slab > new_rebate:
                # Store all slab details in a structured list
                for i in income_doc_new.slabs:
                    total_array_new.append(
                        {
                            "from": i.from_amount,
                            "to": i.to_amount,
                            "percent": i.percent_deduction,
                        }
                    )

                for slab_new in total_array_new:
                    if slab_new["to"] == 0.0:  # Upper limit not defined
                        if round(new_annual_slab) >= slab_new["from"]:
                            taxable_amount_new = (
                                round(new_annual_slab) - slab_new["from"]
                            )
                            tax_percent_new = slab_new["percent"]
                            tax_amount_new = round(
                                (taxable_amount_new * tax_percent_new) / 100
                            )

                            remaining_slabs_new = [
                                s
                                for s in total_array_new
                                if s["from"] < slab_new["from"]
                            ]
                            for rem_slab in remaining_slabs_new:
                                from_amount_new.append(rem_slab["from"])
                                to_amount_new.append(rem_slab["to"])
                                percentage_new.append(rem_slab["percent"])
                                difference_new.append(rem_slab["to"] - rem_slab["from"])
                                total_value_new.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount_new.append(slab_new["from"])
                            to_amount_new.append(slab_new["to"])
                            percentage_new.append(tax_percent_new)
                            difference_new.append(taxable_amount_new)
                            total_value_new.append(tax_amount_new)

                    else:  # Standard slab range
                        if slab_new["from"] <= round(new_annual_slab) <= slab_new["to"]:
                            taxable_amount_new = (
                                round(new_annual_slab) - slab_new["from"]
                            )
                            tax_percent_new = slab_new["percent"]
                            tax_amount_new = round(
                                (taxable_amount_new * tax_percent_new) / 100
                            )

                            # Process lower slabs
                            remaining_slabs = [
                                s
                                for s in total_array_new
                                if s["from"] < slab_new["from"]
                            ]
                            for rem_slab in remaining_slabs:
                                from_amount_new.append(rem_slab["from"])
                                to_amount_new.append(rem_slab["to"])
                                percentage_new.append(rem_slab["percent"])
                                difference_new.append(rem_slab["to"] - rem_slab["from"])
                                total_value_new.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount_new.append(slab_new["from"])
                            to_amount_new.append(slab_new["to"])
                            percentage_new.append(tax_percent_new)
                            difference_new.append(taxable_amount_new)
                            total_value_new.append(tax_amount_new)

                total_sum_new = sum(total_value_new)

                if (
                    income_doc_new.custom_marginal_relief_applicable
                    and income_doc_new.custom_minmum_value
                    and income_doc_new.custom_maximun_value
                ):
                    if (
                        income_doc_new.custom_minmum_value
                        < new_annual_slab
                        < income_doc_new.custom_maximun_value
                    ):
                        new_rebate_value = total_sum_new - (
                            new_annual_slab - income_doc_new.custom_minmum_value
                        )
                        final_value = total_sum_new - new_rebate_value

                        new_education_cess = final_value * 4 / 100

                    else:
                        if new_annual_slab < new_rebate:
                            new_rebate_value = total_sum_new

                        else:
                            new_rebate_value = 0

                        if new_annual_slab > 5000000:
                            new_surcharge_m = round((total_sum_new * 10) / 100)
                            new_education_cess = round(
                                (new_surcharge_m + total_sum_new) * 4 / 100
                            )

                        else:
                            new_surcharge_m = 0
                            new_education_cess = round((0 + total_sum_new) * 4 / 100)

                else:
                    if new_annual_slab < new_rebate:
                        new_rebate_value = total_sum_new

                    else:
                        new_rebate_value = 0

                    if new_annual_slab > 5000000:
                        new_surcharge_m = round((total_sum_new * 10) / 100)
                        new_education_cess = round(
                            (new_surcharge_m + total_sum_new) * 4 / 100
                        )

                    else:
                        new_surcharge_m = 0
                        new_education_cess = round((0 + total_sum_new) * 4 / 100)

    tax_already_paid = 0

    get_all_salary_slip = frappe.get_list(
        "Salary Slip",
        filters={
            "employee": employee,
            "docstatus": ["in", [1]],
            "custom_payroll_period": payroll_period,
        },
        fields=["current_month_income_tax"],
    )


    tax_already_paid = round(sum(slip.current_month_income_tax for slip in get_all_salary_slip))

    return {
        "from_amount": from_amount,
        "to_amount": to_amount,
        "percentage": percentage,
        "total_value": total_value,
        "total_sum": total_sum,
        "rebate": old_rebate,
        "max_amount": old_max_amount,
        "old_rebate_value": old_rebate_value,
        "old_surcharge_m": old_surcharge_m,
        "old_education_cess": old_education_cess,
        "from_amount_new": from_amount_new,
        "to_amount_new": to_amount_new,
        "percentage_new": percentage_new,
        "total_value_new": total_value_new,
        "total_sum_new": total_sum_new,
        "rebate_new": new_rebate,
        "max_amount_new": new_max_amount,
        "new_regime_marginal_relief_min_value": new_regime_marginal_relief_min_value,
        "new_regime_marginal_relief_max_value": new_regime_marginal_relief_max_value,
        "old_regime_marginal_relief_min_value": old_regime_marginal_relief_min_value,
        "old_regime_marginal_relief_max_value": old_regime_marginal_relief_max_value,
        "new_rebate_value": new_rebate_value,
        "new_surcharge_m": new_surcharge_m,
        "new_education_cess": new_education_cess,
        "tax_already_paid": tax_already_paid,
    }
