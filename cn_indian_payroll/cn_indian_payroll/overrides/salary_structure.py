import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import SalaryStructure


class CustomSalaryStructureAssignment(SalaryStructure):

    def custom_set_salary_structure(self):
        pass