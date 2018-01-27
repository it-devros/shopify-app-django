

(function () {
	//Build a pseudo-class to prevent polluting our own scope.
    window.localStorage.setItem("load_script", "no");
    window.localStorage.setItem("load_front", "no");
	var api = {
		Settings: {},
		Vox: {},
		Start: function () {
			//The start function handles widget initialization.
            //Get the *.myshopify.com domain
            var shop = Shopify.shop;
            
            //Load the store owner's widget settings
            if (window.localStorage.getItem("load_script") == "no") {
                api.LoadSettings(shop, function (settings) {
                    //Save app settings
                    api.Settings = settings;
                    
                    //Load Riddlevox
                    api.LoadCremaScript(function () {
                        //Configure Riddlevox
                        api.Vox = api.ConfigureCremaScript(api.Settings);

                        //Show the widget!
                        api.Vox.Open();
                    });
                });
                window.localStorage.setItem("load_script", "yes");
            }
                

		},
		ExecuteJSONP: function (url, parameters, callback) {
			//This function will create and execute JSONP requests for other functions.

            //Prepare a function name that will be called when the JSONP request has loaded.
            //It should be unique, to prevent accidentally calling it multiple times.
            var callbackName = "MyAppJSONPCallback" + new Date().getMilliseconds();
            
            //Make the callback function available to the global scope, 
            //otherwise it can't be called when the settings are loaded.
            window[callbackName] = callback;
            
            //Convert the parameters into a querystring
            var kvps = ["callback=" + callbackName];
            var keys = Object.getOwnPropertyNames(parameters);
            
            for (var i = 0; i < keys.length; i++) {
                var key = keys[i];
                kvps.push(key + "=" + parameters[key]);
            }
            
            //Add a unique parameter to the querystring, to overcome browser caching.
            kvps.push("uid=" + new Date().getMilliseconds());
            
            var qs = "?" + kvps.join("&");
            
            //Build the script element, passing along the shop name and the load function's name
            var script = document.createElement("script");
            script.src = url + qs;
            script.async = true;
            script.type = "text/javascript";
            
            //Append the script to the document's head to execute it.
            document.head.appendChild(script);

		},
		LoadSettings: function (shop, callback) {
			//This function will load the app's settings from your app server.

            //Prepare a function to handle when the settings are loaded.
            var settingsLoaded = function (settings) {
                //Return the settings to the Start function so it can continue loading.
                callback(settings);
            };
            
            //Get the settings
            
            if (window.localStorage.getItem("load_script") == "no") {
                console.log(" +++++++++++++++++++++++ inrease api calls ++++++++++++++++");
                api.ExecuteJSONP("https://1a9c4247.ngrok.io/app/get_settings", { shop : shop }, settingsLoaded);

            }

		},
		LoadCremaScript: function (callback) {
			//This function loads our 3rd-party email capture library.
        
            //Build the script element
            var script = document.createElement("script");
            script.src = "https://1a9c4247.ngrok.io/static/script/front.js";
            script.async = true;
            script.type = "text/javascript";
            
            //Set the script's onload event to the callback, so api.Start can continue after Riddlevox has loaded.
            script.onload = callback;
            
            //Append the script and style to the document's head.
            document.head.appendChild(script);

		},
		ConfigureCremaScript: function (settings) {
			//This function configures Riddlevox with the store owner's settings.
            console.log('++++++++ settings +++++++');
            console.log(settings);
            //Build Riddlevox's options
            var options = {
                days: settings.days,
                hours: settings.hours,
                mins: settings.mins,
                secs: settings.secs,
                content: settings.content,
                font_color: settings.font_color,
                font_weight: settings.font_weight,
                font_size: settings.font_size
            };
            
            //Initialize and start riddlevox
            var vox = new CremaScript(options).Start();
            
            //Return this instance of Riddlevox to the calling function
            return vox;


		},
		
	};
	
	//Start the widget
	api.Start();
	
	//Optionally make the api available to the global scope for debugging.
	window["MyWidget"] = api;
}());
