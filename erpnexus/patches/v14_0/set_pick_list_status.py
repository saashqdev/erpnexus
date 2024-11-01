# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import saashq
from pypika.terms import ExistsCriterion


def execute():
	pl = saashq.qb.DocType("Pick List")
	se = saashq.qb.DocType("Stock Entry")
	dn = saashq.qb.DocType("Delivery Note")

	(
		saashq.qb.update(pl).set(
			pl.status,
			(
				saashq.qb.terms.Case()
				.when(pl.docstatus == 0, "Draft")
				.when(pl.docstatus == 2, "Cancelled")
				.else_("Completed")
			),
		)
	).run()

	(
		saashq.qb.update(pl)
		.set(pl.status, "Open")
		.where(
			(
				ExistsCriterion(
					saashq.qb.from_(se).select(se.name).where((se.docstatus == 1) & (se.pick_list == pl.name))
				)
				| ExistsCriterion(
					saashq.qb.from_(dn).select(dn.name).where((dn.docstatus == 1) & (dn.pick_list == pl.name))
				)
			).negate()
			& (pl.docstatus == 1)
		)
	).run()
