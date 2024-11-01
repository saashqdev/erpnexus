import saashq


def execute():
	for dt in ("GoCardless Settings", "GoCardless Mandate", "Mpesa Settings"):
		saashq.delete_doc("DocType", dt, ignore_missing=True)
