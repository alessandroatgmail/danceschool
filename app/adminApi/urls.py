from django.urls import path, include
from rest_framework.routers import DefaultRouter
from adminApi import views

router = DefaultRouter()
router.register('', views.AdminUserViewSets)


app_name = 'adminApi'

urlpatterns =[
    path('', include(router.urls)),

]
