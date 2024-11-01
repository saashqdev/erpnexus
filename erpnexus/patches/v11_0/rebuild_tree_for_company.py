import saashq
from saashq.utils.nestedset import rebuild_tree


def execute():
	saashq.reload_doc("setup", "doctype", "company")
	rebuild_tree("Company")
