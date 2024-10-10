import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

@frappe.whitelist()
def appraisal_calculation(promotion_id, employee_id, company, date,effective_from):
    
    if promotion_id:
        old_amounts = {}
        new_amounts = {}
        
        # Fetch salary structure assignments
        salary_structure_assignment = frappe.get_list('Salary Structure Assignment',
            filters={'employee': employee_id, 'company': company, 'docstatus': 1},
            fields=['*'],
            order_by='from_date desc',
            limit=2
        )

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

        # frappe.msgprint(str(new_amounts))

        for new_deduction in new_salary_slip.deductions:
            part_of_ctc = frappe.get_doc("Salary Component", new_deduction.salary_component)
            if part_of_ctc.custom_is_part_of_appraisal == 1:
                component = new_deduction.salary_component
                new_amounts[component] = new_deduction.amount

        old_salary_slip = make_salary_slip(
            source_name=salary_structure_assignment[1].salary_structure,
            employee=employee_id,
            print_format='Salary Slip Standard for CTC',  
            posting_date=salary_structure_assignment[1].from_date  
        )

        for old_earning in old_salary_slip.earnings:
            part_of_ctc = frappe.get_doc("Salary Component", old_earning.salary_component)
            if part_of_ctc.custom_is_part_of_appraisal == 1:
                component = old_earning.salary_component
                old_amounts[component] = old_earning.amount

        for old_deduction in old_salary_slip.deductions:
            part_of_ctc = frappe.get_doc("Salary Component", old_deduction.salary_component)
            if part_of_ctc.custom_is_part_of_appraisal == 1:
                component = old_deduction.salary_component
                old_amounts[component] = old_deduction.amount

        all_components = set(old_amounts.keys()).union(set(new_amounts.keys()))

        result = []
        for component in all_components:
            old_amount = old_amounts.get(component, 0)  
            new_amount = new_amounts.get(component, 0)  
            
            result.append({
                "component": component,
                "old_amount": old_amount,
                "new_amount": new_amount
            })

        # frappe.msgprint(str(result))


        if date:
            final_array = []
           
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

                    for entry in result:
                        final_array.append({
                            "salary_component": entry["component"],
                            "salary_slip": slip.name,
                            "month": get_each_doc.custom_month,
                            "working_days": get_each_doc.total_working_days,
                            "lop_days": get_each_doc.leave_without_pay,
                            "old_amount": entry["old_amount"],
                            "new_amount": entry["new_amount"]
                        })

            # frappe.msgprint(str(final_array))


        insert_appraisal = frappe.get_doc({
            "doctype": "Salary Appraisal Calculation",
            "employee": employee_id,
            "posting_date": date,
            "company":company,
            "employee_promotion_id":promotion_id,
            "old_salary_structure_assignment_id":salary_structure_assignment[0].name,
            "old_from_date":salary_structure_assignment[0].from_date,
            "new_salary_structure_assignment_id":salary_structure_assignment[1].name,
            "new_from_date":salary_structure_assignment[1].from_date
        })
        
        
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
                "working_days":insert_arrear["working_days"],
                "lop_days":insert_arrear["lop_days"],
                "old_amount":insert_arrear["old_amount"],
                "expected_amount":insert_arrear["new_amount"],
            })


        
        insert_appraisal.insert()
        frappe.db.commit()

        frappe.msgprint("Salary Appraisal Calculation inserted successfully!")
