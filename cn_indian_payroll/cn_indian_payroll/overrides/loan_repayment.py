

import frappe

def before_save(self, method):
    if self.loan:
        loan = frappe.get_doc('Loan', self.loan)

        if loan.applicant_type == "Employee":
            self.custom_employee = loan.applicant
            self.custom_loan_perquisite_interest_rate = loan.custom_loan_perquisite_rate_of_interest
            self.custom_employee_name = loan.applicant_name

            if self.repayment_schedule:
                self.custom_loan_perquisite = []

                for repayment in self.repayment_schedule:
                    payment_date_str = repayment.payment_date
                    year, month, day = map(int, payment_date_str.split('-'))

                    if month in [1, 3, 5, 7, 8, 10, 12]:
                        last_day_of_month = 31
                    elif month in [4, 6, 9, 11]:
                        last_day_of_month = 30
                    else:
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            last_day_of_month = 29
                        else:
                            last_day_of_month = 28

                    payroll_date = f"{year}-{month:02d}-{last_day_of_month:02d}"
                    perquisite_amount = round(
                        (repayment.balance_loan_amount * self.custom_loan_perquisite_interest_rate) / 1200
                    )

                    self.append("custom_loan_perquisite", {
                        "payment_date": repayment.payment_date,
                        "balance_amount": repayment.balance_loan_amount,
                        "perquisite_amount": perquisite_amount,
                        "payroll_date": payroll_date
                    })



def before_update_after_submit(self,method):
    if self.repayment_schedule:
        self.repayment_periods=len(self.repayment_schedule)
