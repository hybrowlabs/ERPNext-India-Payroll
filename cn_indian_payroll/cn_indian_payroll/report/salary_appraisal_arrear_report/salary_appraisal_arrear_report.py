def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


# ---------------------------------------------------
# COLUMNS
# ---------------------------------------------------
def get_columns():
    columns = [
        col("Sr. No", "sr_no", "Int", 60),
        col("Emp Code", "emp_code", "Data", 90),
        col("ERP Code", "erp_code", "Data", 90),
        col("Name", "name", "Data", 120),
        col("DOJ", "doj", "Data", 90),
        # ---- SUMMARY COLUMNS ----
        col("New CTC (2025)", "new_ctc", "Currency", 130),
        col("Old CTC (2024)", "old_ctc", "Currency", 130),
        col("CTC Diff", "ctc_diff", "Currency", 120),
        col("Attendance Total", "attendance_total", "Float", 130),
        col("Arrears Total", "arrears_total", "Currency", 130),
    ]

    # ---- DETAILED SECTIONS ----
    columns += ctc_columns("2025", "CTC 2025")
    columns += ctc_columns("2024", "CTC 2024")
    columns += ctc_columns("diff", "Diff")

    # ---- ATTENDANCE ----
    columns += [
        col("04/25", "apr_25", "Float", 70),
        col("05/25", "may_25", "Float", 70),
        col("06/25", "jun_25", "Float", 70),
        col("07/25", "jul_25", "Float", 70),
    ]

    # ---- ARREARS ----
    columns += ctc_columns("arrear", "Arrears")

    return columns


def ctc_columns(prefix, label_prefix):
    components = [
        "Basic",
        "House Rent Allowance",
        "TWA-DFI",
        "Uniform",
        "Medical",
        "HEEMA",
        "Employee Provident Fund",
        "Bonus Deduction",
        "Monthly Bonus",
        "Food Coupon (Earning)",
        "NPS",
        "Leave Travel Allowance",
        "Petrol Reimbursement",
        "Vehicle Maintenance Reimbursement",
        "Driver Salary Reimbursement",
    ]

    return [
        col(f"{label_prefix} - {c}", f"{prefix}_{i}", "Currency", 140)
        for i, c in enumerate(components)
    ]


def col(label, fieldname, fieldtype, width):
    return {
        "label": label,
        "fieldname": fieldname,
        "fieldtype": fieldtype,
        "width": width,
    }


# ---------------------------------------------------
# DATA (HARD CODED)
# ---------------------------------------------------
def get_data():
    return [
        {
            "sr_no": 1,
            "emp_code": "57007",
            "erp_code": "1",
            "name": "A",
            "doj": "01-04-2024",
            # ---- SUMMARY VALUES ----
            "new_ctc": 421333,
            "old_ctc": 385333,
            "ctc_diff": 36000,
            "attendance_total": 122,
            "arrears_total": 139000,
            # ---- CTC 2025 ----
            "2025_0": 150967,
            "2025_1": 75483,
            "2025_2": 20000,
            "2025_3": 1250,
            "2025_4": 1250,
            "2025_5": 120074,
            "2025_6": 18116,
            "2025_7": 30193,
            "2025_8": 0,
            "2025_9": 2000,
            "2025_10": 7000,
            "2025_11": 5000,
            "2025_12": 0,
            "2025_13": 0,
            "2025_14": 0,
            # ---- CTC 2024 ----
            "2024_0": 138717,
            "2024_1": 69358,
            "2024_2": 20000,
            "2024_3": 1250,
            "2024_4": 1250,
            "2024_5": 109369,
            "2024_6": 16646,
            "2024_7": 27743,
            "2024_8": 0,
            "2024_9": 2000,
            "2024_10": 5000,
            "2024_11": 5000,
            "2024_12": 0,
            "2024_13": 0,
            "2024_14": 0,
            # ---- DIFF ----
            "diff_0": 12250,
            "diff_1": 6125,
            "diff_2": 0,
            "diff_3": 0,
            "diff_4": 0,
            "diff_5": 10705,
            "diff_6": 1470,
            "diff_7": 2450,
            "diff_8": 0,
            "diff_9": 0,
            "diff_10": 2000,
            "diff_11": 0,
            "diff_12": 0,
            "diff_13": 0,
            "diff_14": 0,
            # ---- ATTENDANCE ----
            "apr_25": 30,
            "may_25": 31,
            "jun_25": 30,
            "jul_25": 31,
            # ---- ARREARS ----
            "arrear_0": 49000,
            "arrear_1": 24500,
            "arrear_2": 0,
            "arrear_3": 0,
            "arrear_4": 0,
            "arrear_5": 42820,
            "arrear_6": 5880,
            "arrear_7": 9800,
            "arrear_8": 0,
            "arrear_9": 0,
            "arrear_10": 8000,
            "arrear_11": 0,
            "arrear_12": 0,
            "arrear_13": 0,
            "arrear_14": 0,
        }
    ]
