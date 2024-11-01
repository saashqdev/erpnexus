saashq.provide("erpnexus.demo");

$(document).on("toolbar_setup", function () {
	if (saashq.boot.sysdefaults.demo_company) {
		render_clear_demo_action();
	}
});

function render_clear_demo_action() {
	let demo_action = $(
		`<a class="dropdown-item" onclick="return erpnexus.demo.clear_demo()">
			${__("Clear Demo Data")}
		</a>`
	);

	demo_action.appendTo($("#toolbar-user"));
}

erpnexus.demo.clear_demo = function () {
	saashq.confirm(__("Are you sure you want to clear all demo data?"), () => {
		saashq.call({
			method: "erpnexus.setup.demo.clear_demo_data",
			freeze: true,
			freeze_message: __("Clearing Demo Data..."),
			callback: function (r) {
				saashq.ui.toolbar.clear_cache();
				saashq.show_alert({
					message: __("Demo data cleared"),
					indicator: "green",
				});
			},
		});
	});
};
