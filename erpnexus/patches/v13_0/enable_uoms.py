import saashq


def execute():
	saashq.reload_doc("setup", "doctype", "uom")

	uom = saashq.qb.DocType("UOM")

	(
		saashq.qb.update(uom)
		.set(uom.enabled, 1)
		.where(uom.creation >= "2021-10-18")  # date when this field was released
	).run()
