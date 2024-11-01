import saashq


def execute():
	assets = saashq.get_all("Asset", filters={"allow_monthly_depreciation": 1})

	for d in assets:
		print(d.name)
		asset_doc = saashq.get_doc("Asset", d.name)
		for i in asset_doc.get("finance_books"):
			if i.frequency_of_depreciation != 1:
				i.total_number_of_depreciations *= i.frequency_of_depreciation
				i.frequency_of_depreciation = 1
				i.db_update()
