import frappe

from hrms.hr.doctype.leave_encashment.leave_encashment import LeaveEncashment
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


class CustomLeaveEncashment(LeaveEncashment):

    def validate(self):
        self.set_encashment_amount()
        super().validate()

    def set_encashment_amount(self):
        # self.encashment_amount=11

        if self.company:

            get_company_data=frappe.get_doc("Company",self.company)

            

            salary_structure_assignment = frappe.get_list('Salary Structure Assignment',
            filters={'employee': self.employee, 'company': self.company, 'docstatus': 1},
            fields=['*'],
            order_by='from_date desc',
            limit=1
            )
            if salary_structure_assignment:
                # frappe.msgprint("YES")

                new_salary_slip = make_salary_slip(
                source_name=salary_structure_assignment[0].salary_structure,
                employee=self.employee,
                print_format='Salary Slip Standard for CTC',  
                posting_date=salary_structure_assignment[0].from_date  
                )
            
            # # Collect new amounts from earnings and deductions
                for new_earning in new_salary_slip.earnings:
                    # frappe.msgprint(str(new_earning.salary_component))

                    if new_earning.salary_component==get_company_data.basic_component:
                        self.custom_basic_amount=new_earning.amount
                        if self.encashment_days:
                            self.encashment_amount=(new_earning.amount/30)*self.encashment_days

                   

            else:
                frappe.msgprint("Please Assign Salary Structure Assignment for Employee")




