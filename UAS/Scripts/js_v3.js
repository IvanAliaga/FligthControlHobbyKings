var cantidad = 1;
var imagenArray = [];

function downloadURI(uri, name) { 
	var link = document.createElement("a"); 
	link.download = name; 
	link.href = uri; 
	link.click(); 
var imagen = document.createElement("img");
	imagen.src = uri;//"../static/image/marker_UAS.png";

	imagen.id = "imagen"+cantidad;
	imagen.width = 250;
	imagen.height = 250;
	var div =document.getElementById("divImg");
	imagenArray.push(imagen);
	div.appendChild(imagen);
	var link = document.createElement("a"); 
	
	console.log(imagenArray);
	cantidad++;
}


