
from django.contrib import admin
from django.urls import include,path
from django.contrib.auth import views as auth_views
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('principal.urls')),
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
