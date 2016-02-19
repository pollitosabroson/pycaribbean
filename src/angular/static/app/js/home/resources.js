demo.factory('Book', [
    '$api', '$resource',
    function($api, $resource) {
        return $resource($api.url('books/:id'), {id: '@id'},
            {
                update: {
                    method: 'PUT'
                }
            });
    }
]);

demo.factory('Author', [
    '$api', '$resource',
    function($api, $resource) {
        return $resource($api.url('author'));
    }
]);