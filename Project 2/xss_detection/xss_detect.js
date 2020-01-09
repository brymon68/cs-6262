function notifyUser(message2) {
	var options = {type: "basic", title: "Popup alert for XSS", message: message2, iconUrl: "bt.png"};
	chrome.notifications.create(options, callback);
	function callback(){
	}
}

chrome.webRequest.onBeforeRequest.addListener(
   function (details) {
   var urlString = details.url.toString();
	 var script_start_re = /<\s*script(\s*>|\s+[\S\s]*?>)([\s\S]*?)<\s*\/\s*script\s*/igm

  	if(details.method == "POST") {
      body = JSON.stringify(details.requestBody);
       if (script_start_re.test(body)) {
         notifyUser("XSS detected! Your POST Request was not processed");
         return {cancel: true};
       }
  	}

    else if(details.method == "GET") {
			 //decode string first
			 var res = decodeURI(urlString);
			 //then do some find replace
			 res = res.replace(/\+/g,' ').replace(/\%3B/g,';').replace(/\%2F/g,'/');
       if (script_start_re.test(res)) {
         notifyUser("XSS detected! Your GET Request was not processed");
         return {cancel: true};
       }
  	}
},
{urls: ["<all_urls>"]}, ["blocking","requestBody"]);
