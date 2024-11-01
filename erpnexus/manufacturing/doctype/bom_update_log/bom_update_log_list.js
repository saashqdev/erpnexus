saashq.listview_settings["BOM Update Log"] = {
	add_fields: ["status"],
	get_indicator: (doc) => {
		let status_map = {
			Queued: "orange",
			"In Progress": "blue",
			Completed: "green",
			Failed: "red",
		};

		return [__(doc.status), status_map[doc.status], "status,=," + doc.status];
	},
	onload: () => {
		if (!saashq.model.can_write("Log Settings")) {
			return;
		}

		let sidebar_entry = $('<ul class="list-unstyled sidebar-menu log-retention-note"></ul>').appendTo(
			cur_list.page.sidebar
		);
		let message = __("Note: Automatic log deletion only applies to logs of type <i>Update Cost</i>");
		$(`<hr><div class='text-muted'>${message}</div>`).appendTo(sidebar_entry);

		saashq.require("logtypes.bundle.js", () => {
			saashq.utils.logtypes.show_log_retention_message(cur_list.doctype);
		});
	},
};
