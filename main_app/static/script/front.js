
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
            var obj = document.getElementById("text_pannel");
            console.log("++++++++++++++ obj +++++++++++++++", obj);
            if (obj) {
                var str = "<h3 style='color:" + this.Options.font_color + ";font-weight:" + this.Options.font_weight + ";font-size:" + this.Options.font_size + ";'>" + this.Options.content + "&nbsp;&nbsp;&nbsp;&nbsp;" + this.Options.days + " Days" + "&nbsp;&nbsp;" + this.Options.hours + " Hours" + "&nbsp;&nbsp;" + "Left! Hurry Up." + "</h3>";
                obj.insertAdjacentHTML("beforeend", str);
            }
            window.localStorage.setItem("load_front", "yes");
        }

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