import saashq


def execute():
	for doctype in ["Customer", "Supplier"]:
		field = doctype.lower() + "_type"
		saashq.db.set_value(doctype, {field: "Proprietorship"}, field, "Individual")
