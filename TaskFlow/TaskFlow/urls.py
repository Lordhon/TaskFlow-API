
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet
from tasks.views import CreateUserAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView , TokenVerifyView
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)





urlpatterns = [

    path('admin/', admin.site.urls),
    path('register/', CreateUserAPI.as_view(), name='register'),
    path('api/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view() , name = 'login' ),
]
