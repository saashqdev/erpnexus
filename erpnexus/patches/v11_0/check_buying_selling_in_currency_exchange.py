import saashq


def execute():
	saashq.reload_doc("setup", "doctype", "currency_exchange")
	saashq.db.sql("""update `tabCurrency Exchange` set for_buying = 1, for_selling = 1""")
