# Copyright (c) 2020, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	saashq.reload_doc("setup", "doctype", "Email Digest")
	saashq.reload_doc("setup", "doctype", "Email Digest Recipient")
	email_digests = saashq.db.get_list("Email Digest", fields=["name", "recipient_list"])
	for email_digest in email_digests:
		if email_digest.recipient_list:
			for recipient in email_digest.recipient_list.split("\n"):
				doc = saashq.get_doc(
					{
						"doctype": "Email Digest Recipient",
						"parenttype": "Email Digest",
						"parentfield": "recipients",
						"parent": email_digest.name,
						"recipient": recipient,
					}
				)
				doc.insert()
