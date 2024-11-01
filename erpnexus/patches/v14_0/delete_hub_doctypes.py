import saashq


def execute():
	doctypes = saashq.get_all("DocType", {"module": "Hub Node", "custom": 0}, pluck="name")
	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	saashq.delete_doc("Module Def", "Hub Node", ignore_missing=True, force=True)
