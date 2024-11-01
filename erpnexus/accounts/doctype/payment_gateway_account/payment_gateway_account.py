# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq.model.document import Document


class PaymentGatewayAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		currency: DF.ReadOnly | None
		is_default: DF.Check
		message: DF.SmallText | None
		payment_account: DF.Link
		payment_channel: DF.Literal["", "Email", "Phone"]
		payment_gateway: DF.Link
	# end: auto-generated types

	def autoname(self):
		self.name = self.payment_gateway + " - " + self.currency

	def validate(self):
		self.currency = saashq.get_cached_value("Account", self.payment_account, "account_currency")

		self.update_default_payment_gateway()
		self.set_as_default_if_not_set()

	def update_default_payment_gateway(self):
		if self.is_default:
			saashq.db.sql(
				"""update `tabPayment Gateway Account` set is_default = 0
				where is_default = 1 """
			)

	def set_as_default_if_not_set(self):
		if not saashq.db.get_value(
			"Payment Gateway Account", {"is_default": 1, "name": ("!=", self.name)}, "name"
		):
			self.is_default = 1
