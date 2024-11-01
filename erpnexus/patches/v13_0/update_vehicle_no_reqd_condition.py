import saashq


def execute():
	saashq.reload_doc("custom", "doctype", "custom_field", force=True)
	company = saashq.get_all("Company", filters={"country": "India"})
	if not company:
		return

	if saashq.db.exists("Custom Field", {"fieldname": "vehicle_no"}):
		saashq.db.set_value("Custom Field", {"fieldname": "vehicle_no"}, "mandatory_depends_on", "")
