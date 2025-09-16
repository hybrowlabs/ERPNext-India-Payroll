# # # import frappe
# # # from collections import defaultdict

# # # def execute(filters=None):
# # #     # Get components
# # #     earning_components, deduction_components = get_used_components(filters)

# # #     # Split into fixed / variable
# # #     fixed_earnings, variable_earnings = split_components(earning_components)
# # #     fixed_deductions, variable_deductions = split_components(deduction_components)

# # #     # Columns and Data
# # #     columns = get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)
# # #     data = get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)

# # #     return columns, data


# # # def split_components(components):
# # #     """Split components into Fixed and Variable based on custom_component_sub_type."""
# # #     fixed, variable = [], []
# # #     for c in components:
# # #         comp = frappe.get_cached_doc("Salary Component", c)
# # #         if comp.custom_component_sub_type == "Fixed":
# # #             fixed.append(c)
# # #         else:
# # #             variable.append(c)
# # #     return fixed, variable


# # # def get_used_components(filters):
# # #     """Fetch salary components actually used in selected Salary Slips (only do_not_include_in_total=0)."""
# # #     conditions = {"docstatus": ["in", [0, 1]]}
# # #     if filters.get("company"):
# # #         conditions["company"] = filters["company"]
# # #     if filters.get("employee"):
# # #         conditions["employee"] = filters["employee"]
# # #     if filters.get("custom_payroll_period"):
# # #         conditions["custom_payroll_period"] = filters["custom_payroll_period"]

# # #     slips = frappe.get_all("Salary Slip", filters=conditions, fields=["name"])
# # #     slip_names = [s.name for s in slips]

# # #     if not slip_names:
# # #         return [], []

# # #     # Fetch child rows (earnings & deductions) at once
# # #     earnings = frappe.get_all(
# # #         "Salary Detail",
# # #         filters={
# # #             "parent": ["in", slip_names],
# # #             "parenttype": "Salary Slip",
# # #             "parentfield": "earnings",
# # #             "do_not_include_in_total": 0
# # #         },
# # #         fields=["salary_component"]
# # #     )

# # #     deductions = frappe.get_all(
# # #         "Salary Detail",
# # #         filters={
# # #             "parent": ["in", slip_names],
# # #             "parenttype": "Salary Slip",
# # #             "parentfield": "deductions",
# # #             "do_not_include_in_total": 0
# # #         },
# # #         fields=["salary_component"]
# # #     )

# # #     used_earnings = {e.salary_component for e in earnings}
# # #     used_deductions = {d.salary_component for d in deductions}

# # #     return list(used_earnings), list(used_deductions)


# # # def get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
# # #     base_columns = [
# # #         {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
# # #         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
# # #         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
# # #         {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
# # #     ]

# # #     fixed_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in fixed_earnings]
# # #     fixed_earning_total = [{"label": "Fixed Earnings Total", "fieldname": "fixed_earnings", "fieldtype": "Currency", "width": 150}]

# # #     variable_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in variable_earnings]
# # #     variable_earning_total = [{"label": "Variable Earnings Total", "fieldname": "variable_earnings", "fieldtype": "Currency", "width": 150}]

# # #     gross = [{"label": "Gross Pay", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 150}]

# # #     fixed_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in fixed_deductions]
# # #     fixed_deduction_total = [{"label": "Fixed Deductions Total", "fieldname": "fixed_deductions", "fieldtype": "Currency", "width": 150}]

# # #     variable_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in variable_deductions]
# # #     variable_deduction_total = [{"label": "Variable Deductions Total", "fieldname": "variable_deductions", "fieldtype": "Currency", "width": 150}]

# # #     totals = [
# # #         {"label": "Total Deductions", "fieldname": "total_deduction", "fieldtype": "Currency", "width": 150},
# # #         {"label": "Net Pay", "fieldname": "net_pay", "fieldtype": "Currency", "width": 150},
# # #     ]

# # #     return (
# # #         base_columns
# # #         + fixed_earning_cols + fixed_earning_total
# # #         + variable_earning_cols + variable_earning_total
# # #         + gross
# # #         + fixed_deduction_cols + fixed_deduction_total
# # #         + variable_deduction_cols + variable_deduction_total
# # #         + totals
# # #     )


# # # def get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
# # #     conditions = {"docstatus": ["in", [0, 1]]}
# # #     if filters.get("company"):
# # #         conditions["company"] = filters["company"]
# # #     if filters.get("employee"):
# # #         conditions["employee"] = filters["employee"]
# # #     if filters.get("custom_payroll_period"):
# # #         conditions["custom_payroll_period"] = filters["custom_payroll_period"]

# # #     salary_slips = frappe.get_all(
# # #         "Salary Slip",
# # #         filters=conditions,
# # #         fields=["name", "employee", "employee_name", "company",
# # #                 "custom_payroll_period", "gross_pay", "total_deduction", "net_pay"]
# # #     )
# # #     slip_names = [s.name for s in salary_slips]

# # #     if not slip_names:
# # #         return []

# # #     # Bulk fetch earnings & deductions
# # #     earnings = frappe.get_all(
# # #         "Salary Detail",
# # #         filters={
# # #             "parent": ["in", slip_names],
# # #             "parenttype": "Salary Slip",
# # #             "parentfield": "earnings",
# # #             "do_not_include_in_total": 0
# # #         },
# # #         fields=["parent", "salary_component", "amount"]
# # #     )

# # #     deductions = frappe.get_all(
# # #         "Salary Detail",
# # #         filters={
# # #             "parent": ["in", slip_names],
# # #             "parenttype": "Salary Slip",
# # #             "parentfield": "deductions",
# # #             "do_not_include_in_total": 0
# # #         },
# # #         fields=["parent", "salary_component", "amount"]
# # #     )

# # #     # Group child rows by Salary Slip
# # #     earnings_by_slip = defaultdict(list)
# # #     for e in earnings:
# # #         earnings_by_slip[e.parent].append(e)

# # #     deductions_by_slip = defaultdict(list)
# # #     for d in deductions:
# # #         deductions_by_slip[d.parent].append(d)

# # #     # Prepare final data
# # #     data = []
# # #     for slip in salary_slips:
# # #         row = {
# # #             "employee": slip.employee,
# # #             "employee_name": slip.employee_name,
# # #             "company": slip.company,
# # #             "custom_payroll_period": slip.custom_payroll_period,
# # #             "gross_pay": slip.gross_pay,
# # #             "total_deduction": slip.total_deduction,
# # #             "net_pay": slip.net_pay,
# # #             "fixed_earnings": 0,
# # #             "variable_earnings": 0,
# # #             "fixed_deductions": 0,
# # #             "variable_deductions": 0,
# # #         }

# # #         # Init component columns
# # #         for ec in fixed_earnings + variable_earnings:
# # #             row[frappe.scrub(ec)] = 0
# # #         for dc in fixed_deductions + variable_deductions:
# # #             row[frappe.scrub(dc)] = 0

# # #         # Earnings
# # #         for e in earnings_by_slip.get(slip.name, []):
# # #             row[frappe.scrub(e.salary_component)] = e.amount
# # #             comp = frappe.get_cached_doc("Salary Component", e.salary_component)
# # #             if comp.custom_component_sub_type == "Fixed":
# # #                 row["fixed_earnings"] += e.amount
# # #             else:
# # #                 row["variable_earnings"] += e.amount

# # #         # Deductions
# # #         for d in deductions_by_slip.get(slip.name, []):
# # #             row[frappe.scrub(d.salary_component)] = d.amount
# # #             comp = frappe.get_cached_doc("Salary Component", d.salary_component)
# # #             if comp.custom_component_sub_type == "Fixed":
# # #                 row["fixed_deductions"] += d.amount
# # #             else:
# # #                 row["variable_deductions"] += d.amount

# # #         data.append(row)

# # #     return data


# # import frappe
# # from collections import defaultdict

# # def execute(filters=None):
# #     # Get components
# #     earning_components, deduction_components = get_used_components(filters)

# #     # Split into fixed / variable
# #     fixed_earnings, variable_earnings = split_components(earning_components)
# #     fixed_deductions, variable_deductions = split_components(deduction_components)

# #     # Columns and Data
# #     columns = get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)
# #     data = get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)

# #     return columns, data


# # def split_components(components):
# #     """Split components into Fixed and Variable based on custom_component_sub_type."""
# #     fixed, variable = [], []
# #     for c in components:
# #         comp = frappe.get_cached_doc("Salary Component", c)
# #         if comp.custom_component_sub_type == "Fixed":
# #             fixed.append(c)
# #         else:
# #             variable.append(c)
# #     return fixed, variable


# # def get_used_components(filters):
# #     """Fetch salary components actually used in selected Salary Slips (only do_not_include_in_total=0)."""
# #     conditions = {"docstatus": ["in", [0, 1]]}
# #     if filters.get("company"):
# #         conditions["company"] = filters["company"]
# #     if filters.get("employee"):
# #         conditions["employee"] = filters["employee"]
# #     if filters.get("custom_payroll_period"):
# #         conditions["custom_payroll_period"] = filters["custom_payroll_period"]
# #     if filters.get("start_date"):
# #         conditions["start_date"] = [">=", filters["start_date"]]
# #     if filters.get("end_date"):
# #         conditions["end_date"] = ["<=", filters["end_date"]]

# #     slips = frappe.get_all("Salary Slip", filters=conditions, fields=["name"])
# #     slip_names = [s.name for s in slips]

# #     if not slip_names:
# #         return [], []

# #     # Fetch child rows (earnings & deductions) at once
# #     earnings = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "earnings",
# #             "do_not_include_in_total": 0
# #         },
# #         fields=["salary_component"]
# #     )

# #     deductions = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "deductions",
# #             "do_not_include_in_total": 0
# #         },
# #         fields=["salary_component"]
# #     )

# #     used_earnings = {e.salary_component for e in earnings}
# #     used_deductions = {d.salary_component for d in deductions}

# #     return list(used_earnings), list(used_deductions)


# # def get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
# #     base_columns = [
# #         {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
# #         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
# #         {"label": "Salary Slip ID", "fieldname": "salary_slip_id", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
# #         {"label": "Date of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
# #         {"label": "Total Working Days", "fieldname": "total_working_days", "fieldtype": "Float", "width": 140},
# #         {"label": "Absent Days", "fieldname": "absent_days", "fieldtype": "Float", "width": 120},
# #         {"label": "Leave Without Pay", "fieldname": "leave_without_pay", "fieldtype": "Float", "width": 140},
# #         {"label": "Total LOP Days", "fieldname": "total_lop_days", "fieldtype": "Float", "width": 130},
# #         {"label": "Payment Days", "fieldname": "payment_days", "fieldtype": "Float", "width": 130},
# #         {"label": "Arrear Days", "fieldname": "arrear_days", "fieldtype": "Float", "width": 120},
# #         {"label": "Total Payment Days", "fieldname": "total_payment_days", "fieldtype": "Float", "width": 150},
# #         {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
# #         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
# #         {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
# #     ]

# #     fixed_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in fixed_earnings]
# #     fixed_earning_total = [{"label": "Fixed Earnings Total", "fieldname": "fixed_earnings", "fieldtype": "Currency", "width": 150}]

# #     variable_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in variable_earnings]
# #     variable_earning_total = [{"label": "Variable Earnings Total", "fieldname": "variable_earnings", "fieldtype": "Currency", "width": 150}]

# #     gross = [{"label": "Gross Pay", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 150}]

# #     fixed_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in fixed_deductions]
# #     fixed_deduction_total = [{"label": "Fixed Deductions Total", "fieldname": "fixed_deductions", "fieldtype": "Currency", "width": 150}]

# #     variable_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in variable_deductions]
# #     variable_deduction_total = [{"label": "Variable Deductions Total", "fieldname": "variable_deductions", "fieldtype": "Currency", "width": 150}]

# #     totals = [
# #         {"label": "Total Deductions", "fieldname": "total_deduction", "fieldtype": "Currency", "width": 150},
# #         {"label": "Net Pay", "fieldname": "net_pay", "fieldtype": "Currency", "width": 150},
# #     ]

# #     return (
# #         base_columns
# #         + fixed_earning_cols + fixed_earning_total
# #         + variable_earning_cols + variable_earning_total
# #         + gross
# #         + fixed_deduction_cols + fixed_deduction_total
# #         + variable_deduction_cols + variable_deduction_total
# #         + totals
# #     )


# # def get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
# #     conditions = {"docstatus": ["in", [0, 1]]}
# #     if filters.get("company"):
# #         conditions["company"] = filters["company"]
# #     if filters.get("employee"):
# #         conditions["employee"] = filters["employee"]
# #     if filters.get("custom_payroll_period"):
# #         conditions["custom_payroll_period"] = filters["custom_payroll_period"]
# #     if filters.get("start_date"):
# #         conditions["start_date"] = [">=", filters["start_date"]]
# #     if filters.get("end_date"):
# #         conditions["end_date"] = ["<=", filters["end_date"]]


# #     salary_slips = frappe.get_all(
# #         "Salary Slip",
# #         filters=conditions,
# #         fields=[
# #             "name", "employee", "employee_name", "company", "custom_payroll_period",
# #             "gross_pay", "total_deduction", "net_pay", "total_working_days",
# #             "absent_days", "leave_without_pay", "payment_days","start_date", "end_date",
# #             "custom_lop_reversal_days", "custom_month","custom_statutory_grosspay","custom_net_pay_amount"
# #         ]
# #     )
# #     slip_names = [s.name for s in salary_slips]

# #     if not slip_names:
# #         return []

# #     # Bulk fetch earnings & deductions
# #     earnings = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "earnings",
# #             "do_not_include_in_total": 0
# #         },
# #         fields=["parent", "salary_component", "amount"]
# #     )

# #     deductions = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "deductions",
# #             "do_not_include_in_total": 0
# #         },
# #         fields=["parent", "salary_component", "amount"]
# #     )

# #     # Fetch employee join dates in bulk
# #     employee_ids = list({s.employee for s in salary_slips})
# #     employees = frappe.get_all(
# #         "Employee",
# #         filters={"name": ["in", employee_ids]},
# #         fields=["name", "date_of_joining"]
# #     )
# #     employee_map = {emp.name: emp.date_of_joining for emp in employees}

# #     # Group child rows by Salary Slip
# #     earnings_by_slip = defaultdict(list)
# #     for e in earnings:
# #         earnings_by_slip[e.parent].append(e)

# #     deductions_by_slip = defaultdict(list)
# #     for d in deductions:
# #         deductions_by_slip[d.parent].append(d)

# #     # Prepare final data
# #     data = []
# #     for slip in salary_slips:
# #         total_lop_days = (slip.leave_without_pay or 0) + (slip.absent_days or 0)
# #         total_payment_days = (slip.payment_days or 0) + (slip.custom_lop_reversal_days or 0)

# #         row = {
# #             "employee": slip.employee,
# #             "employee_name": slip.employee_name,
# #             "salary_slip_id": slip.name,
# #             "date_of_joining": employee_map.get(slip.employee),
# #             "total_working_days": slip.total_working_days,
# #             "absent_days": slip.absent_days,
# #             "leave_without_pay": slip.leave_without_pay,
# #             "total_lop_days": total_lop_days,
# #             "payment_days": slip.payment_days,
# #             "arrear_days": slip.custom_lop_reversal_days,
# #             "total_payment_days": total_payment_days,
# #             "month": slip.custom_month,
# #             "company": slip.company,
# #             "custom_payroll_period": slip.custom_payroll_period,
# #             "gross_pay": slip.custom_statutory_grosspay,
# #             "total_deduction": slip.total_deduction,
# #             "net_pay": slip.custom_net_pay_amount,
# #             "fixed_earnings": 0,
# #             "variable_earnings": 0,
# #             "fixed_deductions": 0,
# #             "variable_deductions": 0,
# #         }

# #         # Init component columns
# #         for ec in fixed_earnings + variable_earnings:
# #             row[frappe.scrub(ec)] = 0
# #         for dc in fixed_deductions + variable_deductions:
# #             row[frappe.scrub(dc)] = 0

# #         # Earnings
# #         for e in earnings_by_slip.get(slip.name, []):
# #             row[frappe.scrub(e.salary_component)] = e.amount
# #             comp = frappe.get_cached_doc("Salary Component", e.salary_component)
# #             if comp.custom_component_sub_type == "Fixed":
# #                 row["fixed_earnings"] += e.amount
# #             else:
# #                 row["variable_earnings"] += e.amount

# #         # Deductions
# #         for d in deductions_by_slip.get(slip.name, []):
# #             row[frappe.scrub(d.salary_component)] = d.amount
# #             comp = frappe.get_cached_doc("Salary Component", d.salary_component)
# #             if comp.custom_component_sub_type == "Fixed":
# #                 row["fixed_deductions"] += d.amount
# #             else:
# #                 row["variable_deductions"] += d.amount

# #         data.append(row)

# #     return data



# # import frappe
# # from collections import defaultdict

# # def execute(filters=None):
# #     # Get components
# #     earning_components, deduction_components = get_used_components(filters)

# #     # Split into fixed / variable and sort by custom_sequence
# #     fixed_earnings, variable_earnings = split_and_sort_components(earning_components)
# #     fixed_deductions, variable_deductions = split_and_sort_components(deduction_components)

# #     # Columns and Data
# #     columns = get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)
# #     data = get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)

# #     return columns, data


# # def split_and_sort_components(components):
# #     """Split components into Fixed and Variable based on custom_component_sub_type and sort by custom_sequence."""
# #     fixed, variable = [], []
# #     comp_sequence_map = {}
# #     for c in components:
# #         comp = frappe.get_cached_doc("Salary Component", c)
# #         comp_sequence_map[c] = comp.custom_sequence or 9999
# #         if comp.custom_component_sub_type == "Fixed":
# #             fixed.append(c)
# #         else:
# #             variable.append(c)
# #     # Sort lists based on custom_sequence
# #     fixed.sort(key=lambda x: comp_sequence_map[x])
# #     variable.sort(key=lambda x: comp_sequence_map[x])
# #     return fixed, variable


# # def get_used_components(filters):
# #     """Fetch salary components actually used in selected Salary Slips (only do_not_include_in_total=0)."""
# #     conditions = [["docstatus", "in", [0, 1]]]

# #     if filters.get("company"):
# #         conditions.append(["company", "=", filters["company"]])
# #     if filters.get("employee"):
# #         conditions.append(["employee", "=", filters["employee"]])
# #     if filters.get("custom_payroll_period"):
# #         conditions.append(["custom_payroll_period", "=", filters["custom_payroll_period"]])
# #     if filters.get("start_date"):
# #         conditions.append(["start_date", ">=", filters["start_date"]])
# #     if filters.get("end_date"):
# #         conditions.append(["end_date", "<=", filters["end_date"]])

# #     slips = frappe.get_all("Salary Slip", filters=conditions, fields=["name"])
# #     slip_names = [s.name for s in slips]

# #     if not slip_names:
# #         return [], []

# #     # Fetch child rows (earnings & deductions)
# #     earnings = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "earnings",
# #             "do_not_include_in_total": 0
# #         },
# #         fields=["salary_component"]
# #     )

# #     deductions = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "deductions",
# #             "do_not_include_in_total": 0
# #         },
# #         fields=["salary_component"]
# #     )

# #     used_earnings = {e.salary_component for e in earnings}
# #     used_deductions = {d.salary_component for d in deductions}

# #     return list(used_earnings), list(used_deductions)


# # def get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
# #     base_columns = [
# #         {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
# #         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
# #         {"label": "Salary Slip ID", "fieldname": "salary_slip_id", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
# #         {"label": "Date of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
# #         {"label": "Total Working Days", "fieldname": "total_working_days", "fieldtype": "Float", "width": 140},
# #         {"label": "Absent Days", "fieldname": "absent_days", "fieldtype": "Float", "width": 120},
# #         {"label": "Leave Without Pay", "fieldname": "leave_without_pay", "fieldtype": "Float", "width": 140},
# #         {"label": "Total LOP Days", "fieldname": "total_lop_days", "fieldtype": "Float", "width": 130},
# #         {"label": "Payment Days", "fieldname": "payment_days", "fieldtype": "Float", "width": 130},
# #         {"label": "Arrear Days", "fieldname": "arrear_days", "fieldtype": "Float", "width": 120},
# #         {"label": "Total Payment Days", "fieldname": "total_payment_days", "fieldtype": "Float", "width": 150},
# #         {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
# #         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
# #         {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
# #     ]

# #     fixed_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in fixed_earnings]
# #     fixed_earning_total = [{"label": "Fixed Earnings Total", "fieldname": "fixed_earnings", "fieldtype": "Currency", "width": 150}]

# #     variable_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in variable_earnings]
# #     variable_earning_total = [{"label": "Variable Earnings Total", "fieldname": "variable_earnings", "fieldtype": "Currency", "width": 150}]

# #     gross = [{"label": "Gross Pay", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 150}]

# #     fixed_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in fixed_deductions]
# #     fixed_deduction_total = [{"label": "Fixed Deductions Total", "fieldname": "fixed_deductions", "fieldtype": "Currency", "width": 150}]

# #     variable_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in variable_deductions]
# #     variable_deduction_total = [{"label": "Variable Deductions Total", "fieldname": "variable_deductions", "fieldtype": "Currency", "width": 150}]

# #     totals = [
# #         {"label": "Total Deductions", "fieldname": "total_deduction", "fieldtype": "Currency", "width": 150},
# #         {"label": "Net Pay", "fieldname": "net_pay", "fieldtype": "Currency", "width": 150},
# #     ]

# #     return (
# #         base_columns
# #         + fixed_earning_cols + fixed_earning_total
# #         + variable_earning_cols + variable_earning_total
# #         + gross
# #         + fixed_deduction_cols + fixed_deduction_total
# #         + variable_deduction_cols + variable_deduction_total
# #         + totals
# #     )


# # def get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
# #     conditions = [["docstatus", "in", [0, 1]]]

# #     if filters.get("company"):
# #         conditions.append(["company", "=", filters["company"]])
# #     if filters.get("employee"):
# #         conditions.append(["employee", "=", filters["employee"]])
# #     if filters.get("custom_payroll_period"):
# #         conditions.append(["custom_payroll_period", "=", filters["custom_payroll_period"]])
# #     if filters.get("start_date"):
# #         conditions.append(["start_date", ">=", filters["start_date"]])
# #     if filters.get("end_date"):
# #         conditions.append(["end_date", "<=", filters["end_date"]])

# #     salary_slips = frappe.get_all(
# #         "Salary Slip",
# #         filters=conditions,
# #         fields=[
# #             "name", "employee", "employee_name", "company", "custom_payroll_period",
# #             "gross_pay", "total_deduction", "net_pay", "total_working_days",
# #             "absent_days", "leave_without_pay", "payment_days", "start_date", "end_date",
# #             "custom_lop_reversal_days", "custom_month", "custom_statutory_grosspay", "custom_net_pay_amount"
# #         ]
# #     )
# #     slip_names = [s.name for s in salary_slips]

# #     if not slip_names:
# #         return []

# #     # Bulk fetch earnings & deductions
# #     earnings = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "earnings",
# #             # "do_not_include_in_total": 0
# #         },
# #         fields=["parent", "salary_component", "amount"]
# #     )

# #     deductions = frappe.get_all(
# #         "Salary Detail",
# #         filters={
# #             "parent": ["in", slip_names],
# #             "parenttype": "Salary Slip",
# #             "parentfield": "deductions",
# #             "do_not_include_in_total": 0
# #         },
# #         fields=["parent", "salary_component", "amount"]
# #     )

# #     # Fetch employee join dates
# #     employee_ids = list({s.employee for s in salary_slips})
# #     employees = frappe.get_all(
# #         "Employee",
# #         filters={"name": ["in", employee_ids]},
# #         fields=["name", "date_of_joining"]
# #     )
# #     employee_map = {emp.name: emp.date_of_joining for emp in employees}

# #     # Group child rows by Salary Slip
# #     earnings_by_slip = defaultdict(list)
# #     for e in earnings:
# #         earnings_by_slip[e.parent].append(e)
# #     deductions_by_slip = defaultdict(list)
# #     for d in deductions:
# #         deductions_by_slip[d.parent].append(d)

# #     # Prepare final data
# #     data = []
# #     for slip in salary_slips:
# #         total_lop_days = (slip.leave_without_pay or 0) + (slip.absent_days or 0)
# #         total_payment_days = (slip.payment_days or 0) + (slip.custom_lop_reversal_days or 0)

# #         row = {
# #             "employee": slip.employee,
# #             "employee_name": slip.employee_name,
# #             "salary_slip_id": slip.name,
# #             "date_of_joining": employee_map.get(slip.employee),
# #             "total_working_days": slip.total_working_days,
# #             "absent_days": slip.absent_days,
# #             "leave_without_pay": slip.leave_without_pay,
# #             "total_lop_days": total_lop_days,
# #             "payment_days": slip.payment_days,
# #             "arrear_days": slip.custom_lop_reversal_days,
# #             "total_payment_days": total_payment_days,
# #             "month": slip.custom_month,
# #             "company": slip.company,
# #             "custom_payroll_period": slip.custom_payroll_period,
# #             "gross_pay": slip.custom_statutory_grosspay,
# #             "total_deduction": slip.total_deduction,
# #             "net_pay": slip.custom_net_pay_amount,
# #             "fixed_earnings": 0,
# #             "variable_earnings": 0,
# #             "fixed_deductions": 0,
# #             "variable_deductions": 0,
# #         }

# #         # Init component columns
# #         for ec in fixed_earnings + variable_earnings:
# #             row[frappe.scrub(ec)] = 0
# #         for dc in fixed_deductions + variable_deductions:
# #             row[frappe.scrub(dc)] = 0

# #         # Earnings
# #         for e in earnings_by_slip.get(slip.name, []):
# #             row[frappe.scrub(e.salary_component)] = e.amount
# #             comp = frappe.get_cached_doc("Salary Component", e.salary_component)
# #             if comp.custom_component_sub_type == "Fixed":
# #                 row["fixed_earnings"] += e.amount
# #             else:
# #                 row["variable_earnings"] += e.amount

# #         # Deductions
# #         for d in deductions_by_slip.get(slip.name, []):
# #             row[frappe.scrub(d.salary_component)] = d.amount
# #             comp = frappe.get_cached_doc("Salary Component", d.salary_component)
# #             if comp.custom_component_sub_type == "Fixed":
# #                 row["fixed_deductions"] += d.amount
# #             else:
# #                 row["variable_deductions"] += d.amount

# #         data.append(row)

# #     return data
# import frappe
# from collections import defaultdict

# # ----------------------------
# # Helper Functions
# # ----------------------------

# def split_and_sort_components(components):
#     """
#     Split components into Fixed and Variable based on custom_component_sub_type
#     and sort by custom_sequence.
#     """
#     fixed, variable = [], []
#     comp_sequence_map = {}
#     for c in components:
#         comp = frappe.get_cached_doc("Salary Component", c)
#         comp_sequence_map[c] = comp.custom_sequence or 9999  # default if sequence not set
#         if comp.custom_component_sub_type == "Fixed":
#             fixed.append(c)
#         else:
#             variable.append(c)
#     fixed.sort(key=lambda x: comp_sequence_map[x])
#     variable.sort(key=lambda x: comp_sequence_map[x])
#     return fixed, variable


# def get_used_components(filters):
#     """
#     Fetch salary components actually used in selected Salary Slips
#     considering do_not_include_in_total = 0
#     """
#     flt = {"docstatus": ["in", [0, 1]]}
#     if filters.get("company"):
#         flt["company"] = filters["company"]
#     if filters.get("employee"):
#         flt["employee"] = filters["employee"]
#     if filters.get("custom_payroll_period"):
#         flt["custom_payroll_period"] = filters["custom_payroll_period"]
#     if filters.get("custom_month"):
#         flt["custom_month"] = filters["custom_month"]

#     slips = frappe.get_all("Salary Slip", filters=flt, fields=["name"])
#     slip_names = [s.name for s in slips]
#     if not slip_names:
#         return [], []

#     earnings = frappe.get_all(
#         "Salary Detail",
#         filters={
#             "parent": ["in", slip_names],
#             "parenttype": "Salary Slip",
#             "parentfield": "earnings",
#             # "do_not_include_in_total": 0
#         },
#         fields=["salary_component"]
#     )

#     deductions = frappe.get_all(
#         "Salary Detail",
#         filters={
#             "parent": ["in", slip_names],
#             "parenttype": "Salary Slip",
#             "parentfield": "deductions",
#             "do_not_include_in_total": 0
#         },
#         fields=["salary_component"]
#     )

#     used_earnings = {e.salary_component for e in earnings}
#     used_deductions = {d.salary_component for d in deductions}

#     return list(used_earnings), list(used_deductions)


# def get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
#     """
#     Define the report columns dynamically based on fixed/variable components.
#     """
#     base_columns = [
#         {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
#         {"label": "Salary Slip ID", "fieldname": "salary_slip_id", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
#         {"label": "Date of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
#         {"label": "Total Working Days", "fieldname": "total_working_days", "fieldtype": "Float", "width": 140},
#         {"label": "Absent Days", "fieldname": "absent_days", "fieldtype": "Float", "width": 120},
#         {"label": "Leave Without Pay", "fieldname": "leave_without_pay", "fieldtype": "Float", "width": 140},
#         {"label": "Total LOP Days", "fieldname": "total_lop_days", "fieldtype": "Float", "width": 130},
#         {"label": "Payment Days", "fieldname": "payment_days", "fieldtype": "Float", "width": 130},
#         {"label": "Arrear Days", "fieldname": "arrear_days", "fieldtype": "Float", "width": 120},
#         {"label": "Total Payment Days", "fieldname": "total_payment_days", "fieldtype": "Float", "width": 150},
#         {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
#     ]

#     fixed_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in fixed_earnings]
#     fixed_earning_total = [{"label": "Fixed Earnings Total", "fieldname": "fixed_earnings", "fieldtype": "Currency", "width": 150}]

#     variable_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in variable_earnings]
#     variable_earning_total = [{"label": "Variable Earnings Total", "fieldname": "variable_earnings", "fieldtype": "Currency", "width": 150}]

#     gross = [{"label": "Gross Pay", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 150}]

#     fixed_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in fixed_deductions]
#     fixed_deduction_total = [{"label": "Fixed Deductions Total", "fieldname": "fixed_deductions", "fieldtype": "Currency", "width": 150}]

#     variable_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in variable_deductions]
#     variable_deduction_total = [{"label": "Variable Deductions Total", "fieldname": "variable_deductions", "fieldtype": "Currency", "width": 150}]

#     totals = [
#         {"label": "Total Deductions", "fieldname": "total_deduction", "fieldtype": "Currency", "width": 150},
#         {"label": "Net Pay", "fieldname": "net_pay", "fieldtype": "Currency", "width": 150},
#     ]

#     return (
#         base_columns
#         + fixed_earning_cols + fixed_earning_total
#         + variable_earning_cols + variable_earning_total
#         + gross
#         + fixed_deduction_cols + fixed_deduction_total
#         + variable_deduction_cols + variable_deduction_total
#         + totals
#     )


# def get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
#     """
#     Fetch salary slip data and map component amounts to dynamic columns.
#     """
#     flt = {"docstatus": ["in", [0, 1]]}
#     if filters.get("company"):
#         flt["company"] = filters["company"]
#     if filters.get("employee"):
#         flt["employee"] = filters["employee"]
#     if filters.get("custom_payroll_period"):
#         flt["custom_payroll_period"] = filters["custom_payroll_period"]
#     if filters.get("custom_month"):
#         flt["custom_month"] = filters["custom_month"]

#     salary_slips = frappe.get_all(
#         "Salary Slip",
#         filters=flt,
#         fields=[
#             "name", "employee", "employee_name", "company", "custom_payroll_period",
#             "gross_pay", "total_deduction", "net_pay", "total_working_days",
#             "absent_days", "leave_without_pay", "payment_days", "custom_lop_reversal_days",
#             "custom_month", "custom_statutory_grosspay", "custom_net_pay_amount"
#         ]
#     )

#     if not salary_slips:
#         return []

#     slip_names = [s.name for s in salary_slips]

#     # Fetch earnings & deductions in bulk
#     earnings = frappe.get_all(
#         "Salary Detail",
#         filters={"parent": ["in", slip_names], "parenttype": "Salary Slip", "parentfield": "earnings", "do_not_include_in_total": 0},
#         fields=["parent", "salary_component", "amount"]
#     )
#     deductions = frappe.get_all(
#         "Salary Detail",
#         filters={"parent": ["in", slip_names], "parenttype": "Salary Slip", "parentfield": "deductions", "do_not_include_in_total": 0},
#         fields=["parent", "salary_component", "amount"]
#     )

#     # Employee join dates
#     employee_ids = list({s.employee for s in salary_slips})
#     employees = frappe.get_all("Employee", filters={"name": ["in", employee_ids]}, fields=["name", "date_of_joining"])
#     employee_map = {emp.name: emp.date_of_joining for emp in employees}

#     # Group earnings & deductions by Salary Slip
#     earnings_map = defaultdict(list)
#     for e in earnings:
#         earnings_map[e.parent].append(e)
#     deductions_map = defaultdict(list)
#     for d in deductions:
#         deductions_map[d.parent].append(d)

#     # Build final data
#     data = []
#     for slip in salary_slips:
#         total_lop_days = (slip.leave_without_pay or 0) + (slip.absent_days or 0)
#         total_payment_days = (slip.payment_days or 0) + (slip.custom_lop_reversal_days or 0)

#         row = {
#             "employee": slip.employee,
#             "employee_name": slip.employee_name,
#             "salary_slip_id": slip.name,
#             "date_of_joining": employee_map.get(slip.employee),
#             "total_working_days": slip.total_working_days,
#             "absent_days": slip.absent_days,
#             "leave_without_pay": slip.leave_without_pay,
#             "total_lop_days": total_lop_days,
#             "payment_days": slip.payment_days,
#             "arrear_days": slip.custom_lop_reversal_days,
#             "total_payment_days": total_payment_days,
#             "month": slip.custom_month,
#             "company": slip.company,
#             "custom_payroll_period": slip.custom_payroll_period,
#             "gross_pay": slip.custom_statutory_grosspay,
#             "total_deduction": slip.total_deduction,
#             "net_pay": slip.custom_net_pay_amount,
#             "fixed_earnings": 0,
#             "variable_earnings": 0,
#             "fixed_deductions": 0,
#             "variable_deductions": 0,
#         }

#         # Initialize component columns
#         for ec in fixed_earnings + variable_earnings:
#             row[frappe.scrub(ec)] = 0
#         for dc in fixed_deductions + variable_deductions:
#             row[frappe.scrub(dc)] = 0

#         # Map earnings
#         for e in earnings_map.get(slip.name, []):
#             row[frappe.scrub(e.salary_component)] = e.amount
#             comp = frappe.get_cached_doc("Salary Component", e.salary_component)
#             if comp.custom_component_sub_type == "Fixed":
#                 row["fixed_earnings"] += e.amount
#             else:
#                 row["variable_earnings"] += e.amount

#         # Map deductions
#         for d in deductions_map.get(slip.name, []):
#             row[frappe.scrub(d.salary_component)] = d.amount
#             comp = frappe.get_cached_doc("Salary Component", d.salary_component)
#             if comp.custom_component_sub_type == "Fixed":
#                 row["fixed_deductions"] += d.amount
#             else:
#                 row["variable_deductions"] += d.amount

#         data.append(row)

#     return data


# # ----------------------------
# # Main execute function
# # ----------------------------
# def execute(filters=None):
#     filters = filters or {}

#     # Get components used in Salary Slips
#     earning_components, deduction_components = get_used_components(filters)

#     # Split into Fixed / Variable and sort by sequence
#     fixed_earnings, variable_earnings = split_and_sort_components(earning_components)
#     fixed_deductions, variable_deductions = split_and_sort_components(deduction_components)

#     # Get report columns
#     columns = get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)

#     # Get report data
#     data = get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)

#     return columns, data





import frappe
from collections import defaultdict

def split_and_sort_components(components):
    """
    Split components into Fixed and Variable based on custom_component_sub_type
    and sort by custom_sequence.
    """
    fixed, variable = [], []
    comp_sequence_map = {}
    for c in components:
        comp = frappe.get_cached_doc("Salary Component", c)
        comp_sequence_map[c] = comp.custom_sequence or 9999
        if comp.custom_component_sub_type == "Fixed":
            fixed.append(c)
        else:
            variable.append(c)
    fixed.sort(key=lambda x: comp_sequence_map[x])
    variable.sort(key=lambda x: comp_sequence_map[x])
    return fixed, variable


def get_used_components(filters):
    """
    Fetch salary components actually used in selected Salary Slips
    considering do_not_include_in_total = 0
    """
    flt = {"docstatus": ["in", [0, 1]]}
    if filters.get("company"):
        flt["company"] = filters["company"]
    if filters.get("employee"):
        flt["employee"] = filters["employee"]
    if filters.get("custom_payroll_period"):
        flt["custom_payroll_period"] = filters["custom_payroll_period"]
    if filters.get("custom_month") and filters.get("custom_month") != "All":
        flt["custom_month"] = filters["custom_month"]

    if filters.get("custom_employment_type"):
        flt["custom_employment_type"] = filters["custom_employment_type"]

    slips = frappe.get_all("Salary Slip", filters=flt, fields=["name"])

    if not slips:
        return [], []
    slip_names = [s.name for s in slips]
    if not slip_names:
        return [], []

    earnings = frappe.get_all(
        "Salary Detail",
        filters={
            "parent": ["in", slip_names],
            "parenttype": "Salary Slip",
            "parentfield": "earnings",
        },
        fields=["salary_component"]
    )


    deductions = frappe.get_all(
        "Salary Detail",
        filters={
            "parent": ["in", slip_names],
            "parenttype": "Salary Slip",
            "parentfield": "deductions",
            "do_not_include_in_total": 0
        },
        fields=["salary_component"]
    )

    used_earnings = {e.salary_component for e in earnings}
    used_deductions = {d.salary_component for d in deductions}

    return list(used_earnings), list(used_deductions)


def get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
    """
    Define the report columns dynamically based on fixed/variable components.
    """
    base_columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Salary Slip ID", "fieldname": "salary_slip_id", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
        {"label": "Date of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
        {"label": "Total Working Days", "fieldname": "total_working_days", "fieldtype": "Float", "width": 140},
        {"label": "Absent Days", "fieldname": "absent_days", "fieldtype": "Float", "width": 120},
        {"label": "Leave Without Pay", "fieldname": "leave_without_pay", "fieldtype": "Float", "width": 140},
        {"label": "Total LOP Days", "fieldname": "total_lop_days", "fieldtype": "Float", "width": 130},
        {"label": "Payment Days", "fieldname": "payment_days", "fieldtype": "Float", "width": 130},
        {"label": "Arrear Days", "fieldname": "arrear_days", "fieldtype": "Float", "width": 120},
        {"label": "Total Payment Days", "fieldname": "total_payment_days", "fieldtype": "Float", "width": 150},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
    ]

    fixed_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in fixed_earnings]
    fixed_earning_total = [{"label": "Fixed Earnings Total", "fieldname": "fixed_earnings", "fieldtype": "Currency", "width": 150}]

    variable_earning_cols = [{"label": ec, "fieldname": frappe.scrub(ec), "fieldtype": "Currency", "width": 120} for ec in variable_earnings]
    variable_earning_total = [{"label": "Variable Earnings Total", "fieldname": "variable_earnings", "fieldtype": "Currency", "width": 150}]

    gross = [{"label": "Gross Pay", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 150}]

    fixed_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in fixed_deductions]
    fixed_deduction_total = [{"label": "Fixed Deductions Total", "fieldname": "fixed_deductions", "fieldtype": "Currency", "width": 150}]

    variable_deduction_cols = [{"label": dc, "fieldname": frappe.scrub(dc), "fieldtype": "Currency", "width": 120} for dc in variable_deductions]
    variable_deduction_total = [{"label": "Variable Deductions Total", "fieldname": "variable_deductions", "fieldtype": "Currency", "width": 150}]

    totals = [
        {"label": "Total Deductions", "fieldname": "total_deduction", "fieldtype": "Currency", "width": 150},
        {"label": "Net Pay", "fieldname": "net_pay", "fieldtype": "Currency", "width": 150},
    ]

    return (
        base_columns
        + fixed_earning_cols + fixed_earning_total
        + variable_earning_cols + variable_earning_total
        + gross
        + fixed_deduction_cols + fixed_deduction_total
        + variable_deduction_cols + variable_deduction_total
        + totals
    )


def get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions):
    """
    Fetch salary slip data and map component amounts to dynamic columns.
    """
    flt = {"docstatus": ["in", [0, 1]]}
    if filters.get("company"):
        flt["company"] = filters["company"]
    if filters.get("employee"):
        flt["employee"] = filters["employee"]
    if filters.get("custom_payroll_period"):
        flt["custom_payroll_period"] = filters["custom_payroll_period"]
    if filters.get("custom_month") and filters.get("custom_month") != "All":
        flt["custom_month"] = filters["custom_month"]

    if filters.get("custom_employment_type"):
        flt["custom_employment_type"] = filters["custom_employment_type"]

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=flt,
        fields=[
            "name", "employee", "employee_name", "company", "custom_payroll_period",
            "gross_pay", "total_deduction", "net_pay", "total_working_days",
            "absent_days", "leave_without_pay", "payment_days", "custom_lop_reversal_days",
            "custom_month", "custom_statutory_grosspay", "custom_net_pay_amount","custom_employment_type"
        ]
    )

    if not salary_slips:
        return []

    slip_names = [s.name for s in salary_slips]

    earnings = frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", slip_names], "parenttype": "Salary Slip", "parentfield": "earnings"},
        fields=["parent", "salary_component", "amount"]
    )
    deductions = frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", slip_names], "parenttype": "Salary Slip", "parentfield": "deductions", "do_not_include_in_total": 0},
        fields=["parent", "salary_component", "amount"]
    )

    employee_ids = list({s.employee for s in salary_slips})
    employees = frappe.get_all("Employee", filters={"name": ["in", employee_ids]}, fields=["name", "date_of_joining"])
    employee_map = {emp.name: emp.date_of_joining for emp in employees}

    earnings_map = defaultdict(list)
    for e in earnings:
        earnings_map[e.parent].append(e)
    deductions_map = defaultdict(list)
    for d in deductions:
        deductions_map[d.parent].append(d)

    data = []
    for slip in salary_slips:
        total_lop_days = (slip.leave_without_pay or 0) + (slip.absent_days or 0)
        total_payment_days = (slip.payment_days or 0) + (slip.custom_lop_reversal_days or 0)

        row = {
            "employee": slip.employee,
            "employee_name": slip.employee_name,
            "salary_slip_id": slip.name,
            "date_of_joining": employee_map.get(slip.employee),
            "total_working_days": slip.total_working_days,
            "absent_days": slip.absent_days,
            "leave_without_pay": slip.leave_without_pay,
            "total_lop_days": total_lop_days,
            "payment_days": slip.payment_days,
            "arrear_days": slip.custom_lop_reversal_days,
            "total_payment_days": total_payment_days,
            "month": slip.custom_month,
            "company": slip.company,
            "custom_payroll_period": slip.custom_payroll_period,
            "gross_pay": slip.custom_statutory_grosspay,
            "total_deduction": slip.total_deduction,
            "net_pay": slip.custom_net_pay_amount,
            "fixed_earnings": 0,
            "variable_earnings": 0,
            "fixed_deductions": 0,
            "variable_deductions": 0,
        }

        for ec in fixed_earnings + variable_earnings:
            row[frappe.scrub(ec)] = 0
        for dc in fixed_deductions + variable_deductions:
            row[frappe.scrub(dc)] = 0

        for e in earnings_map.get(slip.name, []):
            row[frappe.scrub(e.salary_component)] = e.amount
            comp = frappe.get_cached_doc("Salary Component", e.salary_component)
            if comp.custom_component_sub_type == "Fixed":
                row["fixed_earnings"] += e.amount
            else:
                row["variable_earnings"] += e.amount

        for d in deductions_map.get(slip.name, []):
            row[frappe.scrub(d.salary_component)] = d.amount
            comp = frappe.get_cached_doc("Salary Component", d.salary_component)
            if comp.custom_component_sub_type == "Fixed":
                row["fixed_deductions"] += d.amount
            else:
                row["variable_deductions"] += d.amount

        data.append(row)

    return data

def execute(filters=None):
    filters = filters or {}

    earning_components, deduction_components = get_used_components(filters)

    fixed_earnings, variable_earnings = split_and_sort_components(earning_components)
    fixed_deductions, variable_deductions = split_and_sort_components(deduction_components)

    columns = get_columns(fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)

    data = get_data(filters, fixed_earnings, variable_earnings, fixed_deductions, variable_deductions)

    return columns, data
