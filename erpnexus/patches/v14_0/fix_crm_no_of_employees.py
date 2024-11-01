import saashq


def execute():
	options = {
		"11-20": "11-50",
		"21-30": "11-50",
		"31-100": "51-200",
		"101-500": "201-500",
		"500-1000": "501-1000",
		">1000": "1000+",
	}

	for doctype in ("Lead", "Opportunity", "Prospect"):
		saashq.reload_doctype(doctype)
		for key, value in options.items():
			saashq.db.sql(
				f"""
                update `tab{doctype}`
                set no_of_employees = %s
                where no_of_employees = %s
            """,
				(value, key),
			)
