demo.config([
    '$contentProvider', '$stateProvider',
    function($contentProvider, $stateProvider) {
        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: $contentProvider.url('home/base.html'),
                abstract: true
            })
            .state('home.list', {
                url: '',
                controller: 'bookList',
                templateUrl: $contentProvider.url('home/list.html'),
                resolve: {
                    books: function(Book) {
                        return Book.query().$promise;
                    }
                }

            })
            .state('home.detail', {
                url: 'book/{bookId:[0-9]+}',
                templateUrl: $contentProvider.url('home/bookdetail.html'),
                controller: 'singleBook',
                resolve: {
                    bookInstance: function($stateParams, Book) {
                        return Book.get({id: $stateParams.bookId}).$promise;
                    }
                }
            })
            .state('home.create', {
                url: 'book/new',
                controller: 'bookNew',
                templateUrl: $contentProvider.url('home/newbook.html'),
                resolve: {
                    Authors: function(Author) {
                        return Author.query().$promise;
                    }
                }

            })
            .state('home.edit', {
                url: 'book/:bookId/edit',
                controller: 'bookEdit',
                templateUrl: $contentProvider.url('home/newbook.html'),
                resolve: {
                    Authors: function(Author) {
                        return Author.query().$promise;
                    },
                    bookInstance: function($stateParams, Book) {
                        return Book.get({id: $stateParams.bookId}).$promise;
                    }
                }

            });
    }
]);