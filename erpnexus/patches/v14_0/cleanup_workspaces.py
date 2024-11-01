import saashq


def execute():
	for ws in ["Retail", "Utilities"]:
		saashq.delete_doc_if_exists("Workspace", ws)

	for ws in ["Integrations", "Settings"]:
		saashq.db.set_value("Workspace", ws, "public", 0)
