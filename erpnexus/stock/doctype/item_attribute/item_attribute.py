# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


import saashq
from saashq import _
from saashq.model.document import Document
from saashq.utils import flt

from erpnexus.controllers.item_variant import (
	InvalidItemAttributeValueError,
	validate_is_incremental,
	validate_item_attribute_value,
)


class ItemAttributeIncrementError(saashq.ValidationError):
	pass


class ItemAttribute(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.stock.doctype.item_attribute_value.item_attribute_value import ItemAttributeValue

		attribute_name: DF.Data
		from_range: DF.Float
		increment: DF.Float
		item_attribute_values: DF.Table[ItemAttributeValue]
		numeric_values: DF.Check
		to_range: DF.Float
	# end: auto-generated types

	def validate(self):
		saashq.flags.attribute_values = None
		self.validate_numeric()
		self.validate_duplication()

	def on_update(self):
		self.validate_exising_items()

	def validate_exising_items(self):
		"""Validate that if there are existing items with attributes, they are valid"""
		attributes_list = [d.attribute_value for d in self.item_attribute_values]

		# Get Item Variant Attribute details of variant items
		items = saashq.db.sql(
			"""
			select
				i.name, iva.attribute_value as value
			from
				`tabItem Variant Attribute` iva, `tabItem` i
			where
				iva.attribute = %(attribute)s
				and iva.parent = i.name and
				i.variant_of is not null and i.variant_of != ''""",
			{"attribute": self.name},
			as_dict=1,
		)

		for item in items:
			if self.numeric_values:
				validate_is_incremental(self, self.name, item.value, item.name)
			else:
				validate_item_attribute_value(
					attributes_list, self.name, item.value, item.name, from_variant=False
				)

	def validate_numeric(self):
		if self.numeric_values:
			self.set("item_attribute_values", [])
			if self.from_range is None or self.to_range is None:
				saashq.throw(_("Please specify from/to range"))

			elif flt(self.from_range) >= flt(self.to_range):
				saashq.throw(_("From Range has to be less than To Range"))

			if not self.increment:
				saashq.throw(_("Increment cannot be 0"), ItemAttributeIncrementError)
		else:
			self.from_range = self.to_range = self.increment = 0

	def validate_duplication(self):
		values, abbrs = [], []
		for d in self.item_attribute_values:
			if d.attribute_value.lower() in map(str.lower, values):
				saashq.throw(
					_("Attribute value: {0} must appear only once").format(d.attribute_value.title())
				)
			values.append(d.attribute_value)

			if d.abbr.lower() in map(str.lower, abbrs):
				saashq.throw(_("Abbreviation: {0} must appear only once").format(d.abbr.title()))
			abbrs.append(d.abbr)
