
import frappe
from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import EmployeeTaxExemptionDeclaration
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

from frappe.utils import flt
from hrms.hr.utils import (
	calculate_annual_eligible_hra_exemption,
	get_total_exemption_amount,
	validate_active_employee,
	validate_duplicate_exemption_for_payroll_period,
	validate_tax_declaration,
)

from datetime import datetime, timedelta
from datetime import date


import json
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta







class CustomEmployeeTaxExemptionDeclaration(EmployeeTaxExemptionDeclaration):


    # def validate(self):

    #     # self.validate_tax_declaration()
        

    #     super().validate()


    def before_save(self):

        if self.custom_tax_regime=="Old Regime":
            form_data = json.loads(self.custom_declaration_form_data or '{}')
            
            for k in self.declarations:
                if k.exemption_sub_category == "Employee Provident Fund (Auto)":
                    form_data['pfValue'] = round(k.amount)
                
                elif k.exemption_sub_category == "NPS Contribution by Employer":
                    form_data['nineNumber'] = round(k.amount)
                
                elif k.exemption_sub_category == "Tax on employment (Professional Tax)":
                    form_data['nineteenNumber'] = round(k.amount)
            
            self.custom_declaration_form_data = json.dumps(form_data)


        if self.custom_tax_regime=="New Regime":
            form_data = json.loads(self.custom_declaration_form_data or '{}')
            
            for k in self.declarations:
                if k.exemption_sub_category == "NPS Contribution by Employer":
                    form_data['nineNumber'] = round(k.amount)      
            
            self.custom_declaration_form_data = json.dumps(form_data)

       

    
            
                
        



    # def on_submit(self):
    #     self.insert_declaration_history()



    def before_update_after_submit(self):

        self.process_form_data()
        
        if self.custom_check==0:
            self.calculate_hra_exemption()
        
        self.calculate_hra_breakup()
        self.update_hra_breakup()
        self.update_tax_declaration()
        
        self.set_total_declared_amount()
        self.set_total_exemption_amount()
   
        self.show_tax_projection()





    def show_tax_projection(self):
        if self.employee:
            latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )

            if len(latest_salary_structure)>0:

                

                get_payroll=frappe.get_doc("Payroll Period",latest_salary_structure[0].custom_payroll_period)
                effective_start_date=latest_salary_structure[0].from_date
                payroll_end_date=get_payroll.end_date
                payroll_start_date=get_payroll.start_date

                start_date = max(effective_start_date, payroll_start_date)

                if isinstance(start_date, str):
                    start = datetime.strptime(start_date, "%Y-%m-%d").date()
                else:
                    start = start_date  # Already a date object

                if isinstance(payroll_end_date, str):
                    end = datetime.strptime(payroll_end_date, "%Y-%m-%d").date()
                else:
                    end = payroll_end_date  # Already a date object

                num_months = (end.year - start.year) * 12 + (end.month - start.month)+1



                title_array = [
                    
                    
                    "Current Taxable Earning",
                    "Future Taxable Earning",
                    "Total Perquisite",
                    "Total Taxable Income", 
                    "Total Exemption", 
                    "Standard Deduction", 
                    "Annual Taxable Income",
                    "Total Income",
                    "Rebate", 
                    "Total Tax on Income",
                    "Surcharge", 
                    "Education Cess",
                    "Tax Payable", 
                    "Tax Paid",
                    "Current Tax",
                    "Total Tax Deducted at source",
                    "Tax Payable / Refundable (14 - 15(A))",
                    "TDS For Future Month",
                    
                ]

                
                old_regime_values = []
                new_regime_values = []
                old_amount_sum=0
                new_amount_sum=0
                nps_amount=0
                bonus_amount=0
                epf_amount=0
                pt_amount=0
                salary_slip_count=0
                other_perquisite_amount=0
                basic_component_value_old=[]
                basic_component_value_new=[]

                future_old_amount=[]
                future_new_amount=[]

                #CAR PERQUISITE

                # if latest_salary_structure[0].custom__car_perquisite==1 and latest_salary_structure[0].custom_car_perquisite_as_per_rules:
                #     old_amount_sum+=latest_salary_structure[0].custom_car_perquisite_as_per_rules*num_months
                #     new_amount_sum+=latest_salary_structure[0].custom_car_perquisite_as_per_rules*num_months
                # else:
                #     old_amount_sum=0
                #     new_amount_sum=0


                # #DRIVER PERQUISITE
                # if latest_salary_structure[0].custom_driver_provided_by_company==1 and latest_salary_structure[0].custom_driver_perquisite_as_per_rules:
                #     old_amount_sum+=latest_salary_structure[0].custom_driver_perquisite_as_per_rules*num_months
                #     new_amount_sum+=latest_salary_structure[0].custom_driver_perquisite_as_per_rules*num_months
                # else:
                #     old_amount_sum=0
                #     new_amount_sum=0

                


                # #OTHER PERQUISITE
                # get_other_perquisite=frappe.get_doc("Salary Structure Assignment",latest_salary_structure[0].name)
                # if get_other_perquisite.custom_other_perquisites:
                #     for other_perquisite in get_other_perquisite.custom_other_perquisites:
                #         old_amount_sum+=other_perquisite.amount*num_months
                #         new_amount_sum+=other_perquisite.amount*num_months

                # else:
                #     old_amount_sum=0
                #     new_amount_sum=0

                

                # old_regime_values.append(old_amount_sum)
                # new_regime_values.append(new_amount_sum)

                # get_all_salary_slip = frappe.get_list(
                #     'Salary Slip',
                #     filters={
                #         'employee': self.employee,
                #         'custom_payroll_period': self.payroll_period,
                #         'docstatus': ['in', [0, 1]]
                #     },
                #     fields=['*'],
                #     order_by='posting_date desc'
                # )

                # # custom_posting_date = getdate(self.custom_posting_date)

                # if len(get_all_salary_slip) > 0:

                #     salary_slip_count=len(get_all_salary_slip)

                #     for salary_list in get_all_salary_slip:
                #         get_salary_doc = frappe.get_doc("Salary Slip", salary_list.name)

                #         for component in get_salary_doc.earnings:
                            
                #             taxable_component = frappe.get_doc("Salary Component", component.salary_component)

                #             #All BASIC TAXABLE COMPONENT 
                #             if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "All":
                #                 old_amount_sum+=component.amount
                #                 new_amount_sum+=component.amount

                                
                #                 basic_component_value_old.append(component.amount)
                #                 basic_component_value_new.append(component.amount)
                #             #BONUS
                #             if taxable_component.is_tax_applicable == 1 and taxable_component.custom_is_accrual == 1:
                #                 old_amount_sum+=component.amount
                #                 new_amount_sum+=component.amount

                                
                #                 basic_component_value_old.append(component.amount)
                #                 basic_component_value_new.append(component.amount)
                        
                                
                            
                #             #FOOD COUPON
                #             if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #                 taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "Old Regime":
                #                 old_amount_sum+=component.amount
                #                 basic_component_value_old.append(component.amount)
                                                                        
                #             if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #                 taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "New Regime":
                #                 new_amount_sum+=component.amount
                #                 basic_component_value_new.append(component.amount)

                #             #NPS FOR DECLARTION

                #             if taxable_component.is_tax_applicable == 1 and taxable_component.component_type == "NPS":
                #                 nps_amount+=component.amount

                            

                    
                            

                #         for deduction in get_salary_doc.deductions:
                                 
                #             taxable_component = frappe.get_doc("Salary Component", deduction.salary_component)
                #             if taxable_component.component_type == "EPF":

                #                     epf_amount+=deduction.amount
                                
                #             if taxable_component.component_type == "Professional Tax":
                #                     pt_amount+=deduction.amount

                #     # frappe.msgprint(str(basic_component_value_old))
                #     # frappe.msgprint(str(basic_component_value_new))

                #     old_standard_value=sum(basic_component_value_old)
                #     new_standard_value=sum(basic_component_value_new)
                    

                #     old_regime_values.append(round(old_standard_value))
                #     new_regime_values.append(round(new_standard_value))


                #     new_salary_slip = make_salary_slip(
                #     source_name=latest_salary_structure[0].salary_structure,
                #     employee=self.employee,
                #     print_format='Salary Slip Standard for CTC',
                #     # posting_date=latest_salary_structure[0].from_date
                #     )

                #     for new_earning in new_salary_slip.earnings:
                #         taxable_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                #         #STANDARD COMPONENT
                #         if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #             taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "All":
                #             old_amount_sum+=new_earning.amount*(num_months-salary_slip_count)
                #             new_amount_sum+=new_earning.amount*(num_months-salary_slip_count)

                #             future_old_amount.append(new_earning.amount*(num_months-salary_slip_count))
                #             future_new_amount.append(new_earning.amount*(num_months-salary_slip_count))


                #         #BONUS

                #         if taxable_component.is_tax_applicable == 1 and taxable_component.custom_is_accrual == 1:
                #             old_amount_sum+=new_earning.amount*(num_months-salary_slip_count)
                #             new_amount_sum+=new_earning.amount*(num_months-salary_slip_count)

                                
                #             future_old_amount.append(new_earning.amount*(num_months-salary_slip_count))
                #             future_new_amount.append(new_earning.amount*(num_months-salary_slip_count))
                        
                #         #FOOD COUPON
                        
                #         if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #             taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "Old Regime":
                #             old_amount_sum+=new_earning.amount*(num_months-salary_slip_count)  
                #             future_old_amount.append(new_earning.amount*(num_months-salary_slip_count))                              

                        
                #         if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #             taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "New Regime":
                #             new_amount_sum+=new_earning.amount*(num_months-salary_slip_count)
                #             future_new_amount.append(new_earning.amount*(num_months-salary_slip_count))

                        
                #         if taxable_component.is_tax_applicable == 1 and taxable_component.component_type == "NPS":
                #                 nps_amount+=new_earning.amount*(num_months-salary_slip_count)



                #     for deduction in get_salary_doc.deductions:
                                 
                #         taxable_component = frappe.get_doc("Salary Component", deduction.salary_component)
                #         if taxable_component.component_type == "EPF":

                #             epf_amount+=deduction.amount*(num_months-salary_slip_count)
                                
                #         if taxable_component.component_type == "Professional Tax":
                #             pt_amount+=deduction.amount*(num_months-salary_slip_count)
                            
                #     # frappe.msgprint(str(future_old_amount))
                #     # frappe.msgprint(str(future_new_amount))

                #     future_old_amount_sum=sum(future_old_amount)
                #     future_new_amount_sum=sum(future_new_amount)

                #     old_regime_values.append(round(future_old_amount_sum))
                #     new_regime_values.append(round(future_new_amount_sum))


                # else:

                    
                    
                #     new_salary_slip = make_salary_slip(
                #     source_name=latest_salary_structure[0].salary_structure,
                #     employee=self.employee,
                #     print_format='Salary Slip Standard for CTC',
                #     # posting_date=latest_salary_structure[0].from_date
                #     )

                #     for new_earning in new_salary_slip.earnings:
                #         taxable_component = frappe.get_doc("Salary Component", new_earning.salary_component)

                #         if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #             taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "All":
                #             old_amount_sum+=new_earning.amount*(num_months)
                #             new_amount_sum+=new_earning.amount*(num_months)

                       
                #         if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #             taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "Old Regime":
                #             old_amount_sum+=new_earning.amount*(num_months)                                

                        
                #         if taxable_component.is_tax_applicable == 1 and taxable_component.custom_perquisite == 0 and \
                #             taxable_component.custom_tax_exemption_applicable_based_on_regime == 1 and taxable_component.custom_regime == "New Regime":
                #             new_amount_sum+=new_earning.amount*(num_months)
                        
                #         if taxable_component.is_tax_applicable == 1 and taxable_component.component_type == "NPS":
                #                 nps_amount+=new_earning.amount*(num_months)


                #         if taxable_component.custom_is_accrual == 1:
                #                 bonus_amount+=new_earning.amount*(num_months)

                    

                #     for deduction in new_salary_slip.deductions:
                                 
                #         taxable_component = frappe.get_doc("Salary Component", deduction.salary_component)
                #         if taxable_component.component_type == "EPF":

                #             epf_amount+=deduction.amount*(num_months)
                                
                #         if taxable_component.component_type == "Professional Tax":
                #             pt_amount+=deduction.amount*(num_months)
                    

                

                # old_regime_values.append(round(old_amount_sum))
                # new_regime_values.append(round(new_amount_sum))

                # old_regime_values.append(0)
                # new_regime_values.append(0)

                # old_regime_values.append(round(old_amount_sum))
                # new_regime_values.append(round(new_amount_sum))




                # frappe.msgprint(str(old_regime_values))
                # frappe.msgprint(str(new_amount_sum))

                # if self.custom_tax_regime=="Old Regime":

                #     old_regime_values.append(round(self.total_exemption_amount))  
                #     new_regime_values.append(round(nps_amount))


                # if self.custom_tax_regime=="New Regime":


                #     if epf_amount>=150000:
                #         old_regime_values.append(round(150000+nps_amount+pt_amount))
                #         new_regime_values.append(round(nps_amount))

                #     else:
                #         old_regime_values.append(round(epf_amount+nps_amount+pt_amount))
                #         new_regime_values.append(round(nps_amount))


                # if self.custom_income_tax:

                #     get_income_tax = frappe.get_list('Income Tax Slab',
                #         filters={'company': self.company,'docstatus':1,"disabled":0},
                #         fields=["*"],
                        
                #     )
                #     if len(get_income_tax)>0:
                #         for tax_slab in get_income_tax:
                #             if tax_slab.custom_select_regime=="Old Regime":

                #                 old_regime_values.append(tax_slab.standard_tax_exemption_amount)
                #                 annual_taxable_income=(old_amount_sum-self.total_exemption_amount-tax_slab.standard_tax_exemption_amount)
                #                 old_regime_values.append(round(annual_taxable_income))

                #                 income_doc = frappe.get_doc('Income Tax Slab', tax_slab.name)
                #                 total_value=[]
                #                 from_amount=[]
                #                 to_amount=[]
                #                 percentage=[]

                #                 total_array=[]
                #                 difference=[]

                #                 rebate=income_doc.custom_taxable_income_is_less_than
                #                 max_amount=income_doc.custom_maximum_amount

                #                 for i in income_doc.slabs:
                                        

                #                     array_list={
                #                         'from':i.from_amount,
                #                         'to':i.to_amount,
                #                         'percent':i.percent_deduction
                #                         }
                                    
                #                     total_array.append(array_list)
                #                 for slab in total_array:
                                        
                #                     if slab['to'] == 0.0:
                #                         if round(annual_taxable_income) >= slab['from']:
                #                             tt1=round(annual_taxable_income)-slab['from']
                #                             tt2=slab['percent']
                #                             tt3=round((tt1*tt2)/100)
                                            
                #                             tt4=slab['from']
                #                             tt5=slab['to']
                                            
                #                             remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                #                             for slab in remaining_slabs:
                #                                 from_amount.append(slab['from'])
                #                                 to_amount.append(slab['to'])
                #                                 percentage.append(slab["percent"])
                #                                 difference.append(slab['to']-slab['from'])
                #                                 total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                #                             from_amount.append(tt4)
                #                             to_amount.append(tt5)
                #                             percentage.append(tt2)
                #                             difference.append(tt1)
                #                             total_value.append(tt3)

                                          
                    
                #                     else:
                #                         if slab['from'] <= round(annual_taxable_income) <= slab['to']:
                #                             tt1=round(annual_taxable_income)-slab['from']
                #                             tt2=slab['percent']
                #                             tt3=(tt1*tt2)/100
                #                             tt4=slab['from']
                #                             tt5=slab['to']
                #                             remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                                            
                #                             for slab in remaining_slabs:
                #                                 from_amount.append(slab['from'])
                #                                 to_amount.append(slab['to'])
                #                                 percentage.append(slab["percent"])
                #                                 difference.append(slab['to']-slab['from'])
                #                                 total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                #                             from_amount.append(tt4)
                #                             to_amount.append(tt5)
                #                             percentage.append(tt2)
                #                             difference.append(tt1)
                #                             total_value.append(tt3)

                #                 total_sum = sum(total_value)

                #                 total_tax_payable=[]


                #                 old_regime_values.append(round(total_sum))

                                
                #                 if annual_taxable_income<rebate:                                        
                #                     old_regime_values.append(total_sum)
                #                     old_regime_values.append(0)

                #                     total_tax_payable.append(0)


                #                 else:

                #                     old_regime_values.append(0)
                #                     old_regime_values.append(total_sum) 

                                   
                #                     total_tax_payable.append(total_sum)
                                        
                #                 if annual_taxable_income>5000000:

                #                     surcharge_m=(total_sum*10)/100
                #                     old_regime_values.append(surcharge_m)
                                    
                #                     old_regime_values.append((surcharge_m+total_sum)*4/100)

                #                     total_tax_payable.append(((surcharge_m+total_sum)*4/100))

                #                 else:
                #                     old_regime_values.append(0)
                #                     old_regime_values.append(round((0+total_sum)*4/100))
                #                     total_tax_payable.append(((0+total_sum)*4/100))


                #                 tax_sum=sum(total_tax_payable)

                #                 old_regime_values.append(round(tax_sum))

                #                 salary_slip_sum=[]
                #                 get_all_salary_slip = frappe.get_list('Salary Slip',
                #                         filters={'employee': self.employee,'docstatus': ['in', [1]],"custom_payroll_period":self.payroll_period},
                #                         fields=["*"],
                                        
                #                     )

                #                 if len(get_all_salary_slip)>0:
                #                     for salary_slip in get_all_salary_slip:
                #                         salary_slip_sum.append(salary_slip.current_month_income_tax)

                #                 previous_tax_sum=sum(salary_slip_sum)
                #                 old_regime_values.append(round(round(previous_tax_sum)))

                                

                #                 old_regime_values.append(round(tax_sum/num_months))

                #                 slip_sum=(tax_sum/num_months)+previous_tax_sum
                #                 old_regime_values.append(round(slip_sum))
                                



                #                 old_regime_values.append(round(tax_sum-slip_sum))

                                
                                

                #                 future_month_count=(num_months-salary_slip_count)

                #                 old_regime_values.append(round((tax_sum-slip_sum)/future_month_count))


                                




                #             if tax_slab.custom_select_regime=="New Regime":

                #                 new_regime_values.append(tax_slab.standard_tax_exemption_amount)
                #                 annual_taxable_income=round((new_amount_sum-nps_amount-tax_slab.standard_tax_exemption_amount))
                #                 new_regime_values.append(annual_taxable_income)

                #                 income_doc = frappe.get_doc('Income Tax Slab', tax_slab.name)
                #                 total_value=[]
                #                 from_amount=[]
                #                 to_amount=[]
                #                 percentage=[]

                #                 total_array=[]
                #                 difference=[]

                #                 rebate=income_doc.custom_taxable_income_is_less_than
                #                 max_amount=income_doc.custom_maximum_amount

                #                 for i in income_doc.slabs:
                                        

                #                     array_list={
                #                         'from':i.from_amount,
                #                         'to':i.to_amount,
                #                         'percent':i.percent_deduction
                #                         }
                                    
                #                     total_array.append(array_list)
                #                 for slab in total_array:
                                        
                #                     if slab['to'] == 0.0:
                #                         if round(annual_taxable_income) >= slab['from']:
                #                             tt1=round(annual_taxable_income)-slab['from']
                #                             tt2=slab['percent']
                #                             tt3=round((tt1*tt2)/100)
                                            
                #                             tt4=slab['from']
                #                             tt5=slab['to']
                                            
                #                             remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                #                             for slab in remaining_slabs:
                #                                 from_amount.append(slab['from'])
                #                                 to_amount.append(slab['to'])
                #                                 percentage.append(slab["percent"])
                #                                 difference.append(slab['to']-slab['from'])
                #                                 total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                #                             from_amount.append(tt4)
                #                             to_amount.append(tt5)
                #                             percentage.append(tt2)
                #                             difference.append(tt1)
                #                             total_value.append(tt3)

                #                     else:
                #                         if slab['from'] <= round(annual_taxable_income) <= slab['to']:
                #                             tt1=round(annual_taxable_income)-slab['from']
                #                             tt2=slab['percent']
                #                             tt3=(tt1*tt2)/100
                #                             tt4=slab['from']
                #                             tt5=slab['to']
                #                             remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                                            
                #                             for slab in remaining_slabs:
                #                                 from_amount.append(slab['from'])
                #                                 to_amount.append(slab['to'])
                #                                 percentage.append(slab["percent"])
                #                                 difference.append(slab['to']-slab['from'])
                #                                 total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                #                             from_amount.append(tt4)
                #                             to_amount.append(tt5)
                #                             percentage.append(tt2)
                #                             difference.append(tt1)
                #                             total_value.append(tt3)


                #                 total_sum = sum(total_value)
                #                 total_tax_payable=[]
                #                 new_regime_values.append(total_sum)

                #                 if annual_taxable_income<rebate:
                                        
                #                     new_regime_values.append(round(total_sum))
                #                     new_regime_values.append(0)
                #                     total_tax_payable.append(0)
                #                 else:

                #                     new_regime_values.append(0)
                #                     new_regime_values.append(round(total_sum))
                #                     total_tax_payable.append(total_sum)
                                        
                #                 if annual_taxable_income>5000000:

                #                     surcharge_m=round((total_sum*10)/100)
                #                     new_regime_values.append(surcharge_m)
                                    
                #                     new_regime_values.append(round((surcharge_m+total_sum)*4/100))

                #                     total_tax_payable.append(((surcharge_m+total_sum)*4/100))

                #                 else:
                #                     new_regime_values.append(0)
                #                     new_regime_values.append(round(((0+total_sum)*4/100)))
                #                     total_tax_payable.append(((0+total_sum)*4/100))


                #                 tax_sum=sum(total_tax_payable)

                #                 new_regime_values.append(round(tax_sum))

                #                 salary_slip_sum=[]
                #                 get_all_salary_slip = frappe.get_list('Salary Slip',
                #                         filters={'employee': self.employee,'docstatus':1,"custom_payroll_period":self.payroll_period},
                #                         fields=["*"],
                                        
                #                     )

                #                 if len(get_all_salary_slip)>0:
                #                     for salary_slip in get_all_salary_slip:
                #                         salary_slip_sum.append(salary_slip.current_month_income_tax)

                                
                #                 previous_tax_sum=sum(salary_slip_sum)
                #                 new_regime_values.append(round(previous_tax_sum))

                                

                #                 new_regime_values.append(round(tax_sum/num_months))


                #                 slip_sum=(tax_sum/num_months)+previous_tax_sum
                #                 new_regime_values.append(round(slip_sum))



                #                 new_regime_values.append(round(tax_sum-slip_sum))

                #                 future_month_count=(num_months-salary_slip_count)

                #                 new_regime_values.append(round((tax_sum-slip_sum)/future_month_count))
                #                 # frappe.msgprint(str(future_month_count))
                                

                
                self.custom_tds_projection=[]

                frappe.msgprint(str(title_array))
                # frappe.msgprint(str(old_regime_values))

                # frappe.msgprint(str(len(title_array)))
                # frappe.msgprint(str(len(old_regime_values)))
                # frappe.msgprint(str(len(new_regime_values)))

                for i in range(len(title_array)):
                    self.append("custom_tds_projection", {
                        "title": title_array[i],
                        # "old_regime_value":old_regime_values[i],
                        # "new_regime_value":new_regime_values[i],
                       
                    })















                   
                

        

    def set_total_exemption_amount(self):
        self.total_exemption_amount = flt(get_total_exemption_amount(self.declarations), self.precision("total_exemption_amount"))
        
        # if self.custom_check == 1:
        if self.annual_hra_exemption:
            self.total_exemption_amount = self.total_exemption_amount + self.annual_hra_exemption

        

    def on_cancel(self):
        self.cancel_declaration_history()
        


    def cancel_declaration_history(self):
        history_data=frappe.db.get_list('Tax Declaration History',
            filters={
                'tax_exemption':self.name,
            },
            fields=['*'],
            
        )

        if len(history_data)>0:
            data_doc=frappe.get_doc('Tax Declaration History',history_data[0].name)
            frappe.delete_doc('Tax Declaration History', data_doc.name)






    def update_hra_breakup(self):
        if self.monthly_house_rent:
            if self.workflow_state in ["Approved"]:
                array = []
                for t1 in self.custom_hra_breakup:
                    array.append({
                        "month": t1.month,
                        "rent_paid": t1.rent_paid,
                        "basic": t1.earned_basic,
                        "hra": t1.hra_received,
                        "basic_excess": t1.exemption_amount,
                        "exception_amount": t1.exemption_amount
                    })

                # Fetch the latest Tax Declaration History for the employee
                get_latest_history = frappe.get_list(
                    'Tax Declaration History',
                    filters={'employee': self.employee},
                    fields=['*'],
                    order_by='posting_date desc',
                    limit=1  

                )

                if len(get_latest_history) > 0:
                    each_doc = frappe.get_doc("Tax Declaration History", get_latest_history[0].name)

                    each_doc.monthly_house_rent=self.monthly_house_rent
                    each_doc.rented_in_metro_city=self.rented_in_metro_city
                    each_doc.hra_as_per_salary_structure=self.salary_structure_hra
                    each_doc.annual_hra_exemption=self.annual_hra_exemption
                    each_doc.monthly_hra_exemption=self.monthly_hra_exemption

                    
                    
                    each_doc.hra_breakup = []

                    for entry in array:
                        each_doc.append("hra_breakup", {
                            "month": entry["month"],
                            "rent_paid": entry["rent_paid"],
                            "earned_basic": entry["basic"],
                            "hra_received": entry["hra"],
                            "excess_of_rent_paid": entry["basic_excess"],
                            "exemption_amount": entry["exception_amount"]
                        })

                    each_doc.save()
                    frappe.db.commit()

    def update_tax_declaration(self):

        if self.workflow_state in ["Approved"]:
            if len(self.declarations) > 0:
                tax_component = []
                for component in self.declarations:
                    tax_component.append({
                        "sub_category": component.exemption_sub_category,
                        "category": component.exemption_category,
                        "max_amount": component.max_amount,
                        "amount": component.amount
                    })

                hra_component = []
                for hra in self.custom_hra_breakup:
                    hra_component.append({
                        "month": hra.month,
                        "rent_paid": hra.rent_paid,
                        "earned_basic": hra.earned_basic,
                        "hra_received": hra.hra_received,
                        "excess_of_rent_paid": hra.excess_of_rent_paid,
                        "exemption_amount": hra.exemption_amount
                    })

                get_latest_history = frappe.get_list(
                    'Tax Declaration History',
                    filters={'employee': self.employee, "posting_date": self.custom_posting_date},
                    fields=['*'],
                    limit=1
                )

                if len(get_latest_history) > 0:
                    each_doc = frappe.get_doc("Tax Declaration History", get_latest_history[0].name)

                    each_doc.rented_in_metro_city = self.rented_in_metro_city
                    each_doc.hra_as_per_salary_structure = self.salary_structure_hra
                    each_doc.annual_hra_exemption = self.annual_hra_exemption
                    each_doc.monthly_hra_exemption = self.monthly_hra_exemption
                    each_doc.total_declared_amount = self.total_declared_amount
                    each_doc.total_exemption_amount = self.total_exemption_amount
                    each_doc.income_tax= self.custom_income_tax

                    # each_doc.tds_from_previous_employer_amount = self.custom_tds_from_previous_employer_amount

                    each_doc.declaration_details = []
                    for entry in tax_component:
                        each_doc.append("declaration_details", {
                            "exemption_sub_category": entry["sub_category"],
                            "exemption_category": entry["category"],
                            "maximum_exempted_amount": entry["max_amount"],
                            "declared_amount": entry["amount"],
                        })

                    each_doc.hra_breakup = []
                    for hra_entry in hra_component:
                        each_doc.append("hra_breakup", {
                            "month": hra_entry["month"],
                            "rent_paid": hra_entry["rent_paid"],
                            "earned_basic": hra_entry["earned_basic"],
                            "hra_received": hra_entry["hra_received"],
                            "excess_of_rent_paid": hra_entry["excess_of_rent_paid"],
                            "exemption_amount": hra_entry["exemption_amount"],
                        })

                    each_doc.save()
                    frappe.db.commit()

                else:
                    insert_history = frappe.get_doc({
                        'doctype': 'Tax Declaration History',
                        'employee': self.employee,
                        'employee_name': self.employee_name,
                        'income_tax': self.custom_income_tax,
                        'company': self.company,
                        'posting_date': self.custom_posting_date,
                        'payroll_period': self.payroll_period,
                        'tax_exemption': self.name,
                        'total_declared_amount': self.total_declared_amount,
                        'total_exemption_amount': self.total_exemption_amount,
                        'monthly_house_rent': self.monthly_house_rent,
                        'rented_in_metro_city': self.rented_in_metro_city,
                        'hra_as_per_salary_structure': self.salary_structure_hra,
                        'annual_hra_exemption': self.annual_hra_exemption,
                        'monthly_hra_exemption': self.monthly_hra_exemption,
                        'declaration_details': [
                            {
                                "exemption_sub_category": entry["sub_category"],
                                "exemption_category": entry["category"],
                                "maximum_exempted_amount": entry["max_amount"],
                                "declared_amount": entry["amount"],
                            } for entry in tax_component
                        ],
                        'hra_breakup': [
                            {
                                "month": hra_entry["month"],
                                "rent_paid": hra_entry["rent_paid"],
                                "earned_basic": hra_entry["earned_basic"],
                                "hra_received": hra_entry["hra_received"],
                                "excess_of_rent_paid": hra_entry["excess_of_rent_paid"],
                                "exemption_amount": hra_entry["exemption_amount"],
                            } for hra_entry in hra_component
                        ]
                    })

                    insert_history.insert()
                    frappe.db.commit()



    
        
    def insert_declaration_history(self):
        if self.employee:
            declaration_details = []
            hra_breakup=[]

            for i in self.declarations:
                declaration_details.append({
                    'exemption_sub_category': i.exemption_sub_category,
                    'exemption_category': i.exemption_category,
                    'maximum_exempted_amount': i.max_amount,
                    'declared_amount': i.amount
                })

            for j in self.custom_hra_breakup:
                hra_breakup.append({
                    'month': j.month,
                    'rent_paid': j.rent_paid,
                    'earned_basic': j.earned_basic,
                    'hra_received': j.hra_received,
                    'excess_of_rent_paid':j.excess_of_rent_paid,
                    'exemption_amount':j.exemption_amount
                })


            insert_doc = frappe.get_doc({
                'doctype': 'Tax Declaration History',
                'employee': self.employee,
                'employee_name':self.employee_name,
                'income_tax': self.custom_income_tax, 
                'company': self.company,
                'posting_date': frappe.utils.nowdate(),
                'payroll_period': self.payroll_period,
                'monthly_house_rent': self.monthly_house_rent,
                'rented_in_metro_city': self.rented_in_metro_city,
                'hra_as_per_salary_structure': self.salary_structure_hra,  
                'total_declared_amount': self.total_declared_amount,
                'annual_hra_exemption': self.annual_hra_exemption,
                'monthly_hra_exemption': self.monthly_hra_exemption,
                'total_exemption_amount': self.total_exemption_amount,
                'tax_exemption':self.name,
                'declaration_details': declaration_details,
                'hra_breakup': hra_breakup
            })

            insert_doc.insert()
            

    def calculate_hra_breakup(self):
        
        if self.monthly_house_rent:
            

            get_company=frappe.get_doc("Company",self.company)
            basic_component=get_company.basic_component

            ss_assignment = frappe.get_list(
                'Salary Structure Assignment',
                filters={'employee': self.employee, 'docstatus': 1,'company':self.company},
                fields=['*'],
                order_by='from_date desc',
            )

            if ss_assignment:
                start_date=ss_assignment[0].from_date
                if ss_assignment[0].custom_payroll_period:
                    payroll_period=frappe.get_doc("Payroll Period",ss_assignment[0].custom_payroll_period)
                    end_date = payroll_period.end_date
                    current_date = start_date

                    month_count = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1

                    new_salary_slip = make_salary_slip(
                        source_name=ss_assignment[0].salary_structure,
                        employee=self.employee,
                        print_format='Salary Slip Standard for CTC',  
                        posting_date=ss_assignment[0].from_date,
                        for_preview=1,
                    )
                    
                    for new_earning in new_salary_slip.earnings:
                        
                        if new_earning.salary_component==basic_component:
                            if self.custom_check==0:
                                self.custom_basic=new_earning.amount*month_count
                                self.custom_basic_as_per_salary_structure=(new_earning.amount*month_count)*10/100




                    months = []
                    
                    while current_date <= end_date:
                        month_name = current_date.strftime("%B")
                        if month_name not in months:
                            months.append(month_name)
                        current_date = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)

                    
                    

                    
                    earned_basic = 0
                    if self.rented_in_metro_city==1:
                        earned_basic=(self.custom_basic_as_per_salary_structure*10)*50/100
                    else:
                        earned_basic=(self.custom_basic_as_per_salary_structure*10)*40/100
            

                    

                    self.custom_hra_breakup = []  
                    for i in range(len(months)):
                        excess_of_rent_paid = round(self.monthly_house_rent * 12 - self.custom_basic_as_per_salary_structure)
                        

                        exemption_amount = min(self.salary_structure_hra, earned_basic, excess_of_rent_paid)
                        
                        self.append("custom_hra_breakup", {
                            "month": months[i],
                            "rent_paid": self.monthly_house_rent * 12,
                            "hra_received": self.salary_structure_hra,
                            "earned_basic": round(earned_basic),
                            "excess_of_rent_paid": excess_of_rent_paid,
                            "exemption_amount": exemption_amount
                        })

                
      

        else:
            self.custom_basic_as_per_salary_structure=None
            self.custom_basic=None
            self.custom_hra_breakup=[]



    def process_form_data(self):
        if self.custom_tax_regime == "Old Regime":
            if self.workflow_state in ["Approved", "Pending"]:
                form_data = json.loads(self.custom_declaration_form_data or '{}')
                
                # Extract numbers from the form data
                numbers = [
                    {"field": "amount", "name": "Mediclaim Policy for Parents"},
                    {"field": "amount3", "name": "Mediclaim Policy for Self, Spouse, Children for Senior Citizen"},
                    {"field": "mpAmount3", "name": "Mediclaim Policy for Self, Spouse, Children"},
                    {"field": "mpAmount4", "name": "Mediclaim Policy for Parents for Senior Citizen"},
                    {"field": "mp5", "name": "Preventive Health Check-up for Parents"},
                    {"field": "mpAmount6", "name": "Preventive Health Check-up"},
                    {"field": "hlAmount", "name": "Interest Paid On Home Loan"},



                    {"field": "pfValue", "name": "Employee Provident Fund (Auto)"},
                    {"field": "aValue2", "name": "Pension Scheme Investments & ULIP"},
                    {"field": "bValue1", "name": "Principal paid on Home Loan"},
                    {"field": "amount4", "name": "Public Provident Fund"},


                    {"field": "dValue1", "name": "Home Loan Account Of National Housing Bank"},

                    {"field": "eValue1", "name": "Life Insurance Premium"},

                    {"field": "fValue1", "name": "National Savings Certificates"},


                    {"field": "gValue1", "name": "Mutual Funds - Notified Under Clause 23D Of Section 10 "},
                    {"field": "hValue1", "name": "ELSS - Equity Link Saving Scheme Of Mutual Funds "},

                    {"field": "iValue1", "name": "Children Tuition Fees"},


                    {"field": "jValue1", "name": "Fixed Deposits In Banksn"},
                    {"field": "kValue1", "name": "5 Years Term Deposit An Account Under Post Office Term Deposit Rules "},
                    {"field": "kValue2", "name": "Others"},




                    {"field": "fourValue", "name": "Treatment of Dependent with Disability"},
                    {"field": "fiveNumber", "name": "Medical treatment (specified diseases only)"},
                    {"field": "sixNumber", "name": "Interest paid on Education Loan"},
                    {"field": "sevenNumber", "name": "Permanent Physical Disability (Self)"},
                    {"field": "eightNumber", "name": "Donation U/S 80G"},
                    {"field": "nineNumber", "name": "NPS Contribution by Employer"},
                    {"field": "tenNumber", "name": "First HSG Loan Interest Ded.(80EE)"},
                    {"field": "elevenNumber", "name": "Additional Exemption on Voluntary NPS"},


                    {"field": "twelveNumber1", "name": "Tax Incentive for Affordable Housing for Ded U/S 80EEA"},
                    {"field": "fifteenNumber", "name": "Tax Incentives for Electric Vehicles for Ded U/S 80EEB"},
                    {"field": "sixteenNumber", "name": "Donations/contribution made to a political party or an electoral trust"},
                    {"field": "seventeenNumber", "name": "Interest on deposits in saving account for Ded U/S 80TTA"},
                    {"field": "eighteenNumber", "name": "Interest on deposits in saving account for Ded U/S 80TTB"},
                    {"field": "nineteenNumber", "name": "Profession Tax"},

                    {"field": "twentyNumber", "name": "Deduction U/S 80GG"},
                    {"field": "twentyoneNumber", "name": "Rajiv Gandhi Equity Saving Scheme 80CCG"},

                    {"field": "twentyFour", "name": "Uniform Allowance"},

                    {"field": "thirteen", "name": "Education Allowance"},
                    {"field": "twentysix", "name": "Hostel Allowance"},
                    {"field": "twentyseven", "name": "Gratuity"},



                ]
                
                # Prepare lists for child table population
                sub_category, category, max_amount, declared_amount = [], [], [], []
                
                for item in numbers:
                    value = form_data.get(item["field"], 0)
                    if value > 0:
                        # Fetch data for the sub-category
                        get_doc1 = frappe.get_list(
                            'Employee Tax Exemption Sub Category',
                            filters={"is_active": 1, "name": item["name"]},
                            fields=['name', 'exemption_category', 'max_amount']
                        )
                        
                        if get_doc1:
                            sub_category.append(get_doc1[0].name)
                            category.append(get_doc1[0].exemption_category)
                            max_amount.append(get_doc1[0].max_amount)
                            declared_amount.append(value)
                
                # Reset and populate the `declarations` child table
                self.declarations = []
                for i in range(len(sub_category)):
                    self.append('declarations', {
                        "exemption_sub_category": sub_category[i],
                        "exemption_category": category[i],
                        "max_amount": max_amount[i],
                        "amount": declared_amount[i]
                    })

        if self.custom_tax_regime=="New Regime":
            if self.workflow_state in ["Approved", "Pending"]:
                form_data = json.loads(self.custom_declaration_form_data or '{}')
                
                # Extract numbers from the form data
                numbers = [
                    
                    {"field": "nineNumber", "name": "NPS Contribution by Employer"},
                    
                ]
                
                # Prepare lists for child table population
                sub_category, category, max_amount, declared_amount = [], [], [], []
                
                for item in numbers:
                    value = form_data.get(item["field"], 0)
                    if value > 0:
                        # Fetch data for the sub-category
                        get_doc1 = frappe.get_list(
                            'Employee Tax Exemption Sub Category',
                            filters={"is_active": 1, "name": item["name"]},
                            fields=['name', 'exemption_category', 'max_amount']
                        )
                        
                        if get_doc1:
                            sub_category.append(get_doc1[0].name)
                            category.append(get_doc1[0].exemption_category)
                            max_amount.append(get_doc1[0].max_amount)
                            declared_amount.append(value)
                
                # Reset and populate the `declarations` child table
                self.declarations = []
                for i in range(len(sub_category)):
                    self.append('declarations', {
                        "exemption_sub_category": sub_category[i],
                        "exemption_category": category[i],
                        "max_amount": max_amount[i],
                        "amount": declared_amount[i]
                    })

                    

    



            

            
            

            