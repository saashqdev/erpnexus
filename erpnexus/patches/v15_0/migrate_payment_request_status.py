import saashq


def execute():
	"""
	Description:
	Change Inward Payment Requests from statut 'Initiated' to correct status 'Requested'.
	Status 'Initiated' is reserved for Outward Payment Requests and was a semantic error in previour versions.
	"""
	so = saashq.qb.DocType("Payment Request")
	saashq.qb.update(so).set(so.status, "Requested").where(so.payment_request_type == "Inward").where(
		so.status == "Initiated"
	).run()
