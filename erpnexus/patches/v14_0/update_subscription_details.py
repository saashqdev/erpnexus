import saashq


def execute():
	subscription_invoices = saashq.get_all(
		"Subscription Invoice", fields=["document_type", "invoice", "parent"]
	)

	for subscription_invoice in subscription_invoices:
		saashq.db.set_value(
			subscription_invoice.document_type,
			subscription_invoice.invoice,
			"subscription",
			subscription_invoice.parent,
		)

	saashq.delete_doc_if_exists("DocType", "Subscription Invoice")
