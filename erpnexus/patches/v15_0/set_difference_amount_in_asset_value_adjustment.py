import saashq


def execute():
	AssetValueAdjustment = saashq.qb.DocType("Asset Value Adjustment")

	saashq.qb.update(AssetValueAdjustment).set(
		AssetValueAdjustment.difference_amount,
		AssetValueAdjustment.new_asset_value - AssetValueAdjustment.current_asset_value,
	).where(AssetValueAdjustment.docstatus != 2).run()
