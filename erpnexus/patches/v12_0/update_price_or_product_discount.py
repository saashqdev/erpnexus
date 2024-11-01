import saashq


def execute():
	saashq.reload_doc("accounts", "doctype", "pricing_rule")

	saashq.db.sql(
		""" UPDATE `tabPricing Rule` SET price_or_product_discount = 'Price'
		WHERE ifnull(price_or_product_discount,'') = '' """
	)
