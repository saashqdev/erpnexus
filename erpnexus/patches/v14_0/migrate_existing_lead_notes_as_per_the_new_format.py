import saashq
from saashq.utils import cstr, strip_html


def execute():
	for doctype in ("Lead", "Prospect", "Opportunity"):
		if not saashq.db.has_column(doctype, "notes"):
			continue

		dt = saashq.qb.DocType(doctype)
		records = (
			saashq.qb.from_(dt).select(dt.name, dt.notes).where(dt.notes.isnotnull() & dt.notes != "")
		).run(as_dict=True)

		for d in records:
			if strip_html(cstr(d.notes)).strip():
				doc = saashq.get_doc(doctype, d.name)
				doc.append("notes", {"note": d.notes})
				doc.update_child_table("notes")

		saashq.db.sql_ddl(f"alter table `tab{doctype}` drop column `notes`")
