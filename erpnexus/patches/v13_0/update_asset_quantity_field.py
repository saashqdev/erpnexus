import saashq


def execute():
	if saashq.db.count("Asset"):
		saashq.reload_doc("assets", "doctype", "Asset")
		asset = saashq.qb.DocType("Asset")
		saashq.qb.update(asset).set(asset.asset_quantity, 1).run()
