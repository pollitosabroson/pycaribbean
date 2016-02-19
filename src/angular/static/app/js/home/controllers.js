demo.controller('bookList',
    function($scope, books) {
        $scope.books = books;
    }
);

demo.controller('singleBook',
    function($scope, bookInstance) {
        $scope.book = bookInstance;
    }
);

demo.controller('bookNew',
    function($scope, $location, Authors, Book) {
        $scope.authors = Authors;
        $scope.book = {};
        $scope.title = "Agregar";
        $scope.submit = "Agregar";

        $scope.submitForm = function() {
            $scope.instance = new Book();
            var prueba = Book.save($scope.book, function(data){
                $location.path('/')
            })
        }
    }
);

demo.controller('bookEdit',
    function($scope, $location, Authors, Book, bookInstance) {
        $scope.book = bookInstance;
        $scope.authors = Authors;
        $scope.title = "Editar";
        $scope.submit = "Guardar";

        $scope.submitForm = function() {
            Book.update({id: $scope.book.id},
                $scope.book,
                function(data){
                    $location.path('/')
                }
            );
        }
    }
);
