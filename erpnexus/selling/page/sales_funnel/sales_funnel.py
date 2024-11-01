# Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from itertools import groupby

import saashq
from saashq import _
from saashq.utils import flt

from erpnexus.accounts.report.utils import convert


def validate_filters(from_date, to_date, company):
	if from_date and to_date and (from_date >= to_date):
		saashq.throw(_("To Date must be greater than From Date"))

	if not company:
		saashq.throw(_("Please Select a Company"))


@saashq.whitelist()
def get_funnel_data(from_date, to_date, company):
	validate_filters(from_date, to_date, company)

	active_leads = saashq.db.sql(
		"""select count(*) from `tabLead`
		where (date(`creation`) between %s and %s)
		and company=%s""",
		(from_date, to_date, company),
	)[0][0]

	opportunities = saashq.db.sql(
		"""select count(*) from `tabOpportunity`
		where (date(`creation`) between %s and %s)
		and opportunity_from='Lead' and company=%s""",
		(from_date, to_date, company),
	)[0][0]

	quotations = saashq.db.sql(
		"""select count(*) from `tabQuotation`
		where docstatus = 1 and (date(`creation`) between %s and %s)
		and (opportunity!="" or quotation_to="Lead") and company=%s""",
		(from_date, to_date, company),
	)[0][0]

	converted = saashq.db.sql(
		"""select count(*) from `tabCustomer`
		JOIN `tabLead` ON `tabLead`.name = `tabCustomer`.lead_name
		WHERE (date(`tabCustomer`.creation) between %s and %s)
		and `tabLead`.company=%s""",
		(from_date, to_date, company),
	)[0][0]

	return [
		{"title": _("Active Leads"), "value": active_leads, "color": "#B03B46"},
		{"title": _("Opportunities"), "value": opportunities, "color": "#F09C00"},
		{"title": _("Quotations"), "value": quotations, "color": "#006685"},
		{"title": _("Converted"), "value": converted, "color": "#00AD65"},
	]


@saashq.whitelist()
def get_opp_by_utm_source(from_date, to_date, company):
	return get_opp_by("utm_source", from_date, to_date, company)


@saashq.whitelist()
def get_opp_by_utm_campaign(from_date, to_date, company):
	return get_opp_by("utm_campaign", from_date, to_date, company)


@saashq.whitelist()
def get_opp_by_utm_medium(from_date, to_date, company):
	return get_opp_by("utm_medium", from_date, to_date, company)


def get_opp_by(by_field, from_date, to_date, company):
	validate_filters(from_date, to_date, company)

	opportunities = saashq.get_all(
		"Opportunity",
		filters=[
			["status", "in", ["Open", "Quotation", "Replied"]],
			["company", "=", company],
			["transaction_date", "Between", [from_date, to_date]],
		],
		fields=["currency", "sales_stage", "opportunity_amount", "probability", by_field],
	)

	if opportunities:
		default_currency = saashq.get_cached_value("Global Defaults", "None", "default_currency")

		cp_opportunities = [
			dict(
				x,
				**{
					"compound_amount": (
						convert(x["opportunity_amount"], x["currency"], default_currency, to_date)
						* x["probability"]
						/ 100
					)
				},
			)
			for x in opportunities
		]

		summary = {}
		sales_stages = set()
		group_key = lambda o: (o[by_field], o["sales_stage"])  # noqa
		for (by_field_group, sales_stage), rows in groupby(
			sorted(cp_opportunities, key=group_key), group_key
		):
			summary.setdefault(by_field_group, {})[sales_stage] = sum(r["compound_amount"] for r in rows)
			sales_stages.add(sales_stage)

		pivot_table = []
		for sales_stage in sales_stages:
			row = []
			for sales_stage_values in summary.values():
				row.append(flt(sales_stage_values.get(sales_stage)))
			pivot_table.append({"chartType": "bar", "name": sales_stage, "values": row})

		result = {"datasets": pivot_table, "labels": list(summary.keys())}
		return result

	else:
		return "empty"


@saashq.whitelist()
def get_pipeline_data(from_date, to_date, company):
	validate_filters(from_date, to_date, company)

	opportunities = saashq.get_all(
		"Opportunity",
		filters=[
			["status", "in", ["Open", "Quotation", "Replied"]],
			["company", "=", company],
			["transaction_date", "Between", [from_date, to_date]],
		],
		fields=["currency", "sales_stage", "opportunity_amount", "probability"],
	)

	if opportunities:
		default_currency = saashq.get_cached_value("Global Defaults", "None", "default_currency")

		cp_opportunities = [
			dict(
				x,
				**{
					"compound_amount": (
						convert(x["opportunity_amount"], x["currency"], default_currency, to_date)
						* x["probability"]
						/ 100
					)
				},
			)
			for x in opportunities
		]

		summary = {}
		for sales_stage, rows in groupby(cp_opportunities, lambda o: o["sales_stage"]):
			summary[sales_stage] = sum(flt(r["compound_amount"]) for r in rows)

		result = {
			"labels": list(summary.keys()),
			"datasets": [{"name": _("Total Amount"), "values": list(summary.values()), "chartType": "bar"}],
		}
		return result

	else:
		return "empty"
