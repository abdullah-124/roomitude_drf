from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from products.models import FurnitureProduct
from products.serializers import FurnitureProductSerializer


class ProductView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    queryset = FurnitureProduct.objects.all()
    serializer_class = FurnitureProductSerializer

    def get(self, request, pk=None):
        if pk is not None:
            return self.retrieve(request, pk=pk)
        return self.list(request)
