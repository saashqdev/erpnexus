import saashq


def execute():
	saashq.rename_doc("DocType", "Account Type", "Bank Account Type", force=True)
	saashq.rename_doc("DocType", "Account Subtype", "Bank Account Subtype", force=True)
	saashq.reload_doc("accounts", "doctype", "bank_account")
