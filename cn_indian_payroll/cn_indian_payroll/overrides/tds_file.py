

import frappe
from frappe.utils import now

@frappe.whitelist()
def month_wise_tds_value(company=None, payroll_period=None, quarter_ended=None):
    if not (company and payroll_period and quarter_ended):
        return {"error": "Missing required parameters"}

    # Get fiscal year dates
    fy_doc = frappe.get_doc("Payroll Period", payroll_period)
    fy_start = fy_doc.start_date
    fy_end = fy_doc.end_date

    year_start = fy_start.year
    next_year = fy_end.year

    final_array = []

    # ---------- Define quarter months ----------
    if quarter_ended == "Q1 (Apr-Jun)":
        months = [
            ("April", f"{year_start}-04-01", f"{year_start}-04-30"),
            ("May", f"{year_start}-05-01", f"{year_start}-05-31"),
            ("June", f"{year_start}-06-01", f"{year_start}-06-30")
        ]

    elif quarter_ended == "Q2 (Jul-Sep)":
        months = [
            ("July", f"{year_start}-07-01", f"{year_start}-07-31"),
            ("August", f"{year_start}-08-01", f"{year_start}-08-31"),
            ("September", f"{year_start}-09-01", f"{year_start}-09-30")
        ]

    elif quarter_ended == "Q3 (Oct-Dec)":
        months = [
            ("October", f"{year_start}-10-01", f"{year_start}-10-31"),
            ("November", f"{year_start}-11-01", f"{year_start}-11-30"),
            ("December", f"{year_start}-12-01", f"{year_start}-12-31")
        ]

    elif quarter_ended == "Q4 (Jan-Mar)":
        months = [
            ("January", f"{next_year}-01-01", f"{next_year}-01-31"),
            ("February", f"{next_year}-02-01", f"{next_year}-02-28"),
            ("March", f"{next_year}-03-01", f"{next_year}-03-31")
        ]

    else:
        return {"error": "Invalid quarter"}

    # ---------- Loop each month ----------
    for month_name, start_date, end_date in months:
        total_tax = 0
        total_education_cess = 0
        total_surcharge = 0

        employee_breakup = []  # store employee-level details

        # Fetch salary slips for the month
        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={
                "company": company,
                "custom_payroll_period": payroll_period,
                "docstatus": 1,
                "start_date": ["between", [start_date, end_date]]
            },
            fields=[
                "name", "employee", "employee_name",
                "current_month_income_tax",
                "custom_education_cess",
                "custom_surcharge"
            ]
        )

        # Sum up for the month and employee
        for slip in salary_slips:
            tds = slip.current_month_income_tax or 0
            edu_cess = slip.custom_education_cess or 0
            surcharge = slip.custom_surcharge or 0

            total_tax += tds
            total_education_cess += edu_cess
            total_surcharge += surcharge

            get_employee = frappe.get_doc("Employee", slip.employee)



            employee_breakup.append({
                "employee": slip.employee,
                "employee_name": slip.employee_name,
                "tds": round(tds, 2),
                "education_cess": round(edu_cess, 2),
                "surcharge": round(surcharge, 2),
                "total_amount": round(tds + edu_cess + surcharge, 2),
                "employee_pan": get_employee.pan_number if get_employee.pan_number else 0
            })


        # Add month-level summary
        final_array.append({
            "month": month_name,
            "start_date": start_date,
            "end_date": end_date,
            "total_tds": round(total_tax, 2),
            "total_education_cess": round(total_education_cess, 2),
            "total_surcharge": round(total_surcharge, 2),
            "slip_count": len(salary_slips),
            "employees": employee_breakup
        })

    # ---------- Return Final ----------
    return {
        "quarter": quarter_ended,
        "data": final_array
    }



import frappe
import json


@frappe.whitelist()
def insert_tds_details(challan_data, annexure_data, fieldData):
    try:

        if isinstance(fieldData, str):
            fieldData = frappe.parse_json(fieldData)
        if isinstance(challan_data, str):
            challan_data = frappe.parse_json(challan_data)
        if isinstance(annexure_data, str):
            annexure_data = frappe.parse_json(annexure_data)

        payroll_period = fieldData.get("payroll_period")
        quarter = fieldData.get("quarter_ended")
        company = fieldData.get("company")
        fiscal_year = fieldData.get("fiscal_year")


        # frappe.msgprint(str(payroll_period))
        # frappe.msgprint(str(quarter))
        # frappe.msgprint(str(company))
        # frappe.msgprint(str(fiscal_year))





        if not (payroll_period and quarter and company and fiscal_year):
            frappe.throw("Payroll Period, Quarter, and Company are mandatory.")


        get_existing_tds = frappe.get_all(
            "TDS RETURN",
            filters={
                "company": company,
                "quarter_ended": quarter,
                "payroll_period": payroll_period
            },
            pluck="name"
        )


        if not get_existing_tds:

            frappe.msgprint(str("YES"))

            tds_doc = frappe.new_doc("TDS RETURN")
            tds_doc.company = company
            quarter_map = {
                "Q1 (Apr-Jun)": "Q1",
                "Q2 (Jul-Sep)": "Q2",
                "Q3 (Oct-Dec)": "Q3",
                "Q4 (Jan-Mar)": "Q4"
            }

            tds_doc.for_quarter_ended = quarter_map.get(quarter, quarter)
            tds_doc.quarter_ended=quarter
            tds_doc.tan=fieldData.get("assessment_year")
            tds_doc.last_tan=fieldData.get("tan_number")
            tds_doc.pan=fieldData.get("pan_number")
            tds_doc.type_of_deductor=fieldData.get("type_of_deductor")
            tds_doc.financial_year=fieldData.get("fiscal_year")
            tds_doc.assessment_year=fieldData.get("assessment_year")
            tds_doc.is_revised_return=fieldData.get("is_revised_return")
            tds_doc.original_return_receipt_no=fieldData.get("original_receipt_number")
            tds_doc.receipt_number_of_previous_return=fieldData.get("original_prevoius_receipt_number")
            tds_doc.payroll_period = payroll_period




            tds_doc.deductor_name=fieldData.get("deductor_name")
            tds_doc.branch_division=fieldData.get("branch")
            tds_doc.ministry_dept_name_others=fieldData.get("ministry_name_other")
            tds_doc.ddo_code=fieldData.get("ddo_code")
            tds_doc.ddo_registration_no=fieldData.get("ddo_registration_number")
            tds_doc.flat_no=fieldData.get("flat_no")
            tds_doc.road_street_lane=fieldData.get("road_name")
            tds_doc.city_district=fieldData.get("city_district")
            tds_doc.telephone_no=fieldData.get("telephone_number")
            tds_doc.telephone_no_alternate=fieldData.get("telephone_number_alternate")
            tds_doc.ain_of_paoitociddo=fieldData.get("account_office")
            tds_doc.ministry_dept_name=fieldData.get("ministry_name")
            tds_doc.state=fieldData.get("state")
            tds_doc.pao_code=fieldData.get("pao_code")
            tds_doc.pao_registration_no=fieldData.get("pao_registration_number")
            tds_doc.premises_name=fieldData.get("premises_name")
            tds_doc.area_location=fieldData.get("area_location")
            tds_doc.pincode=fieldData.get("pin_code")
            tds_doc.email=fieldData.get("email")
            tds_doc.email_alternate=fieldData.get("email_alternate")
            tds_doc.gstn=fieldData.get("gst")
            tds_doc.has_address_changed=fieldData.get("address_chnages")


            tds_doc.responsible_person_name=fieldData.get("responsible_person_name")
            tds_doc.designation=fieldData.get("designation")
            tds_doc.responsible_person_flat_no=fieldData.get("flat_no_responsible")
            tds_doc.responsible_person_road_street_lane=fieldData.get("road_street_responsible")
            tds_doc.responsible_person_pincode=fieldData.get("pin_code_responsible")
            tds_doc.responsible_person_state=fieldData.get("state_responsible")
            tds_doc.responsible_person_email=fieldData.get("email_responsible")
            tds_doc.responsible_person_mobile_no=fieldData.get("mobile_responsible")
            tds_doc.responsible_person_address_changed=fieldData.get("address_chnages")
            tds_doc.responsible_person_pan=fieldData.get("responsible_person_pan")
            tds_doc.responsible_person_premises_name=fieldData.get("premises_name_responsible")
            tds_doc.responsible_person_area_location=fieldData.get("area_locality_responsible")
            tds_doc.responsible_person_city_district=fieldData.get("town_city_responsible")
            tds_doc.responsible_person_telephone_no=fieldData.get("telephone_responsible")
            tds_doc.responsible_person_email_alternate=fieldData.get("email_alternate")
            tds_doc.has_regular_statement_filed=fieldData.get("change_in_person")
            tds_doc.receipt_no_of_earlier_statement=fieldData.get("original_prevoius_receipt_number")



    #         # --- Append Challan child table ---
            for challan in challan_data:
                tds_doc.append("challan_details", {
                    "sr_no":  challan.get("Sr. No."),
                    "update_mode_for_challan":challan.get("Update Mode for Challan"),
                    "tds":challan.get("TDS (₹)"),
                    "education_cess":challan.get("Education Cess (₹)"),
                    "fee":challan.get("Fee (₹)"),
                    "last_total_tax_deposited":challan.get("Last Total Tax Deposited (₹)"),
                    "cheque_dd_no":challan.get("Cheque / DD No."),
                    "bsr_code_receipt_number_of_form_24g":challan.get("BSR Code / Receipt No. (Form 24G)"),
                    "date_deposited_through_challan_voucher":challan.get("Date Deposited (Challan / Voucher)"),
                    "challan_serial_no_ddo_serial_no_of_form_24g":challan.get("Last DDO / Transfer Voucher / Challan Serial No."),
                    "interest_to_be_allocated":challan.get("Interest Allocated (₹)"),
                    "others_amount":challan.get("Others (₹)"),
                    "challan_balance":challan.get("Challan Balance"),
                    "section_code":challan.get("Section Code"),
                    "surcharge":challan.get("Surcharge (₹)"),
                    "interest":challan.get("Interest (₹)"),
                    "penalty_others":challan.get("Penalty / Others (₹)"),
                    "total_amount_deposited_as_per_challan":challan.get("Total Amount Deposited (₹)"),
                    "bsr_code_24g_receipt_no":challan.get("Last BSR Code / 24G Receipt No."),
                    "last_date_on_which_tax_deposited":challan.get("Last Date Tax Deposited"),
                    "last_ddo_transfer_voucher_challan_serial_no":challan.get("Last DDO / Transfer Voucher / Challan Serial No."),
                    "mode_of_deposit_through_book_adjustment":challan.get("Mode of Deposit (Book Adjustment)"),
                    "minor_head_of_challan":challan.get("Minor Head of Challan"),

                })

            # --- Append Annexure child table ---
            for annex in annexure_data:
                tds_doc.append("deductee_details", {
                    "challan_serial_no":annex.get("Challan Serial No."),

                    "bsr_code_where_tax_deposited": annex.get("BSR Code where Tax Deposited"),
                    "date_on_which_tax_deposited": annex.get("Date on which Tax Deposited"),
                    "section_under_which_payment_made": annex.get("Section Under Which Payment Made"),
                    "total_tds_to_be_allocated":annex.get("TDS (₹)"),
                    "others": annex.get("Others (₹)"),
                    "employee_reference_no":annex.get("Employee Reference No."),
                    "pan_of_the_employee":annex.get("PAN of the Employee"),
                    "date_of_payment_credit":annex.get("Date on which Tax Deposited"),
                    "tds_deducted":annex.get("TDS (₹)"),
                    "health_and_education_cess":annex.get("Health & Education Cess (₹)"),
                    "last_total_tax_deducted":annex.get("Last Total Tax Deducted (₹)"),
                    "total_tax_deposited":annex.get("Total Allocated Amount (₹)"),
                    "update_mode_for_deductee":annex.get("Update Mode for Deductee"),
                    "transfer_voucher_challan_serial_no":annex.get("Transfer Voucher/Challan Serial No."),
                    "interest":annex.get("Interest (₹)"),
                    "total_allocated_amount":annex.get("Total Allocated Amount (₹)"),
                    "last_pan_of_employee":annex.get("Last PAN of Employee"),
                    "name_of_the_employee":annex.get("Name of Employee"),
                    "amount_paid_credited":annex.get("Amount Paid/Credited (₹)"),
                    "surcharge_deducted":annex.get("Surcharge (₹)"),
                    "total_tax_deducted":annex.get("Total Tax Deducted (₹)"),
                    "last_total_tax_deposited":annex.get("Last Total Tax Deposited (₹)"),
                    "date_of_deduction":annex.get("Date of Deduction"),
                    "certificate_number_u_s_197":annex.get("Certificate No. u/s 197"),
                    "remarks_for_non_deduction":annex.get("Remarks"),
                })


            tds_doc.insert()
            frappe.db.commit()

    #         return {
    #             "success": True,
    #             "tds_return": tds_doc.name,
    #             "message": f"TDS RETURN created for {company} ({quarter})"
    #         }

        else:
            # ✅ Update existing document (optional)
            existing_doc = frappe.get_doc("TDS RETURN", get_existing_tds[0])
            return {
                "success": False,
                "message": f"TDS RETURN already exists: {existing_doc.name}"
            }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Insert TDS RETURN Error")
        frappe.throw(f"Error inserting TDS RETURN: {str(e)}")
