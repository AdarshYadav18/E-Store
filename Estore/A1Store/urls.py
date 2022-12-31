from django.urls import path
from .import views
from .views import Index,Cart,Checkout,History
urlpatterns = [
    path('',views.F1,name='main'),
    path('menu/',Index.as_view(),name='homepage'),
    path('about/',views.F3),
    path('service',views.F4),
    path('login/',views.user_login,name='login'),
    path('signup/',views.sign_up,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    path('cart/',Cart.as_view(),name='cart'),
    path('check-out',Checkout.as_view(),name='checkout'),
    path('history',History.as_view(),name='history'),

]
