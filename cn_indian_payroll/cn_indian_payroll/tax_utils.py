import frappe


def calculate_regime_tax(is_new=0,taxable_amount=0):
    total_tax = 0
    slabs = []
    rates = []
    slabs_doc=None
    if is_new==0:
         slabs_doc = frappe.get_doc("Income Tax Slab","Old Regime")
    else:
         slabs_doc=frappe.get_doc("Income Tax Slab","New Regime")
    for slab in slabs_doc.slabs:
        slabs.append(slab.from_amount)
        rates.append(slab.percent_deduction)
    total_slabs_idx=len(slabs)-1
    for i in range(total_slabs_idx):
        if i<total_slabs_idx:
            if taxable_amount >slabs[i+1]:
                total_tax=total_tax+(slabs[i+1]-slabs[i])*(rates[i]/100)
            else:
                total_tax=total_tax+(taxable_amount-slabs[i])*(rates[i]/100)
                break
        else:
            total_tax=total_tax+(taxable_amount-slabs[i])*(rates[i]/100)
    return total_tax

@frappe.whitelist()
def calculate_tax(doc_name=None,totalincome = None):
    emp_id,deduction = frappe.db.get_value('Employee Tax Exemption Declaration', doc_name, ['employee', 'total_declared_amount'])
    total_income=None
    # if totalincome:
    #     total_income = float(totalincome)
    # else:

    total_income_list = frappe.db.get_list('Salary Structure Assignment',
    filters={
        'employee': emp_id
    },
    fields=['total_earning'],
    order_by='from_date desc',
    limit=1,
    as_list=True
    )
    total_income = (total_income_list[0][0])*12
    
    taxable_amount = total_income-deduction
    old_regime_tax = 0
    new_regime_tax = 0
    if taxable_amount > 0:
        old_regime_tax = calculate_regime_tax(0,taxable_amount)
        new_regime_tax = calculate_regime_tax(1,total_income)
    old_cess = (4/100)*old_regime_tax
    new_cess = (4/100)*new_regime_tax
    template_dict = {"total_income":total_income,"deduction":deduction,"taxable_amount":taxable_amount-50000,"old_regime_tax":old_regime_tax,"new_regime_tax":new_regime_tax,"old_cess":old_cess,"new_cess":new_cess,"old_total_tax":old_regime_tax+old_cess,"new_total_tax":new_regime_tax+new_cess}  
    template =  frappe.render_template('cn_indian_payroll/cn_indian_payroll/tax_calculator.html', {"dict": template_dict})
    frappe.msgprint(template)

@frappe.whitelist()
def calculate_hra_exemption(emp_id,monthly_house_rent):
    # emp_id,monthly_house_rent = frappe.db.get_value('Employee Tax Exemption Declaration', doc_name, ['employee', 'monthly_house_rent'])
    sm_doc_name = frappe.db.get_list('Salary Structure Assignment',
        filters={
            'employee': emp_id
        },
        fields=['name'],
        order_by='from_date desc',
        limit=1,
        as_list=True
    )
    sm_doc = frappe.get_doc("Salary Structure Assignment",sm_doc_name[0][0])
    sm_data = {}
    for com in sm_doc.earnings:
        if com.salary_component =="Basic" or com.salary_component=="HRA":
            sm_data[com.salary_component]=com.amount*12
    rent_paid = monthly_house_rent*12
    hra_list = []
    hra_list.append(sm_data["HRA"])
    hra_list.append(sm_data["Basic"]*0.4)
    hra_list.append(float(rent_paid) - (float(sm_data["Basic"]*0.1)))
    hra_exemption = min(hra_list)
    return hra_exemption

@frappe.whitelist()
def income_tax_calculator_template(total_income,deduction):
    taxable_income = float(total_income)-float(deduction)
    if taxable_income > 0:
        old_regime_tax = calculate_regime_tax(0,float(taxable_income))
        new_regime_tax = calculate_regime_tax(1,float(total_income)-50000)
        old_cess = (4/100)*old_regime_tax
        new_cess = (4/100)*new_regime_tax
        template_dict = {"total_income":total_income,"deduction":deduction,"taxable_amount":taxable_income,"old_regime_tax":old_regime_tax,"new_regime_tax":new_regime_tax,"old_cess":old_cess,"new_cess":new_cess,"old_total_tax":old_regime_tax+old_cess,"new_total_tax":new_regime_tax+new_cess}  
        template =  frappe.render_template('cn_indian_payroll/cn_indian_payroll/tax_calculator.html', {"dict": template_dict})
        return template
    else:
        return "No Data Found"
