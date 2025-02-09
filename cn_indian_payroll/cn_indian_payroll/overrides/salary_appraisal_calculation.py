import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

@frappe.whitelist()
def appraisal_calculation(promotion_id, employee_id, company, date, effective_from):
    
    if promotion_id:
        old_amounts = {}
        new_amounts = {}


        old_bonus={}
        new_bonus={}

        
        # Fetch salary structure assignments (limit 2, most recent first)
        salary_structure_assignment = frappe.get_list('Salary Structure Assignment',
            filters={'employee': employee_id, 'company': company, 'docstatus': 1},
            fields=['*'],
            order_by='from_date desc',
            limit=2
        )

        # If fewer than 2 salary structures are found, return error
        if len(salary_structure_assignment) < 2:
            frappe.throw("Unable to find enough salary structure assignments for comparison.")
        
        # Get new salary slip
        new_salary_slip = make_salary_slip(
            source_name=salary_structure_assignment[0].salary_structure,
            employee=employee_id,
            print_format='Salary Slip Standard for CTC',  
            posting_date=salary_structure_assignment[0].from_date  
        )
        
        # Collect new amounts from earnings and deductions
        for new_earning in new_salary_slip.earnings:
            part_of_ctc = frappe.get_doc("Salary Component", new_earning.salary_component)
            if part_of_ctc.custom_is_part_of_appraisal == 1:
                component = new_earning.salary_component
                new_amounts[component] = new_earning.amount

            if part_of_ctc.custom_is_accrual==1:
                component = new_earning.salary_component
                new_bonus[component] = new_earning.amount

                # frappe.msgprint(str(new_bonus[component]))




        for new_deduction in new_salary_slip.deductions:
            part_of_ctc = frappe.get_doc("Salary Component", new_deduction.salary_component)
            if part_of_ctc.custom_is_part_of_appraisal == 1:
                component = new_deduction.salary_component
                new_amounts[component] = new_deduction.amount

        # Get old salary slip
        old_salary_slip = make_salary_slip(
            source_name=salary_structure_assignment[1].salary_structure,
            employee=employee_id,
            print_format='Salary Slip Standard for CTC',  
            posting_date=salary_structure_assignment[1].from_date  
        )

        # Collect old amounts from earnings and deductions
        for old_earning in old_salary_slip.earnings:
            part_of_ctc = frappe.get_doc("Salary Component", old_earning.salary_component)
            if part_of_ctc.custom_is_part_of_appraisal == 1:
                component = old_earning.salary_component
                old_amounts[component] = old_earning.amount

            if part_of_ctc.custom_is_accrual==1:
                component = old_earning.salary_component
                old_bonus[component] = old_earning.amount

                # frappe.msgprint(str(old_bonus[component]))

        for old_deduction in old_salary_slip.deductions:
            part_of_ctc = frappe.get_doc("Salary Component", old_deduction.salary_component)
            if part_of_ctc.custom_is_part_of_appraisal == 1:
                component = old_deduction.salary_component
                old_amounts[component] = old_deduction.amount

        # Collect all components (union of old and new components)
        all_components = set(old_amounts.keys()).union(set(new_amounts.keys()))

        all_bonus_components=set(old_bonus.keys()).union(set(new_bonus.keys()))


        # frappe.msgprint(str(all_bonus_components))

        result = []
        for component in all_components:
            old_amount = old_amounts.get(component, 0)  
            new_amount = new_amounts.get(component, 0)  
            
            result.append({
                "component": component,
                "old_amount": old_amount,
                "new_amount": new_amount
            })

        


        bonus_result=[]

        for component in all_bonus_components:
            old_amount = old_bonus.get(component, 0)  
            new_amount = new_bonus.get(component, 0)  
            
            bonus_result.append({
                "component": component,
                "old_amount": old_amount,
                "new_amount": new_amount
            })

        


        # frappe.msgprint(str(bonus_result))

        final_array = []

        # Get salary slips after effective_from date

        
        if effective_from:
            get_all_salary_slip = frappe.get_list('Salary Slip',
                filters={
                    'employee': employee_id,
                    'company': company,
                    'docstatus': 1,
                    'end_date': ['>=', effective_from]
                },
                fields=['*']
            )

            # Iterate through salary slips and append salary components with old and new amounts
            if get_all_salary_slip:
                for slip in get_all_salary_slip:
                    get_each_doc = frappe.get_doc("Salary Slip", slip.name)

                    # Fetch LOP Reversal for the specific salary slip
                    get_lop_reversal = frappe.get_list('LOP Reversal',
                        filters={
                            'employee': employee_id,
                            'company': company,
                            'docstatus': 1,
                            'salary_slip': get_each_doc.name  # Filter by current salary slip
                        },
                        fields=['*']
                    )

                    lop_reversal = sum([lop.number_of_days for lop in get_lop_reversal])
                        
                    # Calculate actual LOP and payment days
                    actual_lop = get_each_doc.leave_without_pay - lop_reversal
                    payment_days = get_each_doc.total_working_days - actual_lop

                    # Append salary components with prorated amounts based on payment days
                    for entry in result:
                        prorated_old_amount = (entry["old_amount"] / get_each_doc.total_working_days) * payment_days
                        prorated_new_amount = (entry["new_amount"] / get_each_doc.total_working_days) * payment_days

                        final_array.append({
                            "salary_component": entry["component"],
                            "salary_slip": slip.name,
                            "lop_reversal": lop_reversal,
                            "month": get_each_doc.custom_month,
                            "working_days": get_each_doc.total_working_days,
                            "lop_days": get_each_doc.leave_without_pay,
                            "old_amount": prorated_old_amount,
                            "new_amount": prorated_new_amount,
                            "difference": prorated_new_amount - prorated_old_amount
                        })


        final_bonus_array = []

        # Get salary slips after effective_from date
        if effective_from:
            get_all_salary_slip = frappe.get_list('Salary Slip',
                filters={
                    'employee': employee_id,
                    'company': company,
                    'docstatus': 1,
                    'end_date': ['>=', effective_from]
                },
                fields=['*']
            )

            # Iterate through salary slips and append salary components with old and new amounts
            if get_all_salary_slip:
                for slip in get_all_salary_slip:
                    get_each_doc = frappe.get_doc("Salary Slip", slip.name)

                    # Fetch LOP Reversal for the specific salary slip
                    get_lop_reversal = frappe.get_list('LOP Reversal',
                        filters={
                            'employee': employee_id,
                            'company': company,
                            'docstatus': 1,
                            'salary_slip': get_each_doc.name  # Filter by current salary slip
                        },
                        fields=['*']
                    )

                    lop_reversal = sum([lop.number_of_days for lop in get_lop_reversal])
                        
                    # Calculate actual LOP and payment days
                    actual_lop = get_each_doc.leave_without_pay - lop_reversal
                    payment_days = get_each_doc.total_working_days - actual_lop

                    # Append salary components with prorated amounts based on payment days
                    for entry in bonus_result:
                        prorated_old_amount = (entry["old_amount"] / get_each_doc.total_working_days) * payment_days
                        prorated_new_amount = (entry["new_amount"] / get_each_doc.total_working_days) * payment_days

                        final_bonus_array.append({
                            "salary_component": entry["component"],
                            "salary_slip": slip.name,
                            "lop_reversal": lop_reversal,
                            "month": get_each_doc.custom_month,
                            "working_days": get_each_doc.total_working_days,
                            "lop_days": get_each_doc.leave_without_pay,
                            "old_amount": prorated_old_amount,
                            "new_amount": prorated_new_amount,
                            "difference": prorated_new_amount - prorated_old_amount
                        })















        

        # INSERT REIMBURSEMENT
        if len(salary_structure_assignment) == 2:
            reimbursement_array = []
            reimbursement_final_array=[]
            
            # Fetch the new Salary Structure Assignment
            get_ssa_new = frappe.get_doc("Salary Structure Assignment", salary_structure_assignment[0].name)

            # Loop through the new reimbursements and add them to the reimbursement_array
            for reimbursement in get_ssa_new.custom_employee_reimbursements:
                reimbursement_array.append({
                    "component": reimbursement.reimbursements,
                    "new_amount": reimbursement.monthly_total_amount,
                    "old_amount": 0
                })

            # frappe.msgprint(str(reimbursement_array))
            
            # Fetch the old Salary Structure Assignment
            get_ssa_old = frappe.get_doc("Salary Structure Assignment", salary_structure_assignment[1].name)

            # Loop through the old reimbursements and update the reimbursement_array accordingly
            for reimbursemenold in get_ssa_old.custom_employee_reimbursements:
                found = False
                
                # Check if the old reimbursement component already exists in the reimbursement_array
                for reimbursement in reimbursement_array:
                    if reimbursement["component"] == reimbursemenold.reimbursements:
                        # Update the old_amount for the matching component
                        reimbursement["old_amount"] = reimbursemenold.monthly_total_amount
                        found = True
                        break
                
                # If the old reimbursement component was not found, add it to the array
                if not found:
                    reimbursement_array.append({
                        "component": reimbursemenold.reimbursements,
                        "new_amount": 0,
                        "old_amount": reimbursemenold.monthly_total_amount
                    })

            # Display the final reimbursement array
            # frappe.msgprint(str(reimbursement_array))


            if effective_from:
                get_all_salary_slip = frappe.get_list('Salary Slip',
                    filters={
                        'employee': employee_id,
                        'company': company,
                        'docstatus': 1,
                        'end_date': ['>=', effective_from]
                    },
                    fields=['*']
                )

                # Iterate through salary slips and append salary components with old and new amounts
                if get_all_salary_slip:
                    for slip in get_all_salary_slip:
                        get_each_doc = frappe.get_doc("Salary Slip", slip.name)

                        # Fetch LOP Reversal for the specific salary slip
                        get_lop_reversal = frappe.get_list('LOP Reversal',
                            filters={
                                'employee': employee_id,
                                'company': company,
                                'docstatus': 1,
                                'salary_slip': get_each_doc.name  # Filter by current salary slip
                            },
                            fields=['*']
                        )

                        lop_reversal = sum([lop.number_of_days for lop in get_lop_reversal])
                            
                        # Calculate actual LOP and payment days
                        actual_lop = get_each_doc.leave_without_pay - lop_reversal
                        payment_days = get_each_doc.total_working_days - actual_lop

                        # Append salary components with prorated amounts based on payment days
                        for entry in reimbursement_array:
                            prorated_old_amount = (entry["old_amount"] / get_each_doc.total_working_days) * payment_days
                            prorated_new_amount = (entry["new_amount"] / get_each_doc.total_working_days) * payment_days

                            reimbursement_final_array.append({
                                "salary_component": entry["component"],
                                "salary_slip": slip.name,
                                "lop_reversal": lop_reversal,
                                "month": get_each_doc.custom_month,
                                "working_days": get_each_doc.total_working_days,
                                "lop_days": get_each_doc.leave_without_pay,
                                "old_amount": prorated_old_amount,
                                "new_amount": prorated_new_amount,
                                "difference": prorated_new_amount - prorated_old_amount
                            })
            # frappe.msgprint(str(reimbursement_final_array))

            
        insert_appraisal = frappe.get_doc({
            "doctype": "Salary Appraisal Calculation",
            "employee": employee_id,
            "posting_date": date,
            "company": company,
            "employee_promotion_id": promotion_id,
            "old_salary_structure_assignment_id": salary_structure_assignment[1].name,
            "old_from_date": salary_structure_assignment[1].from_date,
            "new_salary_structure_assignment_id": salary_structure_assignment[0].name,
            "new_from_date": salary_structure_assignment[0].from_date
        })
        
        # Append components and amounts to child tables in the Salary Appraisal Calculation document
        for entry in result:
            insert_appraisal.append("old_structure_child", {
                "salary_component": entry["component"],
                "old_amount": entry["old_amount"],
                "new_amount": entry["new_amount"]
            })

        for insert_arrear in final_array:
            insert_appraisal.append("salary_arrear_components", {
                "salary_component": insert_arrear["salary_component"],
                "salary_slip_id": insert_arrear["salary_slip"],
                "month": insert_arrear["month"],
                "working_days": insert_arrear["working_days"],
                "lop_days": insert_arrear["lop_days"],
                "old_amount": insert_arrear["old_amount"],
                "expected_amount": insert_arrear["new_amount"],
                "lop_reversal": insert_arrear["lop_reversal"],
                "difference": insert_arrear["difference"]
            })

        for insert_bonus in final_bonus_array:
            insert_appraisal.append("bonus_components", {
                "salary_component": insert_bonus["salary_component"],
                "salary_slip_id": insert_bonus["salary_slip"],
                "month": insert_bonus["month"],
                "working_days": insert_bonus["working_days"],
                "lop_days": insert_bonus["lop_days"],
                "old_amount": insert_bonus["old_amount"],
                "expected_amount": insert_bonus["new_amount"],
                "lop_reversal": insert_bonus["lop_reversal"],
                "difference": insert_bonus["difference"]
            })


        for insert_reimbursement in reimbursement_final_array:
            insert_appraisal.append("reimbursement_components", {
                "salary_component": insert_reimbursement["salary_component"],
                "salary_slip_id": insert_reimbursement["salary_slip"],
                "month": insert_reimbursement["month"],
                "working_days": insert_reimbursement["working_days"],
                "lop_days": insert_reimbursement["lop_days"],
                "old_amount": insert_reimbursement["old_amount"],
                "expected_amount": insert_reimbursement["new_amount"],
                "lop_reversal": insert_reimbursement["lop_reversal"],
                "difference": insert_reimbursement["difference"]
            })

        insert_appraisal.insert()
        frappe.db.commit()

        frappe.msgprint("Salary Appraisal Calculation inserted successfully!")
