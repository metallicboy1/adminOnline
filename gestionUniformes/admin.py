from django.contrib import admin
from gestionUniformes.models import PlantillaApoyo, PlantillaFinanciera, TraductorAef, Sucursalesaef, Sucursalesfisa, RegistroUniformes
# Register your models here.
class PlantillaApoyoAdmin(admin.ModelAdmin):
    list_display=("nopersona","nombre","nombresucursal","puesto","estado")

class PlantillaFinancieraAdmin(admin.ModelAdmin):
    list_display=("nopersona","nombre","nombresucursal","puesto","estado")

class SucursalesfisaAdmin(admin.ModelAdmin):
    list_display=("numero_sucursal","sucursal","tipo")

class SucursalesaefAdmin(admin.ModelAdmin):
    list_display=("clave","num_sucursal","sucursal")

class TraductoraefAdmin(admin.ModelAdmin):
    list_display=("sucursal","zona","subdireccion","num_sucursal","clave_contable","clave")

class RegistroUniformesAdmin(admin.ModelAdmin):
    list_display=("nopedido","empresa","tiposolicitud","fechasolicitud","nopersona","nombre","nosucursal","nombresucursal","correo","fechaconfirmacion","fechapedido","noseguimiento","fechaentrega","estado")

admin.site.register(PlantillaFinanciera, PlantillaFinancieraAdmin)
admin.site.register(PlantillaApoyo,PlantillaApoyoAdmin)
admin.site.register(Sucursalesfisa,SucursalesfisaAdmin)
admin.site.register(Sucursalesaef,SucursalesaefAdmin)
admin.site.register(TraductorAef,TraductoraefAdmin)
admin.site.register(RegistroUniformes,RegistroUniformesAdmin)