import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
import json


def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [1]]}

    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    salary_structure_assignments = frappe.get_all(
        "Salary Structure Assignment",
        filters=conditions,
        fields=["*"],
        order_by="from_date desc",
    )

    latest_salary_structure = {}
    first_salary_structure = {}

    for structure in salary_structure_assignments:
        employee_id = structure["employee"]

        if (
            employee_id not in latest_salary_structure
            or structure["from_date"]
            > latest_salary_structure[employee_id]["from_date"]
        ):
            latest_salary_structure[employee_id] = structure

        if (
            employee_id not in first_salary_structure
            or structure["from_date"] < first_salary_structure[employee_id]["from_date"]
        ):
            first_salary_structure[employee_id] = structure

    unique_salary_structures = list(latest_salary_structure.values())
    first_unique_salary_structures = list(first_salary_structure.values())

    first_employee_details = [
        {
            "employee": item["employee"],
            "from_date": item["from_date"],
            "salary_structure": item["salary_structure"],
        }
        for item in first_unique_salary_structures
    ]

    salary_components = {}
    final_data = []

    epf_amount = 0
    pt_amount = 0
    pt_amount_prev = 0
    pt_amount_futu = 0

    epf_amount_prev = 0
    epf_amount_futu = 0

    for structure in unique_salary_structures:
        employee = frappe.get_value(
            "Employee",
            structure["employee"],
            ["pan_number", "personal_email", "company_email"],
            as_dict=True,
        )

        structure.update(employee)

        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={
                "employee": structure["employee"],
                "custom_payroll_period": structure["custom_payroll_period"],
                "docstatus": ["in", [0, 1]],
                "company": structure["company"],
            },
            fields=["name"],
        )

        salary_data = structure.copy()
        slip_count = len(salary_slips)
        new_total_income = 0
        old_total_income = 0

        if salary_slips:
            for slip in salary_slips:
                salary_slip_doc = frappe.get_doc("Salary Slip", slip["name"])
                for earning in salary_slip_doc.earnings:
                    get_each_component = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )
                    component_sequence = get_each_component.custom_sequence or 9999

                    if (
                        get_each_component.is_tax_applicable == 1
                        and get_each_component.type == "Earning"
                        and get_each_component.custom_tax_exemption_applicable_based_on_regime
                        == 1
                        and (get_each_component.custom_regime == "New Regime")
                    ):
                        salary_component = earning.salary_component
                        salary_components[salary_component] = component_sequence
                        salary_data[salary_component] = (
                            salary_data.get(salary_component, 0) + earning.amount
                        )
                        new_total_income += earning.amount

                    if (
                        get_each_component.is_tax_applicable == 1
                        and get_each_component.type == "Earning"
                        and get_each_component.custom_tax_exemption_applicable_based_on_regime
                        == 1
                        and (get_each_component.custom_regime == "All")
                    ):
                        salary_component = earning.salary_component
                        salary_components[salary_component] = component_sequence
                        salary_data[salary_component] = (
                            salary_data.get(salary_component, 0) + earning.amount
                        )
                        old_total_income += earning.amount
                        new_total_income += earning.amount

                for deduction in salary_slip_doc.deductions:
                    get_tax_component_ded = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    component_sequence = get_tax_component_ded.custom_sequence or 9999

                    if get_tax_component_ded.component_type == "EPF":
                        epf_amount_prev += deduction.amount

                    if get_tax_component_ded.component_type == "Professional Tax":
                        pt_amount_prev += deduction.amount
        # frappe.msgprint(str(epf_amount_prev))

        last_employee_detail = next(
            (
                d
                for d in first_employee_details
                if d["employee"] == structure["employee"]
            ),
            None,
        )

        if last_employee_detail:
            payroll_period_doc = frappe.get_doc(
                "Payroll Period", structure["custom_payroll_period"]
            )
            end_date = payroll_period_doc.end_date
            month_count = (
                (end_date.year - last_employee_detail["from_date"].year) * 12
                + (end_date.month - last_employee_detail["from_date"].month)
                + 1
            )

            salary_slip = make_salary_slip(
                source_name=last_employee_detail["salary_structure"],
                employee=structure["employee"],
                print_format="Salary Slip Standard",
                posting_date=last_employee_detail["from_date"],
                for_preview=1,
            )

            processed_components = set()

            for projection_earning in salary_slip.earnings:
                get_tax_component = frappe.get_doc(
                    "Salary Component", projection_earning.salary_component
                )

                if get_tax_component.name in processed_components:
                    continue

                if (
                    get_tax_component.is_tax_applicable == 1
                    and get_tax_component.custom_component_category == "Fixed"
                    and get_tax_component.type == "Earning"
                    and get_tax_component.custom_tax_exemption_applicable_based_on_regime
                    == 1
                    and (get_tax_component.custom_regime == "New Regime")
                ):
                    salary_component = projection_earning.salary_component
                    projected_income = projection_earning.amount * (
                        month_count - slip_count
                    )
                    salary_data[salary_component] = (
                        salary_data.get(salary_component, 0) + projected_income
                    )
                    new_total_income += projected_income

                if (
                    get_tax_component.is_tax_applicable == 1
                    and get_tax_component.custom_component_category == "Fixed"
                    and get_tax_component.type == "Earning"
                    and get_tax_component.custom_tax_exemption_applicable_based_on_regime
                    == 1
                    and (get_tax_component.custom_regime == "All")
                ):
                    salary_component = projection_earning.salary_component
                    projected_income = projection_earning.amount * (
                        month_count - slip_count
                    )
                    salary_data[salary_component] = (
                        salary_data.get(salary_component, 0) + projected_income
                    )
                    old_total_income += projected_income
                    new_total_income += projected_income

                processed_components.add(get_tax_component.name)

            for projection_deduction in salary_slip.deductions:
                get_tax_component_ded = frappe.get_doc(
                    "Salary Component", projection_deduction.salary_component
                )
                if get_tax_component_ded.name in processed_components:
                    continue

                if (
                    get_tax_component_ded.component_type == "EPF"
                    and get_tax_component_ded.custom_component_category == "Fixed"
                ):
                    epf_amount_futu = projection_deduction.amount * (
                        month_count - slip_count
                    )

                if (
                    get_tax_component_ded.component_type == "Professional Tax"
                    and get_tax_component_ded.custom_component_category == "Fixed"
                ):
                    pt_amount_futu = projection_deduction.amount * (
                        month_count - slip_count
                    )
                processed_components.add(get_tax_component_ded.name)

        # frappe.msgprint(str(epf_amount_futu))

        epf_amount = min(epf_amount_futu + epf_amount_prev, 150000)

        # frappe.msgprint(str(epf_amount))

        pt_amount = min(pt_amount_futu + pt_amount_prev, 2400)

        start_date = frappe.utils.getdate(payroll_period_doc.start_date)

        loan_repayments = frappe.get_list(
            "Loan Repayment Schedule",
            filters={
                "custom_employee": structure["employee"],
                "status": "Active",
                "docstatus": 1,
            },
            fields=["*"],
        )

        loan_perquisite_total = 0
        if loan_repayments:
            for repayment in loan_repayments:
                loan_doc = frappe.get_doc("Loan Repayment Schedule", repayment.name)
                for date in loan_doc.custom_loan_perquisite:
                    payment_date = frappe.utils.getdate(date.payment_date)
                    if start_date <= payment_date <= end_date:
                        loan_perquisite_total += date.perquisite_amount

        salary_data["loan_perquisite"] = loan_perquisite_total
        salary_data["new_total_income"] = new_total_income + loan_perquisite_total
        salary_data["old_total_income"] = old_total_income + loan_perquisite_total

        # Fetch Tax Exemption Declaration
        declaration = frappe.get_all(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": structure["employee"],
                "payroll_period": structure["custom_payroll_period"],
                "docstatus": 1,
            },
            fields=["name"],
        )

        if declaration:
            get_doc = frappe.get_doc(
                "Employee Tax Exemption Declaration", declaration[0].name
            )

            if get_doc.custom_tax_regime == "New Regime":
                get_tax_slab = frappe.get_doc(
                    "Income Tax Slab", get_doc.custom_income_tax
                )

                standard_deduction_new = get_tax_slab.standard_tax_exemption_amount or 0

                form_data = json.loads(get_doc.custom_declaration_form_data or "{}")
                nps_deduction = form_data.get("nineNumber", 0)
                total = nps_deduction + standard_deduction_new

                salary_data["standard_deduction_new"] = standard_deduction_new
                salary_data["standard_deduction_old"] = 50000
                salary_data["nps_deduction"] = nps_deduction
                salary_data["new_total_deduction"] = (
                    nps_deduction + standard_deduction_new
                )

                salary_data["tax_on_employment"] = pt_amount

                salary_data["pf_auto"] = epf_amount

                salary_data["old_total_deduction"] = (
                    50000 + epf_amount + pt_amount + nps_deduction
                )

                salary_data["new_annual_taxable_income"] = max(
                    new_total_income - total, 0
                )
                salary_data["old_annual_taxable_income"] = max(
                    old_total_income - (50000 + epf_amount + pt_amount + nps_deduction),
                    0,
                )

                new_annual_taxable_income_value = max(new_total_income - total, 0)
                old_annual_taxable_income_value = max(
                    old_total_income - (50000 + epf_amount + pt_amount + nps_deduction),
                    0,
                )

                latest_tax_slab = frappe.get_list(
                    "Income Tax Slab",
                    filters={
                        "company": get_doc.company,
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

                        old_rebate = income_doc.custom_taxable_income_is_less_than
                        old_max_amount = income_doc.custom_maximum_amount

                        if old_annual_taxable_income_value > old_rebate:
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
                                    if (
                                        round(old_annual_taxable_income_value)
                                        >= slab["from"]
                                    ):
                                        taxable_amount = (
                                            round(old_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent = slab["percent"]
                                        tax_amount = round(
                                            (taxable_amount * tax_percent) / 100
                                        )

                                        remaining_slabs = [
                                            s
                                            for s in total_array
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs:
                                            from_amount.append(rem_slab["from"])
                                            to_amount.append(rem_slab["to"])
                                            percentage.append(rem_slab["percent"])
                                            difference.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
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
                                    if (
                                        slab["from"]
                                        <= round(old_annual_taxable_income_value)
                                        <= slab["to"]
                                    ):
                                        taxable_amount = (
                                            round(old_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent = slab["percent"]
                                        tax_amount = round(
                                            (taxable_amount * tax_percent) / 100
                                        )

                                        remaining_slabs = [
                                            s
                                            for s in total_array
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs:
                                            from_amount.append(rem_slab["from"])
                                            to_amount.append(rem_slab["to"])
                                            percentage.append(rem_slab["percent"])
                                            difference.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
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

                            # Compute the total tax

                            total_sum = sum(total_value)

                            # frappe.msgprint(str(total_sum))

                            if old_annual_taxable_income_value < old_rebate:
                                old_rebate_value = total_sum
                            else:
                                old_rebate_value = 0

                            if old_annual_taxable_income_value > 5000000:
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
                        "company": get_doc.company,
                        "docstatus": 1,
                        "disabled": 0,
                        "custom_select_regime": "New Regime",
                    },
                    fields=[
                        "name",
                        "custom_select_regime",
                        "standard_tax_exemption_amount",
                    ],
                    order_by="effective_from DESC",
                    limit=1,
                )

                if latest_tax_slab_new:
                    for slab_new in latest_tax_slab_new:
                        income_doc_new = frappe.get_doc(
                            "Income Tax Slab", slab_new.name
                        )

                        # Initialize Lists
                        total_value_new = []
                        from_amount_new = []
                        to_amount_new = []
                        percentage_new = []
                        difference_new = []
                        total_array_new = []

                        total_sum_new = 0
                        new_rebate_value = 0
                        new_surcharge_m = 0
                        new_education_cess = 0
                        new_regime_tax_payable = 0

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

                        if new_annual_taxable_income_value > new_rebate:
                            for i in income_doc_new.slabs:
                                total_array_new.append(
                                    {
                                        "from": i.from_amount,
                                        "to": i.to_amount,
                                        "percent": i.percent_deduction,
                                    }
                                )

                            for slab in total_array_new:
                                if slab["to"] == 0.0:
                                    if (
                                        round(new_annual_taxable_income_value)
                                        >= slab["from"]
                                    ):
                                        taxable_amount_new = (
                                            round(new_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent_new = slab["percent"]
                                        tax_amount_new = round(
                                            (taxable_amount_new * tax_percent_new) / 100
                                        )

                                        remaining_slabs_new = [
                                            s
                                            for s in total_array_new
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs_new:
                                            from_amount_new.append(rem_slab["from"])
                                            to_amount_new.append(rem_slab["to"])
                                            percentage_new.append(rem_slab["percent"])
                                            difference_new.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
                                            total_value_new.append(
                                                round(
                                                    (rem_slab["to"] - rem_slab["from"])
                                                    * rem_slab["percent"]
                                                    / 100
                                                )
                                            )

                                        from_amount_new.append(slab["from"])
                                        to_amount_new.append(slab["to"])
                                        percentage_new.append(tax_percent_new)
                                        difference_new.append(taxable_amount_new)
                                        total_value_new.append(tax_amount_new)

                                else:
                                    if (
                                        slab["from"]
                                        <= round(new_annual_taxable_income_value)
                                        <= slab["to"]
                                    ):
                                        taxable_amount_new = (
                                            round(new_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent_new = slab["percent"]
                                        tax_amount_new = round(
                                            (taxable_amount_new * tax_percent_new) / 100
                                        )

                                        remaining_slabs_new = [
                                            s
                                            for s in total_array_new
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs_new:
                                            from_amount_new.append(rem_slab["from"])
                                            to_amount_new.append(rem_slab["to"])
                                            percentage_new.append(rem_slab["percent"])
                                            difference_new.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
                                            total_value_new.append(
                                                round(
                                                    (rem_slab["to"] - rem_slab["from"])
                                                    * rem_slab["percent"]
                                                    / 100
                                                )
                                            )

                                        from_amount_new.append(slab["from"])
                                        to_amount_new.append(slab["to"])
                                        percentage_new.append(tax_percent_new)
                                        difference_new.append(taxable_amount_new)
                                        total_value_new.append(tax_amount_new)

                            # Compute the total tax
                            total_sum_new = sum(total_value_new)

                            if (
                                income_doc_new.custom_marginal_relief_applicable
                                and income_doc_new.custom_minmum_value
                                and income_doc_new.custom_maximun_value
                            ):
                                if (
                                    income_doc_new.custom_minmum_value
                                    < new_annual_taxable_income_value
                                    < income_doc_new.custom_maximun_value
                                ):
                                    new_rebate_value = total_sum_new - (
                                        new_annual_taxable_income_value
                                        - income_doc_new.custom_minmum_value
                                    )
                                    final_value = total_sum_new - new_rebate_value

                                    new_education_cess = final_value * 4 / 100

                                    new_regime_tax_payable = (
                                        final_value + new_education_cess
                                    )

                                else:
                                    if new_annual_taxable_income_value < new_rebate:
                                        new_rebate_value = total_sum_new

                                    else:
                                        new_rebate_value = 0

                                    if new_annual_taxable_income_value > 5000000:
                                        new_surcharge_m = round(
                                            (total_sum_new * 10) / 100
                                        )
                                        new_education_cess = round(
                                            (new_surcharge_m + total_sum_new) * 4 / 100
                                        )

                                    else:
                                        new_surcharge_m = 0
                                        new_education_cess = round(
                                            (0 + total_sum_new) * 4 / 100
                                        )

                                    new_regime_tax_payable = (
                                        total_sum_new
                                        + new_surcharge_m
                                        + new_education_cess
                                    )

                            else:
                                if new_annual_taxable_income_value < new_rebate:
                                    new_rebate_value = total_sum_new
                                else:
                                    new_rebate_value = 0

                                if new_annual_taxable_income_value > 5000000:
                                    new_surcharge_m = round((total_sum_new * 10) / 100)
                                    new_education_cess = round(
                                        (new_surcharge_m + total_sum_new) * 4 / 100
                                    )
                                else:
                                    new_surcharge_m = 0
                                    new_education_cess = round(
                                        (0 + total_sum_new) * 4 / 100
                                    )

                        else:
                            new_rebate_value = 0
                            new_surcharge_m = 0
                            new_education_cess = 0

                salary_data["total_sum"] = total_sum
                salary_data["old_rebate_value"] = old_rebate_value
                salary_data["old_surcharge_m"] = old_surcharge_m
                salary_data["old_education_cess"] = old_education_cess

                salary_data["old_regime_tax_payable"] = (
                    total_sum + old_surcharge_m + old_education_cess
                )

                salary_data["total_sum_new"] = total_sum_new
                salary_data["new_rebate_value"] = new_rebate_value
                salary_data["new_surcharge_m"] = new_surcharge_m
                salary_data["new_education_cess"] = new_education_cess

                salary_data["new_regime_tax_payable"] = new_regime_tax_payable

            if get_doc.custom_tax_regime == "Old Regime":
                get_tax_slab = frappe.get_doc(
                    "Income Tax Slab", get_doc.custom_income_tax
                )
                standard_deduction_old = get_tax_slab.standard_tax_exemption_amount or 0

                hra_exemption = get_doc.annual_hra_exemption

                form_data = json.loads(get_doc.custom_declaration_form_data or "{}")

                lta_map = form_data.get("twentyeight", 0)
                education_allowance_map = form_data.get("thirteen", 0)
                hostel_allowance_map = form_data.get("twentysix", 0)
                uniform_allowance_map = form_data.get("twentyFour", 0)

                pt_map = form_data.get("nineteenNumber", 0)

                pf_auto_map = form_data.get("pfValue", 0)

                nps_deduction = form_data.get("nineNumber", 0)

                pension_scheme_map = form_data.get("aValue2", 0)
                housing_loan = form_data.get("bValue1", 0)
                ppf = form_data.get("amount4", 0)
                home_loan = form_data.get("dValue1", 0)

                lic = form_data.get("eValue1", 0)
                nsc = form_data.get("fValue1", 0)
                mutual_fund = form_data.get("gValue1", 0)
                elss = form_data.get("hValue1", 0)
                tuition = form_data.get("iValue1", 0)

                fixed_deposit = form_data.get("jValue1", 0)
                deposit = form_data.get("kValue1", 0)
                others = form_data.get("kValue2", 0)

                mediclaim_self = form_data.get("amount", 0)
                mediclaim_self_senior = form_data.get("amount3", 0)
                mediclaim_parents_below = form_data.get("mpAmount3", 0)
                mediclaim_parents_senior = form_data.get("mpAmount4", 0)
                preventive_health_checkup = form_data.get("mp5", 0)
                preventive_health_checkup_self = form_data.get("mpAmount6", 0)

                total_80d_eligible = form_data.get("amount_80d_eligible_amount", 0)

                medical_treatment_insurance = form_data.get("fourValue", 0)
                medical_treatment_disease = form_data.get("fiveNumber", 0)
                interest_repayment = form_data.get("sixNumber", 0)
                physical_disabled = form_data.get("sevenNumber", 0)
                donation_80g = form_data.get("eightNumber", 0)

                hsg = form_data.get("tenNumber", 0)
                nps_contribution = form_data.get("elevenNumber", 0)
                tax_incentive = form_data.get("twelveNumber1", 0)
                tax_incentive_eeb = form_data.get("fifteenNumber", 0)
                dona_political_party = form_data.get("sixteenNumber", 0)
                interest_saving_account = form_data.get("seventeenNumber", 0)
                interest_fd = form_data.get("eighteenNumber", 0)

                deduction_80gg = form_data.get("twentyNumber", 0)
                regime_80ccg = form_data.get("twentyoneNumber", 0)

                total = (
                    regime_80ccg
                    + deduction_80gg
                    + interest_fd
                    + interest_saving_account
                    + nps_deduction
                    + standard_deduction_old
                    + tax_incentive_eeb
                    + tax_incentive
                    + nps_contribution
                    + hsg
                    + donation_80g
                    + physical_disabled
                    + interest_repayment
                    + medical_treatment_disease
                    + medical_treatment_insurance
                    + total_80d_eligible
                    + deposit
                    + fixed_deposit
                    + tuition
                    + elss
                    + mutual_fund
                    + nsc
                    + lic
                    + home_loan
                    + ppf
                    + housing_loan
                    + pension_scheme_map
                    + pf_auto_map
                    + pt_map
                    + uniform_allowance_map
                    + hostel_allowance_map
                    + education_allowance_map
                    + lta_map
                    + hra_exemption
                )

                salary_data["standard_deduction_old"] = standard_deduction_old
                salary_data["standard_deduction_new"] = 75000

                salary_data["hra_exemption"] = hra_exemption
                salary_data["lta"] = lta_map
                salary_data["education_allowance_exemption"] = education_allowance_map
                salary_data["hostel_allowance_exemption"] = hostel_allowance_map
                salary_data["uniform_allowance_exemption"] = uniform_allowance_map
                salary_data["tax_on_employment"] = pt_map

                salary_data["pf_auto"] = pf_auto_map

                salary_data["pension_scheme"] = pension_scheme_map
                salary_data["housing_loan"] = housing_loan
                salary_data["ppf"] = ppf
                salary_data["home_loan"] = home_loan

                salary_data["lic"] = lic
                salary_data["nsc"] = nsc
                salary_data["mutual_fund"] = mutual_fund
                salary_data["elss"] = elss
                salary_data["tuition"] = tuition
                salary_data["fixed_deposit"] = fixed_deposit
                salary_data["deposit"] = deposit
                salary_data["others"] = others

                salary_data["mediclaim_self"] = mediclaim_self
                salary_data["mediclaim_self_senior"] = mediclaim_self_senior
                salary_data["mediclaim_parents_below"] = mediclaim_parents_below
                salary_data["mediclaim_parents_senior"] = mediclaim_parents_senior
                salary_data["preventive_health_checkup"] = preventive_health_checkup
                salary_data[
                    "preventive_health_checkup_self"
                ] = preventive_health_checkup_self

                salary_data["medical_treatment_insurance"] = medical_treatment_insurance
                salary_data["medical_treatment_disease"] = medical_treatment_disease
                salary_data["interest_repayment"] = interest_repayment
                salary_data["physical_disabled"] = physical_disabled
                salary_data["donation_80g"] = donation_80g

                salary_data["nps_deduction"] = nps_deduction
                salary_data["hsg"] = hsg
                salary_data["nps_contribution"] = nps_contribution
                salary_data["tax_incentive"] = tax_incentive
                salary_data["tax_incentive_eeb"] = tax_incentive_eeb
                salary_data["dona_political_party"] = dona_political_party
                salary_data["interest_saving_account"] = interest_saving_account
                salary_data["interest_fd"] = interest_fd
                salary_data["deduction_80gg"] = deduction_80gg
                salary_data["regime_80ccg"] = regime_80ccg

                salary_data["old_total_deduction"] = total

                salary_data["new_total_deduction"] = nps_deduction + 75000

                salary_data["old_annual_taxable_income"] = round(
                    (old_total_income - total)
                )

                salary_data["new_annual_taxable_income"] = max(
                    new_total_income - nps_deduction - 75000, 0
                )

                new_annual_taxable_income_value = max(
                    new_total_income - nps_deduction - 75000, 0
                )
                old_annual_taxable_income_value = max((old_total_income - total), 0)

                latest_tax_slab = frappe.get_list(
                    "Income Tax Slab",
                    filters={
                        "company": get_doc.company,
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

                        old_rebate = income_doc.custom_taxable_income_is_less_than
                        old_max_amount = income_doc.custom_maximum_amount

                        if old_annual_taxable_income_value > old_rebate:
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
                                    if (
                                        round(old_annual_taxable_income_value)
                                        >= slab["from"]
                                    ):
                                        taxable_amount = (
                                            round(old_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent = slab["percent"]
                                        tax_amount = round(
                                            (taxable_amount * tax_percent) / 100
                                        )

                                        remaining_slabs = [
                                            s
                                            for s in total_array
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs:
                                            from_amount.append(rem_slab["from"])
                                            to_amount.append(rem_slab["to"])
                                            percentage.append(rem_slab["percent"])
                                            difference.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
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
                                    if (
                                        slab["from"]
                                        <= round(old_annual_taxable_income_value)
                                        <= slab["to"]
                                    ):
                                        taxable_amount = (
                                            round(old_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent = slab["percent"]
                                        tax_amount = round(
                                            (taxable_amount * tax_percent) / 100
                                        )

                                        # Process lower slabs
                                        remaining_slabs = [
                                            s
                                            for s in total_array
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs:
                                            from_amount.append(rem_slab["from"])
                                            to_amount.append(rem_slab["to"])
                                            percentage.append(rem_slab["percent"])
                                            difference.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
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

                            # Compute the total tax
                            total_sum = sum(total_value)

                            if old_annual_taxable_income_value < old_rebate:
                                old_rebate_value = total_sum
                            else:
                                old_rebate_value = 0

                            if old_annual_taxable_income_value > 5000000:
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
                        "company": get_doc.company,
                        "docstatus": 1,
                        "disabled": 0,
                        "custom_select_regime": "New Regime",
                    },
                    fields=[
                        "name",
                        "custom_select_regime",
                        "standard_tax_exemption_amount",
                    ],
                    order_by="effective_from DESC",
                    limit=1,
                )

                if latest_tax_slab_new:
                    for slab_new in latest_tax_slab_new:
                        income_doc_new = frappe.get_doc(
                            "Income Tax Slab", slab_new.name
                        )

                        # Initialize Lists
                        total_value_new = []
                        from_amount_new = []
                        to_amount_new = []
                        percentage_new = []
                        difference_new = []
                        total_array_new = []

                        total_sum_new = 0
                        new_rebate_value = 0
                        new_surcharge_m = 0
                        new_education_cess = 0
                        new_regime_tax_payable = 0

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

                        if new_annual_taxable_income_value > new_rebate:
                            for i in income_doc_new.slabs:
                                total_array_new.append(
                                    {
                                        "from": i.from_amount,
                                        "to": i.to_amount,
                                        "percent": i.percent_deduction,
                                    }
                                )

                            for slab in total_array_new:
                                if slab["to"] == 0.0:
                                    if (
                                        round(new_annual_taxable_income_value)
                                        >= slab["from"]
                                    ):
                                        taxable_amount_new = (
                                            round(new_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent_new = slab["percent"]
                                        tax_amount_new = round(
                                            (taxable_amount_new * tax_percent_new) / 100
                                        )

                                        remaining_slabs_new = [
                                            s
                                            for s in total_array_new
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs_new:
                                            from_amount_new.append(rem_slab["from"])
                                            to_amount_new.append(rem_slab["to"])
                                            percentage_new.append(rem_slab["percent"])
                                            difference_new.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
                                            total_value_new.append(
                                                round(
                                                    (rem_slab["to"] - rem_slab["from"])
                                                    * rem_slab["percent"]
                                                    / 100
                                                )
                                            )

                                        from_amount_new.append(slab["from"])
                                        to_amount_new.append(slab["to"])
                                        percentage_new.append(tax_percent_new)
                                        difference_new.append(taxable_amount_new)
                                        total_value_new.append(tax_amount_new)

                                else:
                                    if (
                                        slab["from"]
                                        <= round(new_annual_taxable_income_value)
                                        <= slab["to"]
                                    ):
                                        taxable_amount_new = (
                                            round(new_annual_taxable_income_value)
                                            - slab["from"]
                                        )
                                        tax_percent_new = slab["percent"]
                                        tax_amount_new = round(
                                            (taxable_amount_new * tax_percent_new) / 100
                                        )

                                        remaining_slabs_new = [
                                            s
                                            for s in total_array_new
                                            if s["from"] < slab["from"]
                                        ]
                                        for rem_slab in remaining_slabs_new:
                                            from_amount_new.append(rem_slab["from"])
                                            to_amount_new.append(rem_slab["to"])
                                            percentage_new.append(rem_slab["percent"])
                                            difference_new.append(
                                                rem_slab["to"] - rem_slab["from"]
                                            )
                                            total_value_new.append(
                                                round(
                                                    (rem_slab["to"] - rem_slab["from"])
                                                    * rem_slab["percent"]
                                                    / 100
                                                )
                                            )

                                        from_amount_new.append(slab["from"])
                                        to_amount_new.append(slab["to"])
                                        percentage_new.append(tax_percent_new)
                                        difference_new.append(taxable_amount_new)
                                        total_value_new.append(tax_amount_new)

                            # Compute the total tax
                            total_sum_new = sum(total_value_new)

                            if (
                                income_doc_new.custom_marginal_relief_applicable
                                and income_doc_new.custom_minmum_value
                                and income_doc_new.custom_maximun_value
                            ):
                                if (
                                    income_doc_new.custom_minmum_value
                                    < new_annual_taxable_income_value
                                    < income_doc_new.custom_maximun_value
                                ):
                                    new_rebate_value = total_sum_new - (
                                        new_annual_taxable_income_value
                                        - income_doc_new.custom_minmum_value
                                    )
                                    final_value = total_sum_new - new_rebate_value

                                    new_education_cess = final_value * 4 / 100

                                    new_regime_tax_payable = (
                                        final_value + new_education_cess
                                    )

                                else:
                                    if new_annual_taxable_income_value < new_rebate:
                                        new_rebate_value = total_sum_new

                                    else:
                                        new_rebate_value = 0

                                    if new_annual_taxable_income_value > 5000000:
                                        new_surcharge_m = round(
                                            (total_sum_new * 10) / 100
                                        )
                                        new_education_cess = round(
                                            (new_surcharge_m + total_sum_new) * 4 / 100
                                        )

                                    else:
                                        new_surcharge_m = 0
                                        new_education_cess = round(
                                            (0 + total_sum_new) * 4 / 100
                                        )

                                    new_regime_tax_payable = (
                                        total_sum_new
                                        + new_education_cess
                                        + new_surcharge_m
                                    )

                            else:
                                if new_annual_taxable_income_value < new_rebate:
                                    new_rebate_value = total_sum_new
                                else:
                                    new_rebate_value = 0

                                if new_annual_taxable_income_value > 5000000:
                                    new_surcharge_m = round((total_sum_new * 10) / 100)
                                    new_education_cess = round(
                                        (new_surcharge_m + total_sum_new) * 4 / 100
                                    )
                                else:
                                    new_surcharge_m = 0
                                    new_education_cess = round(
                                        (0 + total_sum_new) * 4 / 100
                                    )

                        else:
                            new_rebate_value = 0
                            new_surcharge_m = 0
                            new_education_cess = 0

                salary_data["total_sum"] = total_sum
                salary_data["old_rebate_value"] = old_rebate_value
                salary_data["old_surcharge_m"] = old_surcharge_m
                salary_data["old_education_cess"] = old_education_cess

                salary_data["old_regime_tax_payable"] = (
                    total_sum + old_surcharge_m + old_education_cess
                )

                salary_data["total_sum_new"] = total_sum_new
                salary_data["new_rebate_value"] = new_rebate_value
                salary_data["new_surcharge_m"] = new_surcharge_m
                salary_data["new_education_cess"] = new_education_cess

                salary_data["new_regime_tax_payable"] = new_regime_tax_payable

            new_regime_payable = max((new_regime_tax_payable), 0)

            old_regime_payable = max(
                (total_sum + old_surcharge_m + old_education_cess), 0
            )

            get_all_salary_slip = frappe.get_list(
                "Salary Slip",
                filters={
                    "employee": get_doc.employee,
                    "docstatus": ["in", [1]],
                    "custom_payroll_period": get_doc.payroll_period,
                },
                fields=["current_month_income_tax"],  # Fetch only the required field
            )

            salary_slip_sum = sum(
                slip.current_month_income_tax for slip in get_all_salary_slip
            )

            salary_data["tax_paid"] = salary_slip_sum

            salary_data["new_regime_tax"] = new_regime_payable / month_count
            salary_data["old_regime_tax"] = old_regime_payable / month_count

            new_regime_tax_amount = new_regime_payable / month_count
            old_regime_tax_amount = old_regime_payable / month_count

            beneficial = min(new_regime_tax_amount, old_regime_tax_amount)

            beneficial_max = max(new_regime_payable, old_regime_payable)
            beneficial_min = min(new_regime_payable, old_regime_payable)

            final_beneficial = None

            if beneficial == new_regime_tax_amount:
                final_beneficial = "New Regime"
            else:
                final_beneficial = "Old Regime"

            salary_data["final_beneficial"] = final_beneficial

            difference = beneficial_max - beneficial_min

            salary_data["difference"] = difference

        final_data.append(salary_data)

    return final_data, salary_components


def execute(filters=None):
    columns = [
        {
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 120,
        },
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 150},
        {
            "label": "Payroll Period",
            "fieldname": "custom_payroll_period",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Effective From Date",
            "fieldname": "from_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Joining Date",
            "fieldname": "custom_date_of_joining",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Opted Slab",
            "fieldname": "custom_tax_regime",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Designation",
            "fieldname": "designation",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "PAN Number",
            "fieldname": "pan_number",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Personal Email",
            "fieldname": "personal_email",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": "Company Email",
            "fieldname": "company_email",
            "fieldtype": "Data",
            "width": 200,
        },
    ]

    data, salary_components = get_salary_slips(filters)

    # sorted_components = sorted(salary_components.items(), key=lambda x: x[1])
    sorted_components = sorted(
        salary_components.items(),
        key=lambda x: x[1] if isinstance(x[1], (int, float)) else 9999,
    )

    for component, _ in sorted_components:
        columns.append(
            {
                "label": component,
                "fieldname": component,
                "fieldtype": "Currency",
                "width": 120,
            }
        )

    columns.extend(
        [
            {
                "label": "Loan Perquisite",
                "fieldname": "loan_perquisite",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "New Regime Total Income",
                "fieldname": "new_total_income",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "Old Regime Total Income",
                "fieldname": "old_total_income",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "HRA Exemption",
                "fieldname": "hra_exemption",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "fieldname": "lta",
                "label": "LTA  U/s 10 (5)",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "fieldname": "education_allowance_exemption",
                "label": "Education Allowance Exemption",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "hostel_allowance_exemption",
                "label": "Hostel Allowances Exemption",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "uniform_allowance_exemption",
                "label": "Uniform Allowance Exemption",
                "fieldtype": "Currency",
                "width": 120,
            },
            # Standard Deduction Columns
            {
                "fieldname": "standard_deduction_old",
                "label": "Standard Deduction Old Regime",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "standard_deduction_new",
                "label": "Standard Deduction New Regime",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tax_on_employment",
                "label": "Tax on Employment",
                "fieldtype": "Currency",
                "width": 120,
            },
            # 80C Columns
            {
                "label": "Investments In PF(Auto)",
                "fieldname": "pf_auto",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Pension Scheme Investments & ULIP",
                "fieldname": "pension_scheme",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Housing Loan Principal Repayment",
                "fieldname": "housing_loan",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "PPF - Public Provident Fund",
                "fieldname": "ppf",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Home Loan Account Of National Housing Bank",
                "fieldname": "home_loan",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "LIC- Life Insurance Premium Directly Paid By Employee",
                "fieldname": "lic",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "NSC - National Saving Certificate",
                "fieldname": "nsc",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "Mutual Funds - Notified Under Clause 23D Of Section 10",
                "fieldname": "mutual_fund",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": "ELSS - Equity Link Saving Scheme Of Mutual Funds",
                "fieldname": "elss",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tuition",
                "label": "Tuition Fees For Full Time Education",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "fixed_deposit",
                "label": "Fixed Deposits In Banks (Period As Per Income Tax Guidelines)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "deposit",
                "label": "5 Years Term Deposit An Account Under Post Office Term Deposit Rules",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "others",
                "label": "Others",
                "fieldtype": "Currency",
                "width": 120,
            },
            # 80D Columns
            {
                "fieldname": "mediclaim_self",
                "label": "Mediclaim Self, Spouse & Children (Below 60 years)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "mediclaim_self_senior",
                "label": "Mediclaim Self (Senior Citizen - 60 years & above)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "mediclaim_parents_below",
                "label": "Mediclaim Parents (Below 60 years)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "mediclaim_parents_senior",
                "label": "Mediclaim Parents (Senior Citizen - 60 years & above)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "preventive_health_checkup",
                "label": "Preventive Health Check-up for Parents",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "preventive_health_checkup_self",
                "label": "Preventive Health Check-up",
                "fieldtype": "Currency",
                "width": 120,
            },
            # 80DD and Other Columns
            {
                "fieldname": "medical_treatment_insurance",
                "label": "Medical treatment / insurance of handicapped dependant",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "medical_treatment_disease",
                "label": "Medical treatment (specified diseases only)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "interest_repayment",
                "label": "Interest repayment of Loan for higher education",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "physical_disabled",
                "label": "Deduction for Physically Disabled",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "donation_80g",
                "label": "Donation U/S 80G",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "nps_deduction",
                "label": "NPS Deduction U/S 80CCD(2)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "hsg",
                "label": "First HSG Loan Interest Ded.(80EE)",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "nps_contribution",
                "label": "Contribution in National Pension Scheme",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tax_incentive",
                "label": "Tax Incentive for Affordable Housing for Ded U/S 80EEA",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "tax_incentive_eeb",
                "label": "Tax Incentives for Electric Vehicles for Ded U/S 80EEB",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "dona_political_party",
                "label": "Donations/contribution made to a political party or an electoral trust",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "interest_saving_account",
                "label": "Interest on deposits in saving account for Ded U/S 80TTA",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "interest_fd",
                "label": "Interest on deposits in saving account for Ded U/S 80TTB",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "deduction_80gg",
                "label": "Deduction U/S 80GG",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "fieldname": "regime_80ccg",
                "label": "Rajiv Gandhi Equity Saving Scheme 80CCG",
                "fieldtype": "Currency",
                "width": 120,
            },
            # Final Columns
            {
                "fieldname": "new_total_deduction",
                "label": "Total Deduction/Exemptions(New Regime)",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "old_total_deduction",
                "label": "Total Deduction/Exemptions(Old Regime)",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "old_annual_taxable_income",
                "label": "Old Annual Taxable Income",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "new_annual_taxable_income",
                "label": "New Annual Taxable Income",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "total_sum",
                "label": "Old Regime Tax on total Income ",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "old_rebate_value",
                "label": "Old Regime Rebate",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "old_surcharge_m",
                "label": "Old Regime Surcharge",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "old_education_cess",
                "label": "Old Regime Education Cess",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "old_regime_tax_payable",
                "label": "Old Regime Tax payable",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "total_sum_new",
                "label": "New Regime Tax on total Income ",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "new_rebate_value",
                "label": "New Regime Rebate",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "new_surcharge_m",
                "label": "New Regime Surcharge",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "new_education_cess",
                "label": "New Regime Education Cess",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "new_regime_tax_payable",
                "label": "New Regime Tax payable",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "tax_paid",
                "label": "Tax Paid",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "new_regime_tax",
                "label": "New Regime Tax",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "old_regime_tax",
                "label": "Old Regime Tax",
                "fieldtype": "Currency",
                "width": 250,
            },
            {
                "fieldname": "final_beneficial",
                "label": "Beneficial",
                "fieldtype": "Data",
                "width": 250,
            },
            {
                "fieldname": "difference",
                "label": "Difference between old and new tax payable",
                "fieldtype": "Currency",
                "width": 250,
            },
        ]
    )

    return columns, data
