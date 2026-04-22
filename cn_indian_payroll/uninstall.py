"""Entry point called by ``bench remove-app cn_indian_payroll``."""

from cn_indian_payroll.cn_indian_payroll.setup import before_uninstall as _before_uninstall


def before_uninstall() -> None:
    _before_uninstall()
