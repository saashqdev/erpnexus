import saashq


def execute():
	saashq.reload_doctype("Opportunity")
	if saashq.db.has_column("Opportunity", "enquiry_from"):
		saashq.db.sql(
			""" UPDATE `tabOpportunity` set opportunity_from = enquiry_from
			where ifnull(opportunity_from, '') = '' and ifnull(enquiry_from, '') != ''"""
		)

	if saashq.db.has_column("Opportunity", "lead") and saashq.db.has_column("Opportunity", "enquiry_from"):
		saashq.db.sql(
			""" UPDATE `tabOpportunity` set party_name = lead
			where enquiry_from = 'Lead' and ifnull(party_name, '') = '' and ifnull(lead, '') != ''"""
		)

	if saashq.db.has_column("Opportunity", "customer") and saashq.db.has_column(
		"Opportunity", "enquiry_from"
	):
		saashq.db.sql(
			""" UPDATE `tabOpportunity` set party_name = customer
			 where enquiry_from = 'Customer' and ifnull(party_name, '') = '' and ifnull(customer, '') != ''"""
		)
