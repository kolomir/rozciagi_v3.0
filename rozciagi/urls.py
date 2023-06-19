from django.urls import path
from .views import wszystkie_wpisy, nowy_wpis,login_request,logout_request,filtrowanie

urlpatterns = [
    path('', nowy_wpis, name='home'),
    path('wszystkie/', wszystkie_wpisy, name='wszystkie_wpisy'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('eksport/', filtrowanie, name='filtrowanie'),
]