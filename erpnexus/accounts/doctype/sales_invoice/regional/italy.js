saashq.ui.form.on("Sales Invoice", {
	refresh: (frm) => {
		if (frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Generate E-Invoice"), () => {
				frm.call({
					method: "erpnexus.regional.italy.utils.generate_single_invoice",
					args: {
						docname: frm.doc.name,
					},
					callback: function (r) {
						frm.reload_doc();
						if (r.message) {
							open_url_post(saashq.request.url, {
								cmd: "saashq.core.doctype.file.file.download_file",
								file_url: r.message,
							});
						}
					},
				});
			});
		}
	},
});
