function showChantier(id) {
	var x = document.getElementById(id);
	if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}


window.addEventListener("load", function(){
	var x = document.getElementById('syntheseform');
	x.style.display = "none";

	var y = document.getElementById('chantierform');
	y.style.display = "none";
});
