
var CremaScript = (function () {
    function CremaScript(Options) {
        var _this = this;
        this.Options = Options;
        
        this.Start = function () {
            return _this;
        };

        this.Open = function (e) {
            
            return _this;
        };
        
        this.Options = this.ConfigureDefaults(Options);

        if (window.localStorage.getItem("load_front") == "no") {
            // var obj = document.getElementById("text_pannel");
            var obj = this.getAllElementsWithAttribute("itemprop", "description");
            console.log("++++++++++++++ obj +++++++++++++++", obj);
            if (obj != []) {
                var str = "<h3 style='color:" + this.Options.font_color + ";font-weight:" + this.Options.font_weight + ";font-size:" + this.Options.font_size + ";'>" + this.Options.content + "&nbsp;&nbsp;&nbsp;&nbsp;" + this.Options.days + " Days" + "&nbsp;&nbsp;" + this.Options.hours + " Hours" + "&nbsp;&nbsp;" + this.Options.mins + " Minutes" + "&nbsp;&nbsp;" + this.Options.secs + " Seconds" + "&nbsp;&nbsp;" + "Left! Hurry Up." + "</h3>";
                obj[0].insertAdjacentHTML("beforeend", str);
            }
            window.localStorage.setItem("load_front", "yes");
        }

    }

    CremaScript.prototype.getAllElementsWithAttribute = function (attribute, value)
    {
      var matchingElements = [];
      var allElements = document.getElementsByTagName('div');
      for (var i = 0, n = allElements.length; i < n; i++)
      {
        if (allElements[i].getAttribute(attribute) !== null)
        {
          // Element exists with attribute. Add to array.
          console.log("++++++++++++ attributes ++++++++++", allElements[i].attribute);
          // if (allElements[i].attribute[1].value = "description") {
          //   console.log("++++++++++++ matched ++++++++++++", allElements[i]);
          // }
          
          matchingElements.push(allElements[i]);
        }
      }
      return matchingElements;
    }


    CremaScript.prototype.ConfigureDefaults = function (options) {
        var output = {};
        for (var attrName in options) {
            output[attrName] = options[attrName];
        }
        return output;
    };
    return CremaScript;
})();