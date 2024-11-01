import saashq


def execute():
	bom = saashq.qb.DocType("BOM")

	(
		saashq.qb.update(bom).set(bom.transfer_material_against, "Work Order").where(bom.with_operations == 0)
	).run()
