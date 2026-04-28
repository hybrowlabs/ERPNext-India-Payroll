

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    CUSTOM_FIELDS = {
        "Payroll Settings": [

            {
                "fieldname": "custom_configure_attendance_cycle",
                "fieldtype": "Check",
                "label": "Configure Attendance Cycle",
                "insert_after": "consider_unmarked_attendance_as",
                "default": 0
            },
            {
                "fieldname": "custom_attendance_start_date",
                "fieldtype": "Int",
                "label": "Attendance Start Date",
                "insert_after": "custom_configure_attendance_cycle",
                "depends_on": "eval:doc.custom_configure_attendance_cycle",
                "mandatory_depends_on": "eval:doc.custom_configure_attendance_cycle"
            },
            {
                "fieldname": "custom_attendance_end_date",
                "fieldtype": "Int",
                "label": "Attendance End Date",
                "insert_after": "custom_attendance_start_date",
                "depends_on": "eval:doc.custom_configure_attendance_cycle",
                "mandatory_depends_on": "eval:doc.custom_configure_attendance_cycle"
            },
            {
                "fieldname": "custom_tax_calculation_based_on",
                "fieldtype": "Select",
                "label": "Tax Calculation Based On",
                "insert_after": "daily_wages_fraction_for_half_day",
                "options": "Use IT Declaration Values in Payroll Processing\nUse POI Approved Values in Payroll Processing",
                "default": "Use IT Declaration Values in Payroll Processing"
            },
            {
                "fieldname": "custom_attendance_regularize_month",
                "fieldtype": "Select",
                "label": "Attendance Regularisation Month",
                "insert_after": "custom_tax_calculation_based_on",
                "options": "\n".join([str(i) for i in range(1, 13)]),
                "default": "1"
            },
            {
                "fieldname": "custom_salary_structure_configuration_visibility",
                "fieldtype": "Section Break",
                "label": "Salary Structure Configuration Visibility",
                "insert_after": "process_payroll_accounting_entry_based_on_employee"
            },
            {
                "fieldname": "custom_hide_salary_structure_configuration",
                "fieldtype": "Table",
                "label": "Hide Salary Structure Configuration",
                "insert_after": "custom_salary_structure_configuration_visibility",
                "options": "Employment Type Child"
            },
            {
                "fieldname": "custom_field_config",
                "fieldtype": "Table",
                "label": "Field Config",
                "insert_after": "custom_hide_salary_structure_configuration",
                "options": "Missing Config Child"
            },
            {
                "fieldname": "custom_employee_advance_component",
                "fieldtype": "Link",
                "label": "Employee Advance Component",
                "insert_after": "custom_field_config",
                "options": "Salary Component"
            }

        ]
    }

    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)