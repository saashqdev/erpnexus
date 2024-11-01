// Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

if (!window.erpnexus) window.erpnexus = {};

erpnexus.subscribe_to_newsletter = function (opts, btn) {
	return saashq.call({
		type: "POST",
		method: "saashq.email.doctype.newsletter.newsletter.subscribe",
		btn: btn,
		args: { email: opts.email },
		callback: opts.callback,
	});
};
