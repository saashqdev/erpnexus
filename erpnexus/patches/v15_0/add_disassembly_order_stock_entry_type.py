import saashq


def execute():
	if not saashq.db.exists("Stock Entry Type", "Disassemble"):
		saashq.get_doc(
			{
				"doctype": "Stock Entry Type",
				"name": "Disassemble",
				"purpose": "Disassemble",
				"is_standard": 1,
			}
		).insert(ignore_permissions=True)
