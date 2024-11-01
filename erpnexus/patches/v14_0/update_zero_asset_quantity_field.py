import saashq


def execute():
	asset = saashq.qb.DocType("Asset")
	saashq.qb.update(asset).set(asset.asset_quantity, 1).where(asset.asset_quantity == 0).run()
