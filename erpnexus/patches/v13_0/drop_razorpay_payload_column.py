import saashq


def execute():
	if saashq.db.exists("DocType", "Membership"):
		if "webhook_payload" in saashq.db.get_table_columns("Membership"):
			saashq.db.sql("alter table `tabMembership` drop column webhook_payload")
