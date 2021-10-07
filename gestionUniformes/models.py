from django.db import models

# Create your models here.
class PlantillaApoyo(models.Model):
    nonomina = models.IntegerField(db_column='NONOMINA', primary_key=True)  # Field name made lowercase.
    nopersona = models.IntegerField(db_column='NOPERSONA')  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=100)  # Field name made lowercase.
    rfc = models.CharField(db_column='RFC', max_length=20)  # Field name made lowercase.
    curp = models.CharField(db_column='CURP', max_length=25)  # Field name made lowercase.
    nss = models.CharField(db_column='NSS', max_length=50)  # Field name made lowercase.
    centrocostos = models.CharField(db_column='CENTROCOSTOS', max_length=255)  # Field name made lowercase.
    nosucursal = models.IntegerField(db_column='NOSUCURSAL')  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NOMBRESUCURSAL', max_length=150)  # Field name made lowercase.
    clvcontable = models.IntegerField(db_column='CLVCONTABLE')  # Field name made lowercase.
    desccontable = models.CharField(db_column='DESCCONTABLE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50, null=True)  # Field name made lowercase.
    puesto = models.CharField(db_column='PUESTO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FECHAINGRESO', max_length=20)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=10)  # Field name made lowercase.
    fechabaja = models.CharField(db_column='FECHABAJA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    motivobaja = models.CharField(db_column='MOTIVOBAJA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='NOMBRES', max_length=50)  # Field name made lowercase.
    ap_paterno = models.CharField(db_column='AP_PATERNO', max_length=50)  # Field name made lowercase.
    ap_materno = models.CharField(db_column='AP_MATERNO', max_length=50)  # Field name made lowercase.
    nombre_cia = models.CharField(db_column='NOMBRE_CIA', max_length=150)  # Field name made lowercase.
    num_solic = models.IntegerField(db_column='NUM_SOLIC', blank=True, null=True)  # Field name made lowercase.
    tel_casa = models.CharField(db_column='TEL_CASA', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tel_celular = models.CharField(db_column='TEL_CELULAR', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tsivale = models.CharField(db_column='TSIVALE', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'plantilla_apoyo'
    
    def __str__(self):
        return '%s %s %s' %(self.nopersona,self.nombre,self.estado)



class PlantillaFinanciera(models.Model):
    nonomina = models.IntegerField(db_column='NONOMINA', primary_key=True)  # Field name made lowercase.
    nopersona = models.IntegerField(db_column='NOPERSONA')  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=100)  # Field name made lowercase.
    rfc = models.CharField(db_column='RFC', max_length=20)  # Field name made lowercase.
    curp = models.CharField(db_column='CURP', max_length=25)  # Field name made lowercase.
    nss = models.CharField(db_column='NSS', max_length=50)  # Field name made lowercase.
    centrocostos = models.CharField(db_column='CENTROCOSTOS', max_length=255)  # Field name made lowercase.
    nosucursal = models.IntegerField(db_column='NOSUCURSAL')  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NOMBRESUCURSAL', max_length=150)  # Field name made lowercase.
    clvcontable = models.IntegerField(db_column='CLVCONTABLE')  # Field name made lowercase.
    desccontable = models.CharField(db_column='DESCCONTABLE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50, null=True)  # Field name made lowercase.
    puesto = models.CharField(db_column='PUESTO', max_length=100)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FECHAINGRESO', max_length=20)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=10)  # Field name made lowercase.
    fechabaja = models.CharField(db_column='FECHABAJA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    motivobaja = models.CharField(db_column='MOTIVOBAJA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='NOMBRES', max_length=50)  # Field name made lowercase.
    ap_paterno = models.CharField(db_column='AP_PATERNO', max_length=50)  # Field name made lowercase.
    ap_materno = models.CharField(db_column='AP_MATERNO', max_length=50)  # Field name made lowercase.
    nombre_cia = models.CharField(db_column='NOMBRE_CIA', max_length=150)  # Field name made lowercase.
    tel_casa = models.CharField(db_column='TEL_CASA', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tel_celular = models.CharField(db_column='TEL_CELULAR', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'plantilla_financiera'
    
    def __str__(self):
        return '%s %s %s' %(self.nopersona,self.nombre,self.estado)


class RegistroUniformes(models.Model):
    nopedido = models.AutoField(db_column='NOPEDIDO', primary_key=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='EMPRESA', max_length=10)  # Field name made lowercase.
    tiposolicitud = models.CharField(db_column='TIPOSOLICITUD', max_length=30)  # Field name made lowercase.
    fechasolicitud = models.DateField(db_column='FECHASOLICITUD')  # Field name made lowercase.
    nopersona = models.IntegerField(db_column='NOPERSONA')  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=150)  # Field name made lowercase.
    sexo = models.CharField(db_column='SEXO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    talla = models.CharField(db_column='TALLA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nosucursal = models.IntegerField(db_column='NOSUCURSAL')  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NOMBRESUCURSAL', max_length=100)  # Field name made lowercase.
    clvcontable = models.IntegerField(db_column='CLVCONTABLE')  # Field name made lowercase.
    fechaingreso = models.DateField(db_column='FECHAINGRESO')  # Field name made lowercase.
    correo = models.CharField(db_column='CORREO', max_length=150, blank=True, null=True)  # Field name made lowercase.
    correo_enviado = models.CharField(db_column='CORREO_ENVIADO', max_length=1)  # Field name made lowercase.
    fechaconfirmacion = models.DateField(db_column='FECHACONFIRMACION', blank=True, null=True)  # Field name made lowercase.
    fechapedido = models.DateField(db_column='FECHAPEDIDO', blank=True, null=True)  # Field name made lowercase.
    noseguimiento = models.CharField(db_column='NOSEGUIMIENTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.DateField(db_column='FECHAENTREGA', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registro_uniformes'

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' %(self.nopedido,self.empresa,self.tiposolicitud,self.fechasolicitud,self.nombre,self.nombresucursal,self.correo, self.estado)

class Sucursalesaef(models.Model):
    clave = models.CharField(db_column='CLAVE', max_length=10)  # Field name made lowercase.
    num_sucursal = models.IntegerField(db_column='Num_Sucursal', primary_key=True)  # Field name made lowercase.
    sucursal = models.CharField(db_column='Sucursal', max_length=100)  # Field name made lowercase.
    correo_subdirector = models.CharField(db_column='Correo_Subdirector', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo_zonal = models.CharField(db_column='Correo_Zonal', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo_sucursal = models.CharField(db_column='Correo_Sucursal', max_length=100, blank=True, null=True)  # Field name made lowercase.
    clave_suc = models.CharField(db_column='Clave_Suc', max_length=20)  # Field name made lowercase.
    flag = models.CharField(db_column='Flag', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sucursalesaef'

    def __str__(self):
        return '%s %s %s' %(self.clave,self.num_sucursal,self.sucursal)

class Sucursalesfisa(models.Model):
    numero_sucursal = models.IntegerField(db_column='Numero_Sucursal', primary_key=True)  # Field name made lowercase.
    sucursal = models.CharField(db_column='Sucursal', max_length=100)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10)  # Field name made lowercase.
    correo_gerente = models.CharField(db_column='Correo_Gerente', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo_zonal = models.CharField(db_column='Correo_Zonal', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo_subdirector = models.CharField(db_column='Correo_Subdirector', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo_analista = models.CharField(db_column='Correo_Analista', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sucursalesfisa'

    def __str__(self):
        return '%s %s %s' %(self.numero_sucursal,self.sucursal, self.tipo)

class TraductorAef(models.Model):
    sucursal = models.CharField(db_column='Sucursal', max_length=100)  # Field name made lowercase.
    zona = models.CharField(db_column='Zona', max_length=100)  # Field name made lowercase.
    subdireccion = models.CharField(db_column='Subdireccion', max_length=100)  # Field name made lowercase.
    num_sucursal = models.IntegerField(db_column='Num_Sucursal', primary_key=True)  # Field name made lowercase.
    clave_contable = models.IntegerField(db_column='Clave_Contable')  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'traductor_aef'

    def __str__(self):
        return '%s %s %s' %(self.sucursal, self.num_sucursal, self.clave_contable)