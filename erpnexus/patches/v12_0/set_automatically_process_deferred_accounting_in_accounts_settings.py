import saashq


def execute():
	saashq.reload_doc("accounts", "doctype", "accounts_settings")

	saashq.db.set_single_value("Accounts Settings", "automatically_process_deferred_accounting_entry", 1)
