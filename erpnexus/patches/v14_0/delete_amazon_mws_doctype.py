import saashq


def execute():
	saashq.delete_doc("DocType", "Amazon MWS Settings", ignore_missing=True)
