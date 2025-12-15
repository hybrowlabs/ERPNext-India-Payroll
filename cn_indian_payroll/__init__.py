import cn_indian_payroll.monkey_patches

import hrms.hr.utils
from cn_indian_payroll.cn_indian_payroll.overrides.hrms_utils import (
    get_total_exemption_amount,
)


hrms.hr.utils.get_total_exemption_amount = get_total_exemption_amount

# from cn_indian_payroll.cn_indian_payroll.overrides.override_salary_slip import (
#     override_calculate_tax_by_tax_slab,
# )
# from hrms.payroll.doctype.salary_slip import salary_slip

# salary_slip.calculate_tax_by_tax_slab = override_calculate_tax_by_tax_slab

__version__ = "0.0.1"
