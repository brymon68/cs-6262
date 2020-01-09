function notifyUser(message) {
	var options = {type: "basic", title: "Popup alert for XSS", message: message, iconUrl: "bt.png"};
	chrome.notifications.create(options, callback);
	function callback(){
	}
}

chrome.webRequest.onBeforeRequest.addListener(
   function (details) {
   	var urlString = details.url.toString();
	 	var script_start_re = /(%3C|<)\s*script\s*(%3E|>)([\s\S]*?)(<|%3C)(\/|%2F)\s*script\s*(%3E|>)/igm

  	if(details.method == "POST") {
      body = JSON.stringify(details.requestBody);
       if (script_start_re.test(body)) {
         console.log("XSS detected!");
         notifyUser("XSS detected! Your POST Request was not processed");
         return {cancel: true};
       }
  	}

    else if(details.method == "GET") {
       if (script_start_re.test(urlString)) {
         console.log("XSS detected!");
         notifyUser("XSS detected! Your GET Request was not processed");
         return {cancel: true};
       }
  	}
},
{urls: ["<all_urls>"]}, ["blocking","requestBody"]);
