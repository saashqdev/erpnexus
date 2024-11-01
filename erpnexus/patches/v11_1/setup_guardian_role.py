import saashq


def execute():
	if "Education" in saashq.get_active_domains() and not saashq.db.exists("Role", "Guardian"):
		doc = saashq.new_doc("Role")
		doc.update({"role_name": "Guardian", "desk_access": 0})

		doc.insert(ignore_permissions=True)
