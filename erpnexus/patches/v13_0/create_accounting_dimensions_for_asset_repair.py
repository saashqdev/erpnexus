import saashq
from saashq.custom.doctype.custom_field.custom_field import create_custom_field


def execute():
	accounting_dimensions = saashq.db.get_all(
		"Accounting Dimension", fields=["fieldname", "label", "document_type", "disabled"]
	)

	if not accounting_dimensions:
		return

	for d in accounting_dimensions:
		doctype = "Asset Repair"
		field = saashq.db.get_value("Custom Field", {"dt": doctype, "fieldname": d.fieldname})
		docfield = saashq.db.get_value("DocField", {"parent": doctype, "fieldname": d.fieldname})

		if field or docfield:
			continue

		df = {
			"fieldname": d.fieldname,
			"label": d.label,
			"fieldtype": "Link",
			"options": d.document_type,
			"insert_after": "accounting_dimensions_section",
		}

		create_custom_field(doctype, df, ignore_validate=True)
		saashq.clear_cache(doctype=doctype)
