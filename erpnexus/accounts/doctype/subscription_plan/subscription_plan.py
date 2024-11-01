# Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from dateutil import relativedelta
from saashq import _
from saashq.model.document import Document
from saashq.utils import date_diff, flt, get_first_day, get_last_day, getdate

from erpnexus.utilities.product import get_price


class SubscriptionPlan(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		billing_interval: DF.Literal["Day", "Week", "Month", "Year"]
		billing_interval_count: DF.Int
		cost: DF.Currency
		cost_center: DF.Link | None
		currency: DF.Link
		item: DF.Link
		payment_gateway: DF.Link | None
		plan_name: DF.Data
		price_determination: DF.Literal["", "Fixed Rate", "Based On Price List", "Monthly Rate"]
		price_list: DF.Link | None
		product_price_id: DF.Data | None
	# end: auto-generated types

	def validate(self):
		self.validate_interval_count()

	def validate_interval_count(self):
		if self.billing_interval_count < 1:
			saashq.throw(_("Billing Interval Count cannot be less than 1"))


@saashq.whitelist()
def get_plan_rate(
	plan, quantity=1, customer=None, start_date=None, end_date=None, prorate_factor=1, party=None
):
	plan = saashq.get_doc("Subscription Plan", plan)
	if plan.price_determination == "Fixed Rate":
		return plan.cost * prorate_factor

	elif plan.price_determination == "Based On Price List":
		if customer:
			customer_group = saashq.db.get_value("Customer", customer, "customer_group")
		else:
			customer_group = None

		price = get_price(
			item_code=plan.item,
			price_list=plan.price_list,
			customer_group=customer_group,
			company=None,
			qty=quantity,
			party=party,
		)
		if not price:
			return 0
		else:
			return price.price_list_rate * prorate_factor

	elif plan.price_determination == "Monthly Rate":
		start_date = getdate(start_date)
		end_date = getdate(end_date)

		no_of_months = relativedelta.relativedelta(end_date, start_date).months + 1
		cost = plan.cost * no_of_months

		# Adjust cost if start or end date is not month start or end
		prorate = saashq.db.get_single_value("Subscription Settings", "prorate")

		if prorate:
			cost -= plan.cost * get_prorate_factor(start_date, end_date)
		return cost


def get_prorate_factor(start_date, end_date):
	total_days_to_skip = date_diff(start_date, get_first_day(start_date))
	total_days_in_month = int(get_last_day(start_date).strftime("%d"))
	prorate_factor = flt(total_days_to_skip / total_days_in_month)

	total_days_to_skip = date_diff(get_last_day(end_date), end_date)
	total_days_in_month = int(get_last_day(end_date).strftime("%d"))
	prorate_factor += flt(total_days_to_skip / total_days_in_month)

	return prorate_factor
