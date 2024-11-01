import saashq


def execute():
	from erpnexus.setup.setup_wizard.operations.install_fixtures import read_lines

	saashq.reload_doc("selling", "doctype", "sales_partner_type")

	saashq.local.lang = saashq.db.get_default("lang") or "en"

	default_sales_partner_type = read_lines("sales_partner_type.txt")

	for s in default_sales_partner_type:
		insert_sales_partner_type(s)

	# get partner type in existing forms (customized)
	# and create a document if not created
	for d in ["Sales Partner"]:
		partner_type = saashq.db.sql_list(f"select distinct partner_type from `tab{d}`")
		for s in partner_type:
			if s and s not in default_sales_partner_type:
				insert_sales_partner_type(s)

		# remove customization for partner type
		for p in saashq.get_all(
			"Property Setter", {"doc_type": d, "field_name": "partner_type", "property": "options"}
		):
			saashq.delete_doc("Property Setter", p.name)


def insert_sales_partner_type(s):
	if not saashq.db.exists("Sales Partner Type", s):
		saashq.get_doc(dict(doctype="Sales Partner Type", sales_partner_type=s)).insert()
