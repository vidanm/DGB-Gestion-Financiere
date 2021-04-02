function showChantier(id) {
	var x = document.getElementById(id);
	if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}

function requiredFiles(){
	var fs = require('fs');
	var numberOfRequiredFiles = 0
	var files = fs.readdirSync('var/')
	files.forEach(function(element) {
		if (element == "PlanComptable.xls" || element == "Charges.xls") {
			numberOfRequiredFiles += 1;
		}
	});

	if (numberOfRequiredFiles == 2)
		return true;
	return false;
}

window.addEventListener("load", function(){
	var x = document.getElementById("syntheseform");
	x.style.display = "none";

	var y = document.getElementById("chantierform");
	y.style.display = "none";

	var z = document.getElementById("structureform");
	z.style.display = "none";

	var buttonChantier = document.getElementById("buttonChantier");
	var buttonSynthese = document.getElementById("buttonSynthese");
	var buttonStructure = document.getElementById("buttonStructure");
	if ( requiredFiles() == false ){
		buttonChantier.disabled = true;
		buttonSynthese.disabled = true;
		buttonStructure.disabled = true;
	}
});
