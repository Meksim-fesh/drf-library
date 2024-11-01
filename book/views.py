from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.serializers import BookListSerializer, BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        return BookSerializer
