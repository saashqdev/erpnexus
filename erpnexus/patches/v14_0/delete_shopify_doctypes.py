import saashq


def execute():
	saashq.delete_doc("DocType", "Shopify Settings", ignore_missing=True)
	saashq.delete_doc("DocType", "Shopify Log", ignore_missing=True)
