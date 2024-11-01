import saashq


def execute():
	pr_table = saashq.qb.DocType("Pricing Rule")
	(
		saashq.qb.update(pr_table)
		.set(pr_table.has_priority, 1)
		.where((pr_table.priority.isnotnull()) & (pr_table.priority != ""))
	).run()
