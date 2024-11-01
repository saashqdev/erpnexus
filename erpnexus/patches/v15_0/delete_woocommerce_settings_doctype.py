import saashq


def execute():
	saashq.delete_doc("DocType", "Woocommerce Settings", ignore_missing=True)
