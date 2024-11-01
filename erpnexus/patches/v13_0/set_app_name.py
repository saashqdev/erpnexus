import saashq


def execute():
	saashq.reload_doctype("System Settings")
	settings = saashq.get_doc("System Settings")
	settings.db_set("app_name", "ERPNexus", commit=True)
