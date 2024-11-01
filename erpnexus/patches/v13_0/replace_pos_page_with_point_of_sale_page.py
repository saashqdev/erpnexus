import saashq


def execute():
	if saashq.db.exists("Page", "point-of-sale"):
		saashq.rename_doc("Page", "pos", "point-of-sale", 1, 1)
