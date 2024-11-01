import saashq

from erpnexus.setup.install import create_default_success_action


def execute():
	saashq.reload_doc("core", "doctype", "success_action")
	create_default_success_action()
