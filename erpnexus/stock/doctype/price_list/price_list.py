# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import saashq
from saashq import _, throw
from saashq.model.document import Document
from saashq.utils import cint


class PriceList(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.stock.doctype.price_list_country.price_list_country import PriceListCountry

		buying: DF.Check
		countries: DF.Table[PriceListCountry]
		currency: DF.Link
		enabled: DF.Check
		price_list_name: DF.Data
		price_not_uom_dependent: DF.Check
		selling: DF.Check
	# end: auto-generated types

	def validate(self):
		if not cint(self.buying) and not cint(self.selling):
			throw(_("Price List must be applicable for Buying or Selling"))

	def on_update(self):
		self.set_default_if_missing()
		self.update_item_price()
		self.delete_price_list_details_key()

	def set_default_if_missing(self):
		if cint(self.selling):
			if not saashq.db.get_single_value("Selling Settings", "selling_price_list"):
				saashq.set_value("Selling Settings", "Selling Settings", "selling_price_list", self.name)

		elif cint(self.buying):
			if not saashq.db.get_single_value("Buying Settings", "buying_price_list"):
				saashq.set_value("Buying Settings", "Buying Settings", "buying_price_list", self.name)

	def update_item_price(self):
		saashq.db.sql(
			"""update `tabItem Price` set currency=%s,
			buying=%s, selling=%s, modified=NOW() where price_list=%s""",
			(self.currency, cint(self.buying), cint(self.selling), self.name),
		)

	def on_trash(self):
		self.delete_price_list_details_key()

		def _update_default_price_list(module):
			b = saashq.get_doc(module + " Settings")
			price_list_fieldname = module.lower() + "_price_list"

			if self.name == b.get(price_list_fieldname):
				b.set(price_list_fieldname, None)
				b.flags.ignore_permissions = True
				b.save()

		for module in ["Selling", "Buying"]:
			_update_default_price_list(module)

	def delete_price_list_details_key(self):
		saashq.cache().hdel("price_list_details", self.name)


def get_price_list_details(price_list):
	price_list_details = saashq.cache().hget("price_list_details", price_list)

	if not price_list_details:
		price_list_details = saashq.get_cached_value(
			"Price List", price_list, ["currency", "price_not_uom_dependent", "enabled"], as_dict=1
		)

		if not price_list_details or not price_list_details.get("enabled"):
			throw(_("Price List {0} is disabled or does not exist").format(price_list))

		saashq.cache().hset("price_list_details", price_list, price_list_details)

	return price_list_details or {}
