(function (window, angular, undefined) {'use strict';

angular.module('vo.api', ['ng'])
    .provider('$api', function() {
        // The base api endpoint to construct the resources urls.
        this.apiEndpoint = '';
    
        // Tell if the api uses trailing slashes in its urls or not.
        this.apiUsesTrailingSlash = undefined;
    

        var appendTrailingSlash = function(url) {
            return url.replace(/\/?(\?|#|$)/, '/$1');
        };

        var stripTrailingSlash = function(url) {
            return url.replace(/\/?(\?|#|$)/, '$1');
        };
        
        var makeAbsoluteUrl = function(url, trailingSlash) {
            // Handle absolute URLs (with protocol-relative prefix)
            // Example: //domain.com/file.png
            if (url.search(/^\/\//) != -1) {
                url = window.location.protocol + url;
            }

            // Handle absolute URLs (with explicit origin)
            // Example: http://domain.com/file.png
            else if (url.search(/:\/\//) != -1) {
                url = url;
            }

            // Handle absolute URLs (without explicit origin)
            // Example: /file.png
            else if (url.search(/^\//) != -1) {
                url = window.location.origin + url;
            }

            // Handle relative URLs
            // Example: file.png
            else {
                var base = window.location.href.match(/(.*\/)/)[0]
                url = base + url;
            }

            if (trailingSlash === false) {
                return stripTrailingSlash(url);
            }
            else if (trailingSlash === true) {
                return appendTrailingSlash(url);
            }

            return url;
        };

        
        this.url = function(url) {
            url = appendTrailingSlash(provider.apiEndpoint) + url.replace(/^\/+/, '');
            return makeAbsoluteUrl(url);
        };


        var provider = this;
        
        this.$get = [function() {
            var providerDefinitionObject = {
                url: function(url) {
                    return provider.url(url, provider.apiUsesTrailingSlash);
                }
            };
    
            return providerDefinitionObject;
        }];
    });
    
})(window, window.angular); 
