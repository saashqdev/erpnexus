import saashq


def execute():
	from erpnexus.setup.setup_wizard.operations.install_fixtures import add_uom_data

	saashq.reload_doc("setup", "doctype", "UOM Conversion Factor")
	saashq.reload_doc("setup", "doctype", "UOM")
	saashq.reload_doc("stock", "doctype", "UOM Category")

	add_uom_data()
