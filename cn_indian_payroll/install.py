"""Entry point called by ``bench install-app cn_indian_payroll``."""

from cn_indian_payroll.cn_indian_payroll.setup import after_install as _after_install


def after_install() -> None:
    _after_install()
