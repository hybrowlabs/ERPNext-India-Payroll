# # Copyright (c) 2024, Hybrowlabs technologies and contributors
# # For license information, please see license.txt

# import frappe









# columns = [
    
#     {"fieldname": "ss_id", "label": "Salary Slip ID", "fieldtype": "Data", "width": 150},
    
    
    
#     {"fieldname": "employee", "label": "Employee ID", "fieldtype": "Data", "width": 150},
#     {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
#     {"fieldname": "income_tax_slab", "label": "Income Tax Slab", "fieldtype": "Data", "width": 150},
    
#     {"fieldname": "working_days", "label": "Working Days", "fieldtype": "Data", "width": 150},
#     {"fieldname": "payment_days", "label": "Payment Days", "fieldtype": "Data", "width": 150},
#     {"fieldname": "LOP", "label": "LOP", "fieldtype": "Data", "width": 150},
    
#      {"fieldname": "start_date", "label": "Start Date", "fieldtype": "Date", "width": 150},
#       {"fieldname": "end_date", "label": "End Date", "fieldtype": "Date", "width": 150},
    
    
#     {"fieldname": "basic", "label": "Basic", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "hra", "label": "HRA", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "twa_dfi", "label": "TWA DFI", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "uniform_allowance", "label": "Uniform Allowance", "fieldtype": "Currency", "width": 150},
#     {"fieldname": "medical_allowance", "label": "Medical Allowance", "fieldtype": "Currency", "width": 150},
#     {"fieldname": "food_coupon", "label": "Food Coupon", "fieldtype": "Currency", "width": 150},
#     {"fieldname": "heema", "label": "HEEMA", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "bonus", "label": "Bonus", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "bonus_accrual", "label": "Bonus Accrual", "fieldtype": "Currency", "width": 100},
    
#     {"fieldname": "petrol_reimbursement", "label": "Petrol Reimbursement", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "vehicle_maintenance_reimbursement", "label": "Vehicle Maintenance Reimbursement", "fieldtype": "Currency", "width": 250},
#     {"fieldname": "driver_salary_reimbursement", "label": "Driver Salary Reimbursement", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "leave_travel_allowance", "label": "Leave Travel Allowance", "fieldtype": "Currency", "width": 200},
    
    
#     {"fieldname": "car_perquisite", "label": "Car Perquisite", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "driver_perquisite", "label": "Driver Perquisite", "fieldtype": "Currency", "width": 200},
    
    
#     {"fieldname": "employee_provident_fund", "label": "Employee Provident Fund", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "nps", "label": "NPS", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "esic", "label": "ESIC", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "bonus_deduction", "label": "Bonus Deduction", "fieldtype": "Currency", "width": 150},
   

#     {"fieldname": "pt_g", "label": "Professional Tax (Gujarat)", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "pt_m", "label": "Professional Tax (Maharashtra)", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "pt_an", "label": "Professional Tax (Andrapradesh)", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "pt_w", "label": "Professional Tax (West Bengal)", "fieldtype": "Currency", "width": 200},
#     {"fieldname": "pt_kar", "label": "Professional Tax (Karnataka)", "fieldtype": "Currency", "width": 200},
    
    
#     {"fieldname": "income_tax", "label": "Income Tax", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "gross_pay", "label": "Gross Pay", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "net_pay", "label": "Net Pay", "fieldtype": "Currency", "width": 100},
#     {"fieldname": "total_deduction", "label": "Total Deduction", "fieldtype": "Currency", "width": 150},
    
    
    
     
    
    
    
# ]











# def get_salary_slips(filters=None):
#     if filters is None:
#         filters = {}

#     conditions = {}
#     if filters.get("employee"):
#         conditions["employee"] = filters["employee"]
        
#     if filters.get("from_date"):
#         conditions["start_date"] = (">=", filters["from_date"])
        
#     if filters.get("to_date"):
#         conditions["end_date"] = ("<=", filters["to_date"])
        
#     if filters.get("income_tax"):
#         conditions["custom_income_tax_slab"] = filters["income_tax"]
        

# frappe.msgprint(str(conditions))
        
        
        
        
#     # data = frappe.get_list(
#     #     'Salary Slip',
#     #     fields=["*"],
#     #     filters=conditions,
#     #     order_by="name DESC"
#     # )
   
#     # return data
    
# # ss_id=[]   
# # total_working_days=[]
# # payment_days=[]
# # leave_without_pay=[]
# # employee = []
# # employee_name = []
# # basic = []
# # hra = []
# # twa = []  
# # uniform = []
# # medical = []
# # food_coupon = []
# # heema = []

# # fuel = []  
# # driver = [] 
# # vehicle=[]
# # lta = []  

# # epf=[]
# # nps=[]
# # esic=[]

# # pt_g=[]
# # pt_m=[]
# # pt_an=[]
# # pt_w=[]
# # pt_kar=[]
# # income_tax_slab=[]

# # total_deduction=[]
# # net_pay=[]
# # gross_pay=[]
# # income_tax=[]

# # car_perquisite=[]
# # driver_perquisite=[]
# # start_date=[]
# # end_date=[]

# # bonus_deduction=[]
# # bonus=[]
# # bonus_accrual=[]

# # data=[]

# # lead_data = get_salary_slips(filters)

# # for slip in lead_data:
# #     doc = frappe.get_doc('Salary Slip', slip.name)
# #     employee.append(doc.employee)
# #     employee_name.append(doc.employee_name)
# #     total_deduction.append(doc.total_deduction)
# #     net_pay.append(doc.net_pay)
    
# #     ss_id.append(doc.name) 
# #     total_working_days.append(doc.total_working_days) 
# #     payment_days.append(doc.payment_days) 
# #     leave_without_pay.append(doc.leave_without_pay) 
# #     gross_pay.append(doc.custom_statutory_grosspay)
    
# #     income_tax_slab.append(doc.custom_income_tax_slab)
   
# #     start_date.append(doc.start_date)
# #     end_date.append(doc.end_date)
    
# #     for earning in doc.earnings:
# #         if earning.salary_component == "Basic":
# #             basic.append(earning.amount)
# #         if earning.salary_component == "House Rent Allowance":
# #             hra.append(earning.amount)
# #         if earning.salary_component == "TWA-DFI":  
# #             twa.append(earning.amount)
        
# #         if earning.salary_component == "Uniform":
# #             uniform.append(earning.amount)
# #         if earning.salary_component == "Medical":
# #             medical.append(earning.amount)
# #         if earning.salary_component == "Food Coupon":
# #             food_coupon.append(earning.amount)
# #         if earning.salary_component == "HEEMA":
# #             heema.append(earning.amount)
# #         if earning.salary_component == "Petrol Reimbursement":
# #             fuel.append(earning.amount)
# #         if earning.salary_component == "Vehicle Maintenance Reimbursement":
# #             vehicle.append(earning.amount)
# #         if earning.salary_component == "Driver Salary Reimbursement":
# #             driver.append(earning.amount)
# #         if earning.salary_component == "Leave Travel Allowance":
# #             lta.append(earning.amount)
# #         if earning.salary_component == "Car Perquisite":
# #             car_perquisite.append(earning.amount)
# #         if earning.salary_component == "Driver Perquisite":
# #             driver_perquisite.append(earning.amount)
            
# #         if earning.salary_component=="Bonus":
# #             bonus.append(earning.amount)
            
# #         if earning.salary_component =="Bonus (Accrual)":
# #             bonus_accrual.append(earning.amount)    
            
# #     for deduction in doc.deductions:
# #         if deduction.salary_component == "Employee Provident Fund":
# #             epf.append(deduction.amount)
# #         if deduction.salary_component == "NPS":
# #             nps.append(deduction.amount)
# #         if deduction.salary_component == "ESIC":
# #             esic.append(deduction.amount)
# #         if deduction.salary_component == "Professional Tax (Gujarat)":
# #             pt_g.append(deduction.amount)
# #         if deduction.salary_component == "Income Tax":
# #             income_tax.append(deduction.amount)
            
# #         if deduction.salary_component=="Bonus Deduction":
            
# #             bonus_deduction.append(deduction.amount)
            
# #         if deduction.salary_component=="Professional Tax (Maharashtra)":
# #             pt_m.append(deduction.amount)
            
# #         if deduction.salary_component=="Professional Tax (Andra Pradesh)":
# #             pt_an.append(deduction.amount)
        
        
# #         if deduction.salary_component=="Professional Tax ( West Bengal)":
# #             pt_w.append(deduction.amount)
        
        
# #         if deduction.salary_component=="Professional Tax (Karnata)":
# #             pt_kar.append(deduction.amount)
   
            
            

   

# # max_length = max(len(employee), len(employee_name), len(basic), len(hra), len(twa),
# #                  len(uniform), len(medical), len(food_coupon), len(heema))

# # employee.extend([''] * (max_length - len(employee)))
# # employee_name.extend([''] * (max_length - len(employee_name)))
# # basic.extend([0] * (max_length - len(basic)))
# # hra.extend([0] * (max_length - len(hra)))
# # twa.extend([0] * (max_length - len(twa)))
# # uniform.extend([0] * (max_length - len(uniform)))
# # medical.extend([0] * (max_length - len(medical)))
# # food_coupon.extend([0] * (max_length - len(food_coupon)))
# # heema.extend([0] * (max_length - len(heema)))  
# # fuel.extend([0] * (max_length - len(fuel)))  
# # vehicle.extend([0] * (max_length - len(vehicle)))  
# # driver.extend([0] * (max_length - len(driver)))  
# # lta.extend([0] * (max_length - len(lta))) 
# # nps.extend([0] * (max_length - len(nps)))  
# # esic.extend([0] * (max_length - len(esic)))  
# # pt_g.extend([0] * (max_length - len(pt_g)))  
# # income_tax.extend([0] * (max_length - len(income_tax))) 
# # epf.extend([0] * (max_length - len(epf)))
# # car_perquisite.extend([0] * (max_length - len(car_perquisite)))
# # driver_perquisite.extend([0] * (max_length - len(driver_perquisite)))
# # bonus_deduction.extend([0] * (max_length - len(bonus_deduction)))
# # bonus.extend([0] * (max_length - len(bonus)))
# # bonus_accrual.extend([0] * (max_length - len(bonus_accrual)))
# # pt_m.extend([0] * (max_length - len(pt_m)))
# # pt_an.extend([0] * (max_length - len(pt_an)))
# # pt_w.extend([0] * (max_length - len(pt_w)))
# # pt_kar.extend([0] * (max_length - len(pt_kar)))



            
            
   

# # for k in range(len(employee)):
# #     data.append([ss_id[k],employee[k], employee_name[k],income_tax_slab[k],total_working_days[k],payment_days[k],leave_without_pay[k],start_date[k],end_date[k], basic[k],hra[k],twa[k],uniform[k],medical[k],food_coupon[k],heema[k],bonus[k],bonus_accrual[k],fuel[k],vehicle[k],driver[k],lta[k],car_perquisite[k],driver_perquisite[k],epf[k],nps[k],esic[k],bonus_deduction[k],pt_g[k],pt_m[k],pt_an[k],pt_w[k],pt_kar[k],income_tax[k],gross_pay[k],net_pay[k],total_deduction[k]])

# # def execute(filters=None):
# #     return columns, data
    

# # data=columns,data,None,None,None
    


