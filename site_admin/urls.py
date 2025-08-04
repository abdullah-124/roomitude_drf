from django.urls import path, include
from rest_framework.routers import DefaultRouter
from site_admin.views import UserAdminView, FurnitureAdminView

# define router
router = DefaultRouter()
# regiseter url 
router.register('user', UserAdminView, basename='user_admin_view' )
router.register('products', FurnitureAdminView, basename='products_admin_view' )

urlpatterns = [
    path('', include(router.urls))
]
