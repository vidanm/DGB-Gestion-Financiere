function showChantier(id) {
	var x = document.getElementById(id);
	if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}

function addOptions(){
	var xmlhttp = new XMLHttpRequest()
	xmlhttp.open("GET","/noms_chantiers");
	xmlhttp.send();
	xmlhttp.onload = function(){
		var txt = xmlhttp.responseText;
		var i = 0;
		var res = txt.split("\n");
		var x = document.getElementById("chantierSelect");
		for (i = 0; i < res.length; i++){
			console.log(res[i]);
			var option = document.createElement("option");
			option.text = res[i];
			x.add(option);
		}
	};
}

window.addEventListener("load", function(){
	
	addOptions();

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


