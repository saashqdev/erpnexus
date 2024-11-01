import click
import saashq
from saashq.utils import flt

import erpnexus
from erpnexus.setup.utils import get_exchange_rate


def execute():
	saashq.reload_doc(
		"accounts", "doctype", "currency_exchange_settings"
	)  # get_exchange_rate depends on Currency Exchange Settings
	saashq.reload_doctype("Opportunity")
	opportunities = saashq.db.get_list(
		"Opportunity",
		filters={"opportunity_amount": [">", 0]},
		fields=["name", "company", "currency", "opportunity_amount"],
	)

	for opportunity in opportunities:
		company_currency = erpnexus.get_company_currency(opportunity.company)

		if opportunity.currency is None or opportunity.currency == "":
			opportunity.currency = company_currency
			saashq.db.set_value(
				"Opportunity",
				opportunity.name,
				{"currency": opportunity.currency},
				update_modified=False,
			)
			click.secho(
				f' Opportunity `{opportunity.name}` has no currency set. Setting it to company currency as default: `{opportunity.currency}`"\n',
				fg="yellow",
			)

		# base total and total will be 0 only since item table did not have amount field earlier
		if opportunity.currency != company_currency:
			conversion_rate = get_exchange_rate(opportunity.currency, company_currency)
			base_opportunity_amount = flt(conversion_rate) * flt(opportunity.opportunity_amount)
		else:
			conversion_rate = 1
			base_opportunity_amount = flt(opportunity.opportunity_amount)

		saashq.db.set_value(
			"Opportunity",
			opportunity.name,
			{"conversion_rate": conversion_rate, "base_opportunity_amount": base_opportunity_amount},
			update_modified=False,
		)
