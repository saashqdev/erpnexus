import saashq

no_cache = 1


def get_context(context):
	if saashq.session.user != "Guest":
		context.all_certifications = get_all_certifications_of_a_member()
		context.show_sidebar = True


def get_all_certifications_of_a_member():
	"""Returns all certifications"""
	all_certifications = []
	all_certifications = saashq.db.sql(
		""" select cc.name,cc.from_date,cc.to_date,ca.amount,ca.currency
		from `tabCertified Consultant` cc
		inner join `tabCertification Application` ca
		on cc.certification_application = ca.name
		where paid = 1 and email = %(user)s order by cc.to_date desc""",
		{"user": saashq.session.user},
		as_dict=True,
	)
	return all_certifications
