import frappe

from cn_indian_payroll.cn_indian_payroll.overrides.salary_appraisal_calculation import (
    appraisal_calculation,
)


# def on_cancel(self, method):
#     cancel_additional_salary(self)
#     cancel_appraisal_calculation(self)


def on_submit(self, method):
    self.custom_status = "Completed"


def cancel_additional_salary(self):
    get_appraisal_additional = frappe.get_list(
        "Additional Salary",
        filters={
            "ref_doctype": "Salary Appraisal Calculation",
            "ref_docname": self.name,
        },
        fields=["*"],
    )
    if get_appraisal_additional:
        for each_appraisal_doc in get_appraisal_additional:
            get_each_doc = frappe.get_doc("Additional Salary", each_appraisal_doc.name)
            get_each_doc.docstatus = 2
            get_each_doc.save()
            frappe.delete_doc("Additional Salary", each_appraisal_doc.name)


def validate(self, methd):
    create_salary_appraisal_calculation(self)


def create_salary_appraisal_calculation(self):
    if self.custom_status == "Payroll Configured":
        get_appraisal_calculation = frappe.get_list(
            "Salary Appraisal Calculation",
            filters={"promotion_reference": self.name},
            fields=["*"],
        )
        if not get_appraisal_calculation:
            result = appraisal_calculation(
                promotion_id=self.name,
                employee_id=self.employee,
                company=self.company,
                date=self.custom_additional_salary_date,
                effective_from=self.promotion_date,
            )


def cancel_appraisal_calculation(self):
    get_appraisal_calculation = frappe.get_list(
        "Salary Appraisal Calculation",
        filters={"promotion_reference": self.name},
        fields=["*"],
    )
    if get_appraisal_calculation:
        for each_appraisal_doc in get_appraisal_calculation:
            get_each_doc = frappe.get_doc(
                "Salary Appraisal Calculation", each_appraisal_doc.name
            )
            get_each_doc.docstatus = 2
            get_each_doc.save()
            frappe.delete_doc("Salary Appraisal Calculation", each_appraisal_doc.name)
