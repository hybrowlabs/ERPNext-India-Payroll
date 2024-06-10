app_name = "cn_indian_payroll"
app_title = "Indian Payroll"
app_publisher = "Hybrowlabs technologies"
app_description = "cn-indian-payroll"
app_email = "chinmay@hybrowlabs.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cn_indian_payroll/css/cn_indian_payroll.css"
# app_include_js = "/assets/cn_indian_payroll/js/cn_indian_payroll.js"

# include js, css files in header of web template
# web_include_css = "/assets/cn_indian_payroll/css/cn_indian_payroll.css"
# web_include_js = "/assets/cn_indian_payroll/js/cn_indian_payroll.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "cn_indian_payroll/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "cn_indian_payroll/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "cn_indian_payroll.utils.jinja_methods",
# 	"filters": "cn_indian_payroll.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "cn_indian_payroll.install.before_install"
# after_install = "cn_indian_payroll.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "cn_indian_payroll.uninstall.before_uninstall"
# after_uninstall = "cn_indian_payroll.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "cn_indian_payroll.utils.before_app_install"
# after_app_install = "cn_indian_payroll.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "cn_indian_payroll.utils.before_app_uninstall"
# after_app_uninstall = "cn_indian_payroll.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cn_indian_payroll.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cn_indian_payroll.tasks.all"
# 	],
# 	"daily": [
# 		"cn_indian_payroll.tasks.daily"
# 	],
# 	"hourly": [
# 		"cn_indian_payroll.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cn_indian_payroll.tasks.weekly"
# 	],
# 	"monthly": [
# 		"cn_indian_payroll.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "cn_indian_payroll.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cn_indian_payroll.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "cn_indian_payroll.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["cn_indian_payroll.utils.before_request"]
# after_request = ["cn_indian_payroll.utils.after_request"]

# Job Events
# ----------
# before_job = ["cn_indian_payroll.utils.before_job"]
# after_job = ["cn_indian_payroll.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"cn_indian_payroll.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt": "Custom Field", "filters": {"module": "cn_indian_payroll"}},
	{"dt":"Print Format","filters":{"module": "cn_indian_payroll"}}
    
]



doctype_js = {
                "Payroll Entry" : "public/js/payroll.js",
                "Employee Benefit Claim" : "public/js/employee_benefit_claim.js",
                "Employee" : "public/js/employee.js",
                "Salary Structure Assignment": "public/js/salary_structure_assignment.js",
                "Employee Tax Exemption Declaration":"public/js/tax_declaration.js"

              }
override_doctype_class = {

    
    "Employee Benefit Claim":"cn_indian_payroll.cn_indian_payroll.overrides.benefit_claim.CustomEmployeeBenefitClaim",

    "Salary Slip":"cn_indian_payroll.cn_indian_payroll.overrides.salary_slip.CustomSalarySlip",
    "Salary Structure Assignment":"cn_indian_payroll.cn_indian_payroll.overrides.salary_structure_assignment.CustomSalaryStructureAssignment",
    "Employee Tax Exemption Declaration":"cn_indian_payroll.cn_indian_payroll.overrides.tax_declaration.CustomEmployeeTaxExemptionDeclaration"

    # "Salary Slip": "cn_indian_payroll.cn_indian_payroll.overrides.salary_slip.CustomSalarySlip"
}
