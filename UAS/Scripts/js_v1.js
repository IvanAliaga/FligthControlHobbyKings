var map, place, vcircle, marker, placeReal, mapOptions;
var markerArray = [];
var cantidad = 1;
var poly, path;
var velocidadDrone, tiempoBateriaDrone, porcentajeError;
var valor, casa, first;
var cantidad = 1;
var imagenArray = [];

var lat=0,lng=0;

/*var ws = new WebSocket("ws://192.168.0.32:8080/websocket");
    ws.onmessage = function (evt) {
        var str =evt.data;      
        var objson = JSON.parse(str);
        lat = objson[0];
        lng = objson[1];
        realMaker();

    };
*/
function realMaker(){
     placeReal = new google.maps.LatLng(lat, lng);
     var drone = new google.maps.Marker({
     	position: placeReal,
        title: 'Real time',
        map: map,
        icon: '../static/image/marker_UAS.png',
      });
}
function initialize() {
	
	place = new google.maps.LatLng(lat, lng);
	var mapOptions = {
		zoom: 15,
		center: place,
		disableDoubleClickZoom: true,
		mapTypeControl: true,
	    mapTypeControlOptions: {
	      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
	    },
	    zoomControl: true,
	    zoomControlOptions: {
	      style: google.maps.ZoomControlStyle.SMALL
	    },
		mapTypeId: google.maps.MapTypeId.ROADMAP, 
	};

	map = new google.maps.Map(document.getElementById('map'), mapOptions);

	var drone = new google.maps.Marker({
		position: place,	
		title: 'Drone localizado',	
		map: map, 
		icon: '../static/image/marker_UAS.png',
	});

	document.getElementById('ptn-0').value = 'Punto Inicial';
	document.getElementById('lat-0').value = place.lat();
	document.getElementById('lon-0').value = place.lng();
	document.getElementById('alt-0').value = 0;

	google.maps.event.addListener(map, 'click', function(e) {
		velocidadDrone = document.getElementById('velIni').value; 
		tiempoBateriaDrone = document.getElementById('durBat').value*60;
		porcentajeError = (document.getElementById('prcErro').value)/100;
		var espacioRecorrido = velocidadDrone*tiempoBateriaDrone;
		var radio = espacioRecorrido/2-espacioRecorrido/2*porcentajeError;
		var coordURP = place;
		var distancia = google.maps.geometry.spherical.computeDistanceBetween(e.latLng,coordURP); 
		
		if (radio == 0) {
			alert("Crear Rango para agregar marcadores."); 
		} else if(distancia>radio) {
			alert("Seleccione un punto dentro del Rango establecido."); 				
		} else { 
			addMarker(e.latLng); 
		}
	});

	var line = {
		strokeColor: '#000000',
		strokeOpacity: 0.8,
		strokeWeight: 2
	};
	poly = new google.maps.Polyline(line);
	path = poly.getPath();
	path.push(place);	
}

function addMarker(position) {
	poly.setMap(map);
	path = poly.getPath();
	marker = new google.maps.Marker({
		position: position,
		center: position,
		map: map,
		title: 'Punto Nº ' + cantidad,
		animation: google.maps.Animation.DROP,
  	});  			
  	markerArray.push(marker);  	
  	path.push(position);
  	addText(position);


	var ws = new WebSocket("ws://192.168.0.32:8080/websocket");
    ws.onmessage = function (evt) {
        var str =evt.data;
        var objson = JSON.parse(str);
        lat = objson[0];
        lng = objson[1];
        realMaker();

    };



}


var disILA, disILO, disI;
function addText(position) {
	var salto = document.createElement('br');
  	salto.id = "salto-"+cantidad;

	var punto = document.createElement('input');
	punto.type = 'text';
	punto.id = 'ptn-'+cantidad;
	punto.value = 'Punto Nº '+cantidad;
	punto.disabled = true;
  	document.getElementById('divDir').appendChild(punto);
  	document.getElementById('divDir').appendChild(salto);

	var latitud = document.createElement('input');	
	latitud.type = 'text';
	latitud.name = 'lat-' +cantidad;
	latitud.id = 'lat-'+cantidad;
	latitud.value = position.lat();
	latitud.disabled = true;
  	document.getElementById('divLat').appendChild(latitud);
  	document.getElementById('divLat').appendChild(salto);

  	var longitud = document.createElement('input');
  	longitud.type = 'text';
  	longitud.name = 'log-' +cantidad;
  	longitud.id = 'log-'+ cantidad;
  	longitud.value = position.lng();
  	longitud.disabled = true;
  	document.getElementById('divLon').appendChild(longitud);
  	document.getElementById('divLon').appendChild(salto);

  	var altura = document.createElement('input');	
	altura.type = 'text';
	altura.name = 'alt-' +cantidad;
	altura.id = 'alt-'+cantidad;
	altura.disabled = true;
	altura.value = document.getElementById('altUra').value;
  	document.getElementById('divAlt').appendChild(altura);
  	document.getElementById('divAlt').appendChild(salto);

  	disILA = document.getElementById('lat-'+(cantidad-1)).value;
  	//var disILO = document.getElementById('log-'+(cantidad-1)).value;
  	//var disI = google.maps.LatLng(disILA, disILO);
  	//google.maps.geometry.spherical.computeDistanceBetween(position,disI)

  	var recorrido = document.createElement('input');	
	recorrido.type = 'text';
	recorrido.name = 'rec-' +cantidad;
	recorrido.id = 'rec-'+cantidad;
	recorrido.disabled = true;
	recorrido.value  = disILA;
  	document.getElementById('divDis').appendChild(recorrido);
  	document.getElementById('divDis').appendChild(salto);

  	document.getElementById('recorridoSob').value = cantidad;
  	cantidad++;
}

function redondeo(numero){
	var flotante = parseFloat(numero);
	var resultado = Math.round(flotante*100)/100;
	return resultado;
}

function createRecord(){
	if (vcircle == null) {
		velocidadDrone = document.getElementById('velIni').value; 
		tiempoBateriaDrone = document.getElementById('durBat').value*60;
		porcentajeError = (document.getElementById('prcErro').value)/100;
		var espacioRecorrido = velocidadDrone*tiempoBateriaDrone;
		var radio = espacioRecorrido/2-espacioRecorrido/2*porcentajeError;
		if(porcentajeError<0 || porcentajeError>1.1){
			alert('El porcentaje de Error se debe encontrar entre 0% y 100%');
			document.getElementById('prcErro').value = '';
			return false;
		}
		if(velocidadDrone<0 || velocidadDrone>3.1){
			alert('La velocidad del Drone se debe encontrar entre 0 m/s y 3 m/s');
			document.getElementById('velIni').value = '';
			return false;
		}
		if(tiempoBateriaDrone<0 || tiempoBateriaDrone>1800){
			alert('La duracion de la Bateria se debe encontrar entre 0 min y 30 min');
			document.getElementById('durBat').value = '';
			return false;
		} else {
			var range = {
				strokeColor: "#FA5858",	
				strokeOpacity: 0.8,	
				strokeWeight: 2,
				fillColor: "#FA5858",	
				fillOpacity: 0.45,	
				map: map,
				center: place,	
				radius: radio, 
				clickable: false,
			};
			vcircle = new google.maps.Circle(range);
			document.getElementById('recorridoMax').value = redondeo(radio*2);
			btnVisualizar();
		}
	} else {
		alert("Elimine el Rango Actual"); 
	}
}

function deleteRecord(){
	vcircle.setMap(null);
	vcircle = null;
	document.getElementById('velIni').value = '';
	document.getElementById('durBat').value = '';
	document.getElementById('recorridoMax').value = '';
	document.getElementById('altUra').value = '';
	document.getElementById('recorridoSob').value = '';
	document.getElementById('prcErro').value = '';
	deleteAll();
}

function deleteLast(){
	for(var i=markerArray.length-1;i<markerArray.length;i++){
		markerArray[i].setMap(null);
		document.getElementById('recorridoSob').value = i;
	}

	markerArray.length = markerArray.length - 1;

	for (var i = path.length - 1; i < path.length; i++) {
		path.removeAt(i);
	};
	
	cantidad = cantidad -1 ;

	for (var i = cantidad-1; i < cantidad; i++) {
		var di = document.getElementById("ptn-"+(i+1));
		di.remove();
		var la = document.getElementById("lat-"+(i+1));
		la.remove();
		var lo = document.getElementById("log-"+(i+1));
		lo.remove();
		var al = document.getElementById("alt-"+(i+1));
		al.remove();
		var re = document.getElementById("rec-"+(i+1));
		re.remove();
		var sa = document.getElementById("salto-"+(i+1));
		sa.remove();
	}
}

function deleteAll() {
	for (i in markerArray) {
	    markerArray[i].setMap(null); 
	}
	cantidad = 1;
	markerArray.length = 0;   

	for (i in path) {
		path.removeAt(i);
	};

	for (var i = 1; i >= cantidad; i++) {
		var X = document.getElementById("ptn-"+(i));
		X.remove();
		var X = document.getElementById("lat-"+(i));
		X.remove();
		var X = document.getElementById("log-"+(i));
		X.remove();
		var X = document.getElementById("alt-"+(i))
		X.remove();
		var X = document.getElementById("rec-"+(i))
		X.remove();	
		var X = document.getElementById("salto-"+(i))
		X.remove();
	};
}

function viewRange() {	
	if(valor == true){
		vcircle.setMap(map);
		valor = false;
	} else {
		vcircle.setMap(null);	
		valor = true;
	}		
}

function isNumber(e){
	var tecla = document.all ? tecla = e.keyCode : tecla = e.which;
	return ( (tecla > 47 && tecla < 58) || tecla == 8 || tecla == 46 );
}

function goHome(){
	var ultLa = place.lat();
	var ultLn = place.lng();
	casa = new google.maps.LatLng(ultLa, ultLn);
	path = poly.getPath();
	marker = new google.maps.Marker({
		position: casa,
		map: map,
		visible: false,
	});
	markerArray.push(marker);
	path.push(casa);
	addText(casa);
}

function goFirst(){
	var firstLa = document.getElementById('lat-1').value;
	var firstLn = document.getElementById('log-1').value;
	first = new google.maps.LatLng(firstLa, firstLn);
	path = poly.getPath();
	marker = new google.maps.Marker({
		position: first,
		map: map,
		visible: false,
	});  			
	markerArray.push(marker);  	
	path.push(first);
}


var imagenArray = [];
var canIm = 1;

function downloadURI(uri, name) { 
	var link = document.createElement("a"); 
	link.download = name; 
	link.href = uri; 
	link.click(); 
var imagen = document.createElement("img");
	imagen.src = "http://192.168.0.20:9000/?action=snapshot ";

	imagen.id = "imagen"+canIm;
	imagen.width = 250;
	imagen.height = 250;
	var div =document.getElementById("divImg");
	imagenArray.push(imagen);
	div.appendChild(imagen);
	var link = document.createElement("a"); 
	
	console.log(imagenArray);
	cantidad++;
}



google.maps.event.addDomListener(window, 'load', initialize);
