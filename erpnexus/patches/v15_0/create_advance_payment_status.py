import saashq


def execute():
	"""
	Description:
	Calculate the new Advance Payment Statuse column in SO & PO
	"""

	if saashq.reload_doc("selling", "doctype", "Sales Order"):
		so = saashq.qb.DocType("Sales Order")
		saashq.qb.update(so).set(so.advance_payment_status, "Not Requested").where(so.docstatus == 1).where(
			so.advance_paid == 0.0
		).run()

		saashq.qb.update(so).set(so.advance_payment_status, "Partially Paid").where(so.docstatus == 1).where(
			so.advance_payment_status.isnull()
		).where(so.advance_paid < (so.rounded_total or so.grand_total)).run()

		saashq.qb.update(so).set(so.advance_payment_status, "Fully Paid").where(so.docstatus == 1).where(
			so.advance_payment_status.isnull()
		).where(so.advance_paid == (so.rounded_total or so.grand_total)).run()

		pr = saashq.qb.DocType("Payment Request")
		saashq.qb.update(so).join(pr).on(so.name == pr.reference_name).set(
			so.advance_payment_status, "Requested"
		).where(so.docstatus == 1).where(pr.docstatus == 1).where(
			so.advance_payment_status == "Not Requested"
		).run()

	if saashq.reload_doc("buying", "doctype", "Purchase Order"):
		po = saashq.qb.DocType("Purchase Order")
		saashq.qb.update(po).set(po.advance_payment_status, "Not Initiated").where(po.docstatus == 1).where(
			po.advance_paid == 0.0
		).run()

		saashq.qb.update(po).set(po.advance_payment_status, "Partially Paid").where(po.docstatus == 1).where(
			po.advance_payment_status.isnull()
		).where(po.advance_paid < (po.rounded_total or po.grand_total)).run()

		saashq.qb.update(po).set(po.advance_payment_status, "Fully Paid").where(po.docstatus == 1).where(
			po.advance_payment_status.isnull()
		).where(po.advance_paid == (po.rounded_total or po.grand_total)).run()

		pr = saashq.qb.DocType("Payment Request")
		saashq.qb.update(po).join(pr).on(po.name == pr.reference_name).set(
			po.advance_payment_status, "Initiated"
		).where(po.docstatus == 1).where(pr.docstatus == 1).where(
			po.advance_payment_status == "Not Initiated"
		).run()
