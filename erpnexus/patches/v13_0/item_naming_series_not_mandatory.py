import saashq

from erpnexus.utilities.naming import set_by_naming_series


def execute():
	stock_settings = saashq.get_doc("Stock Settings")

	set_by_naming_series(
		"Item",
		"item_code",
		stock_settings.get("item_naming_by") == "Naming Series",
		hide_name_field=True,
		make_mandatory=0,
	)
