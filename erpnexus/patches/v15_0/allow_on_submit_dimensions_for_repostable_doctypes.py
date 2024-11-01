import saashq

from erpnexus.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from erpnexus.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger import (
	get_allowed_types_from_settings,
)


def execute():
	for dt in get_allowed_types_from_settings():
		for dimension in get_accounting_dimensions():
			saashq.db.set_value("Custom Field", dt + "-" + dimension, "allow_on_submit", 1)
