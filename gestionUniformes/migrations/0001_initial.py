# Generated by Django 3.2.6 on 2021-08-15 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlantillaApoyo',
            fields=[
                ('nonomina', models.IntegerField(db_column='NONOMINA', primary_key=True, serialize=False)),
                ('nopersona', models.IntegerField(db_column='NOPERSONA')),
                ('nombre', models.CharField(db_column='NOMBRE', max_length=100)),
                ('rfc', models.CharField(db_column='RFC', max_length=20)),
                ('curp', models.CharField(db_column='CURP', max_length=25)),
                ('nss', models.CharField(db_column='NSS', max_length=50)),
                ('centrocostos', models.CharField(db_column='CENTROCOSTOS', max_length=255)),
                ('nosucursal', models.IntegerField(db_column='NOSUCURSAL')),
                ('nombresucursal', models.CharField(db_column='NOMBRESUCURSAL', max_length=150)),
                ('clvcontable', models.IntegerField(db_column='CLVCONTABLE')),
                ('desccontable', models.CharField(blank=True, db_column='DESCCONTABLE', max_length=150, null=True)),
                ('departamento', models.CharField(db_column='DEPARTAMENTO', max_length=50)),
                ('puesto', models.CharField(blank=True, db_column='PUESTO', max_length=100, null=True)),
                ('fechaingreso', models.CharField(db_column='FECHAINGRESO', max_length=20)),
                ('estado', models.CharField(db_column='ESTADO', max_length=10)),
                ('fechabaja', models.CharField(blank=True, db_column='FECHABAJA', max_length=20, null=True)),
                ('motivobaja', models.CharField(blank=True, db_column='MOTIVOBAJA', max_length=255, null=True)),
                ('nombres', models.CharField(db_column='NOMBRES', max_length=50)),
                ('ap_paterno', models.CharField(db_column='AP_PATERNO', max_length=50)),
                ('ap_materno', models.CharField(db_column='AP_MATERNO', max_length=50)),
                ('nombre_cia', models.CharField(db_column='NOMBRE_CIA', max_length=150)),
                ('num_solic', models.IntegerField(blank=True, db_column='NUM_SOLIC', null=True)),
                ('tel_casa', models.CharField(blank=True, db_column='TEL_CASA', max_length=15, null=True)),
                ('tel_celular', models.CharField(blank=True, db_column='TEL_CELULAR', max_length=15, null=True)),
                ('tsivale', models.CharField(blank=True, db_column='TSIVALE', max_length=25, null=True)),
            ],
            options={
                'db_table': 'plantilla_apoyo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlantillaFinanciera',
            fields=[
                ('nonomina', models.IntegerField(db_column='NONOMINA', primary_key=True, serialize=False)),
                ('nopersona', models.IntegerField(db_column='NOPERSONA')),
                ('nombre', models.CharField(db_column='NOMBRE', max_length=100)),
                ('rfc', models.CharField(db_column='RFC', max_length=20)),
                ('curp', models.CharField(db_column='CURP', max_length=25)),
                ('nss', models.CharField(db_column='NSS', max_length=50)),
                ('centrocostos', models.CharField(db_column='CENTROCOSTOS', max_length=255)),
                ('nosucursal', models.IntegerField(db_column='NOSUCURSAL')),
                ('nombresucursal', models.CharField(db_column='NOMBRESUCURSAL', max_length=150)),
                ('clvcontable', models.IntegerField(db_column='CLVCONTABLE')),
                ('desccontable', models.CharField(blank=True, db_column='DESCCONTABLE', max_length=150, null=True)),
                ('departamento', models.CharField(db_column='DEPARTAMENTO', max_length=50)),
                ('puesto', models.CharField(db_column='PUESTO', max_length=100)),
                ('fechaingreso', models.CharField(db_column='FECHAINGRESO', max_length=20)),
                ('estado', models.CharField(db_column='ESTADO', max_length=10)),
                ('fechabaja', models.CharField(blank=True, db_column='FECHABAJA', max_length=20, null=True)),
                ('motivobaja', models.CharField(blank=True, db_column='MOTIVOBAJA', max_length=255, null=True)),
                ('nombres', models.CharField(db_column='NOMBRES', max_length=50)),
                ('ap_paterno', models.CharField(db_column='AP_PATERNO', max_length=50)),
                ('ap_materno', models.CharField(db_column='AP_MATERNO', max_length=50)),
                ('nombre_cia', models.CharField(db_column='NOMBRE_CIA', max_length=150)),
                ('tel_casa', models.CharField(blank=True, db_column='TEL_CASA', max_length=15, null=True)),
                ('tel_celular', models.CharField(blank=True, db_column='TEL_CELULAR', max_length=15, null=True)),
            ],
            options={
                'db_table': 'plantilla_financiera',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegistroUniformes',
            fields=[
                ('nopedido', models.AutoField(db_column='NOPEDIDO', primary_key=True, serialize=False)),
                ('empresa', models.CharField(db_column='EMPRESA', max_length=10)),
                ('tiposolicitud', models.CharField(db_column='TIPOSOLICITUD', max_length=30)),
                ('fechasolicitud', models.DateField(db_column='FECHASOLICITUD')),
                ('nopersona', models.IntegerField(db_column='NOPERSONA')),
                ('nombre', models.CharField(db_column='NOMBRE', max_length=150)),
                ('nosucursal', models.IntegerField(db_column='NOSUCURSAL')),
                ('nombresucursal', models.CharField(db_column='NOMBRESUCURSAL', max_length=100)),
                ('clvcontable', models.IntegerField(db_column='CLVCONTABLE')),
                ('fechaingreso', models.DateField(db_column='FECHAINGRESO')),
                ('correo', models.CharField(blank=True, db_column='CORREO', max_length=150, null=True)),
                ('fechaconfirmacion', models.DateField(blank=True, db_column='FECHACONFIRMACION', null=True)),
                ('fechapedido', models.DateField(blank=True, db_column='FECHAPEDIDO', null=True)),
                ('noseguimiento', models.CharField(blank=True, db_column='NOSEGUIMIENTO', max_length=255, null=True)),
                ('fechaentrega', models.DateField(blank=True, db_column='FECHAENTREGA', null=True)),
                ('estado', models.CharField(db_column='ESTADO', max_length=30)),
            ],
            options={
                'db_table': 'registro_uniformes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sucursalesaef',
            fields=[
                ('clave', models.CharField(db_column='CLAVE', max_length=10)),
                ('num_sucursal', models.IntegerField(db_column='Num_Sucursal', primary_key=True, serialize=False)),
                ('sucursal', models.CharField(db_column='Sucursal', max_length=100)),
                ('correo_subdirector', models.CharField(blank=True, db_column='Correo_Subdirector', max_length=100, null=True)),
                ('correo_zonal', models.CharField(blank=True, db_column='Correo_Zonal', max_length=100, null=True)),
                ('correo_sucursal', models.CharField(blank=True, db_column='Correo_Sucursal', max_length=100, null=True)),
                ('clave_suc', models.CharField(db_column='Clave_Suc', max_length=20)),
                ('flag', models.CharField(blank=True, db_column='Flag', max_length=255, null=True)),
            ],
            options={
                'db_table': 'sucursalesaef',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sucursalesfisa',
            fields=[
                ('numero_sucursal', models.IntegerField(db_column='Numero_Sucursal', primary_key=True, serialize=False)),
                ('sucursal', models.CharField(db_column='Sucursal', max_length=100)),
                ('tipo', models.CharField(db_column='Tipo', max_length=10)),
                ('correo_gerente', models.CharField(blank=True, db_column='Correo_Gerente', max_length=100, null=True)),
                ('correo_zonal', models.CharField(blank=True, db_column='Correo_Zonal', max_length=100, null=True)),
                ('correo_subdirector', models.CharField(blank=True, db_column='Correo_Subdirector', max_length=100, null=True)),
                ('correo_analista', models.CharField(blank=True, db_column='Correo_Analista', max_length=100, null=True)),
            ],
            options={
                'db_table': 'sucursalesfisa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TraductorAef',
            fields=[
                ('sucursal', models.CharField(db_column='Sucursal', max_length=100)),
                ('zona', models.CharField(db_column='Zona', max_length=100)),
                ('subdireccion', models.CharField(db_column='Subdireccion', max_length=100)),
                ('num_sucursal', models.IntegerField(db_column='Num_Sucursal', primary_key=True, serialize=False)),
                ('clave_contable', models.IntegerField(db_column='Clave_Contable')),
                ('clave', models.CharField(blank=True, db_column='Clave', max_length=10, null=True)),
            ],
            options={
                'db_table': 'traductor_aef',
                'managed': False,
            },
        ),
    ]