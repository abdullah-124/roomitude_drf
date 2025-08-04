
from rest_framework.viewsets import ModelViewSet
from site_admin.decorators import IsSuperUser
from products.models import FurnitureProduct
from account.models import User
from site_admin.serializers import UserSerializerAdmin
from site_admin.serializers import FurnitureSerializerAdmin

# Create your views here.
class FurnitureAdminView(ModelViewSet):
    queryset = FurnitureProduct.objects.all()
    serializer_class = FurnitureSerializerAdmin
    permission_classes = [IsSuperUser]


class UserAdminView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerAdmin
    permission_classes = [IsSuperUser]