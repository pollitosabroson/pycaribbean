'use strict';

var demo = angular.module('demo', [
    'ngResource', 'ui.router', 'vo.api', 'vo.content', 'ui.bootstrap', 'ngStorage', 'base64'
]);


demo.config([
    '$apiProvider', '$contentProvider', '$httpProvider', '$locationProvider',
    function($apiProvider, $contentProvider, $httpProvider, $locationProvider) {
        $apiProvider.apiEndpoint = 'http://'+ window.location.host + '/api';
        $apiProvider.apiUsesTrailingSlash = true;

        /* Configure content base url */
        $contentProvider.urlPrefix = '/assets/app/partials/';

        /* Enable HTML5 mode */
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');

        /* Set request and response interceptors */
        /*$httpProvider.interceptors.push('HttpErrorInterceptor');
        
        // Token interceptor for django requests.
        $httpProvider.interceptors.push('TokenInterceptor');*/
    }
]);


/*demo.run([
    '$rootScope', 'HttpErrorService', '$content', '$localStorage', '$interval', 'ValidateTokens',
    function($rootScope, HttpErrorService, $content, $localStorage, $interval, ValidateTokens) {
                // Check route permissions and start the progress bar if required.

    }
]);
*/