# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import copy

import saashq
from saashq.model.document import Document


class Brand(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.stock.doctype.item_default.item_default import ItemDefault

		brand: DF.Data
		brand_defaults: DF.Table[ItemDefault]
		description: DF.Text | None
		image: DF.AttachImage | None
	# end: auto-generated types

	pass


def get_brand_defaults(item, company):
	item = saashq.get_cached_doc("Item", item)
	if item.brand:
		brand = saashq.get_cached_doc("Brand", item.brand)

		for d in brand.brand_defaults or []:
			if d.company == company:
				row = copy.deepcopy(d.as_dict())
				row.pop("name")
				return row

	return saashq._dict()
