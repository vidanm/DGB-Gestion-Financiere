function showChantier(id) {
	var x = document.getElementById(id);
	if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}

window.addEventListener("load", function(){
	var x = document.getElementById("syntheseform");
	x.style.display = "none";

	var y = document.getElementById("chantierform");
	y.style.display = "none";

	var z = document.getElementById("structureform");
	z.style.display = "none";

	var w = document.getElementById("diversform");
	w.style.display = "none";

	
	var buttonChantier = document.getElementById("buttonChantier");
	var buttonSynthese = document.getElementById("buttonSynthese");
	var buttonStructure = document.getElementById("buttonStructure");
	var buttonDivers = document.getElementById("buttonDivers");
	/* buttonChantier.disabled = true;
	buttonSynthese.disabled = true;
	buttonStructure.disabled = true; */
});
