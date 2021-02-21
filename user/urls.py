from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('',views.homepage,name='home'),
    path('cart/',views.cart,name='cart'),
    path('update_item/',views.updateitem,name='update_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/',views.register,name='register'),
]