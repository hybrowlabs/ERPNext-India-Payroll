frappe.ui.form.on('Company', {
    refresh(frm) {

        let component = [];
        Promise.all([
            frappe.db.get_list('Salary Component', {
                filters: {
                    'disabled': 0,
                    'custom_is_accrual': 1,
                },
                fields: ['name']
            }),
            frappe.db.get_list('Salary Component', {
                filters: {
                    'disabled': 0,
                    'custom_is_reimbursement': 1,
                },
                fields: ['name']
            })
        ]).then(([accrualList, reimbursementList]) => {
            const allComponents = [...accrualList, ...reimbursementList];
            component = allComponents.map(d => d.name);

            frm.fields_dict['custom_accrued_component_payable_account'].grid.get_field('salary_component').get_query = function(doc, cdt, cdn) {
                return {
                    filters: [
                        ["Salary Component", "name", "in", component]
                    ]
                };
            };
        });

        frm.fields_dict['custom_accrued_component_payable_account'].grid.get_field('payable_account').get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['Account', 'root_type', '=', 'Liability'],
                    ['Account', 'is_group', '=', 0],
                    ['Account', 'company', '=', frm.doc.name]
                ]
            };
        };

    }
});
