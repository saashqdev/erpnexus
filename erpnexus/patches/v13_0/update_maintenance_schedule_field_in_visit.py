import saashq


def execute():
	saashq.reload_doctype("Maintenance Visit")
	saashq.reload_doctype("Maintenance Visit Purpose")

	# Updates the Maintenance Schedule link to fetch serial nos
	from saashq.query_builder.functions import Coalesce

	mvp = saashq.qb.DocType("Maintenance Visit Purpose")
	mv = saashq.qb.DocType("Maintenance Visit")

	saashq.qb.update(mv).join(mvp).on(mvp.parent == mv.name).set(
		mv.maintenance_schedule, Coalesce(mvp.prevdoc_docname, "")
	).where((mv.maintenance_type == "Scheduled") & (mvp.prevdoc_docname.notnull()) & (mv.docstatus < 2)).run(
		as_dict=1
	)
