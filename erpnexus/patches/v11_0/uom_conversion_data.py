import saashq


def execute():
	from erpnexus.setup.setup_wizard.operations.install_fixtures import add_uom_data

	saashq.reload_doc("setup", "doctype", "UOM Conversion Factor")
	saashq.reload_doc("setup", "doctype", "UOM")
	saashq.reload_doc("stock", "doctype", "UOM Category")

	if not saashq.db.a_row_exists("UOM Conversion Factor"):
		add_uom_data()
	else:
		# delete conversion data and insert again
		saashq.db.sql("delete from `tabUOM Conversion Factor`")
		try:
			saashq.delete_doc("UOM", "Hundredweight")
			saashq.delete_doc("UOM", "Pound Cubic Yard")
		except saashq.LinkExistsError:
			pass

		add_uom_data()
