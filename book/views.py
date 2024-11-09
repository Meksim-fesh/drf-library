from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.serializers import BookListSerializer, BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        return BookSerializer

    def create(self, request, *args, **kwargs):
        """Creates an instance of Book model"""
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """Returns list of all Book instances"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Returns detail info about an instance of Book model"""
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Updates info about an instance of Book model
        (requires all fields to be provided)
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Updates info about an instance of Book model
        (does not require all fields to be provided)
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Deletes an instance of Book model"""
        return super().destroy(request, *args, **kwargs)
