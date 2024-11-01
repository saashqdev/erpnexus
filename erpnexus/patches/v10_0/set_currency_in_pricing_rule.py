import saashq


def execute():
	saashq.reload_doctype("Pricing Rule")

	currency = saashq.db.get_default("currency")
	for doc in saashq.get_all("Pricing Rule", fields=["company", "name"]):
		if doc.company:
			currency = saashq.get_cached_value("Company", doc.company, "default_currency")

		saashq.db.sql("""update `tabPricing Rule` set currency = %s where name = %s""", (currency, doc.name))
