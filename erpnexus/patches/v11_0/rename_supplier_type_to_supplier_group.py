import saashq
from saashq import _
from saashq.model.utils.rename_field import rename_field
from saashq.utils.nestedset import rebuild_tree


def execute():
	if saashq.db.table_exists("Supplier Group"):
		saashq.reload_doc("setup", "doctype", "supplier_group")
	elif saashq.db.table_exists("Supplier Type"):
		saashq.rename_doc("DocType", "Supplier Type", "Supplier Group", force=True)
		saashq.reload_doc("setup", "doctype", "supplier_group")
		saashq.reload_doc("accounts", "doctype", "pricing_rule")
		saashq.reload_doc("accounts", "doctype", "tax_rule")
		saashq.reload_doc("buying", "doctype", "buying_settings")
		saashq.reload_doc("buying", "doctype", "supplier")
		rename_field("Supplier Group", "supplier_type", "supplier_group_name")
		rename_field("Supplier", "supplier_type", "supplier_group")
		rename_field("Buying Settings", "supplier_type", "supplier_group")
		rename_field("Pricing Rule", "supplier_type", "supplier_group")
		rename_field("Tax Rule", "supplier_type", "supplier_group")

	build_tree()


def build_tree():
	saashq.db.sql(
		"""update `tabSupplier Group` set parent_supplier_group = '{}'
		where is_group = 0""".format(_("All Supplier Groups"))
	)

	if not saashq.db.exists("Supplier Group", _("All Supplier Groups")):
		saashq.get_doc(
			{
				"doctype": "Supplier Group",
				"supplier_group_name": _("All Supplier Groups"),
				"is_group": 1,
				"parent_supplier_group": "",
			}
		).insert(ignore_permissions=True)

	rebuild_tree("Supplier Group")
