from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.serializers import FurnitureProductSerializer
from products.models import FurnitureProduct
# Create your views here.
class FurnitureProductView(APIView):
    def get(self,request, id=None):
        try:
            if id:
                product = FurnitureProduct.objects.get(id=id)
                serializer = FurnitureProductSerializer(product, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                products = FurnitureProduct.objects.all()
                serializer = FurnitureProductSerializer(products, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except FurnitureProduct.DoesNotExist:
            return Response(
                {"detail": f"Product with id={id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# PRODUCT MANAGE API VIEW IT WILL DO
# POST, DELETE, PUT AND PATHCH

class ProductManageAPIView(GenericAPIView):
    queryset = FurnitureProduct.objects.all()
    serializer_class = FurnitureProductSerializer
    def get(self, request):
        id = request.query_params.get('id')
        if id is not None:
            try:
                product = self.get_queryset().get(id=id)
                serializer = self.get_serializer(product)
                return Response(serializer.data)
            except FurnitureProduct.DoesNotExist:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = self.get_queryset()
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created", "product": serializer.data}, status=201)
        return Response(serializer.errors, status=400)
    # update request 
    def put(self, request):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({"error": "ID is required"}, status=400)

        try:
            product = FurnitureProduct.objects.get(id=product_id)
        except FurnitureProduct.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated", "product": serializer.data})
        return Response(serializer.errors, status=400)
# pathc request
    def patch(self, request):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({"error": "ID is required"}, status=400)

        try:
            product = FurnitureProduct.objects.get(id=product_id)
        except FurnitureProduct.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product partially updated", "product": serializer.data})
        return Response(serializer.errors, status=400)
    # delete view
    def delete(self, request):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({"error": "ID is required for deletion"}, status=400)

        try:
            product = FurnitureProduct.objects.get(id=product_id)
            product.delete()
            return Response({"message": f"Product with ID {product_id} deleted successfully."}, status=200)
        except FurnitureProduct.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)