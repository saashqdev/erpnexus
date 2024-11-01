saashq.pages["visual-plant-floor"].on_page_load = function (wrapper) {
	var page = saashq.ui.make_app_page({
		parent: wrapper,
		title: "Visual Plant Floor",
		single_column: true,
	});

	saashq.visual_plant_floor = new saashq.ui.VisualPlantFloor(
		{ wrapper: $(wrapper).find(".layout-main-section") },
		wrapper.page
	);
};
