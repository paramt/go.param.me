function getCSV(file, callback){
	var xhttp = new XMLHttpRequest();

	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			data = Papa.parse(this.responseText).data;
			callback(data);
		}
	};

	xhttp.open("GET", file, true);
	xhttp.send();
}

function redirect(data){
	utm = `utm_source=${config.shortDomain}&utm_campaign=redirect`;
	var currentURL = window.location.pathname.substr(1);
	var redirectURL = "";

	for(var i = 1; i < data.length - 1; i++){
		shortURL = data[i][0];
		longURL = data[i][1];

		if(currentURL == shortURL){
			redirectURL = longURL;
			utm += "&utm_medium=short-url";
		}
	}

	if(redirectURL === ""){
		redirectURL = config.defaultRedirect;
		utm += "&utm_medium=catch-all";
	}

	// Redirect to the correct URL and add a UTM if config.utm is set to true
	if(redirectURL.includes("?")){
		window.location = (config.utm) ? redirectURL + "&" + utm : redirectURL;
	} else {
		window.location = (config.utm) ? redirectURL + "?" + utm : redirectURL;
	}
}

getCSV(`https://raw.githubusercontent.com/${config.repo}/master/redirects.csv`, redirect)
