import saashq


def execute():
	saashq.reload_doc("accounts", "doctype", "pos_closing_entry")

	saashq.db.sql("update `tabPOS Closing Entry` set `status` = 'Failed' where `status` = 'Queued'")
