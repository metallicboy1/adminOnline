"""adminOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from gestionUniformes import views
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard),
    path('confirmar_talla/<int:clvcont>',views.confirmar_talla),
    path('confirmar_entrega/<int:clvcont>',views.confirmar_entrega),
    path('recordatorio/<int:tipo>/<int:clvcont>',views.Enviar_correo_recordatorio),
    path('confirmar_pedido/',views.confirmar_pedido, name='confirmar_pedido'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('aplicaciones/',views.aplicaciones, name='aplicaciones'), 
    path('uniformes/',views.uniformes, name='uniformes'),
    path('reporte_general/',views.reporte_general, name='reporte_general'),
    path('bot_uniformes/',views.bot_uniformes),
    path('bot_correos/',views.bot_correos),
    path('correo_almacen/',views.Enviar_correo_almacen),
    path('borrar_errores/',views.borrar_errores),
    path('login/',LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('redireccion/', views.redireccion, name='redireccion'),

]
