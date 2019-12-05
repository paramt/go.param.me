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
  var currentURL = window.location.href.split("go.param.me/")[1];
  var redirectURL = "";

  for(var i = 1; i < data.length - 1; i++){
    shortURL = data[i][0];
    longURL = data[i][1];

    if(currentURL == shortURL){
      redirectURL = longURL;
      console.log("Setting redirect URL to " + longURL);
    }
  }

  if(redirectURL === ""){
    redirectURL = "https://www.param.me";
    console.log("Invalid URL! Defaulting redirect URL to param.me");
  }

  console.log("Redirecting");
  window.location = redirectURL;
}

getCSV("https://raw.githubusercontent.com/paramt/go.param.me/master/redirects.csv", redirect)
