from django import template
from django.db import connection
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from .models import PlantillaApoyo, PlantillaFinanciera, RegistroUniformes
from Correos_bot.uniformes_1_correos import run_bot_uniformes
from django.core.mail import EmailMultiAlternatives, get_connection, message
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
import datetime
import string
import numpy as np
import threading
# Create your views here.

@login_required(login_url='/login/')
def confirmar_pedido(request):
    verificar_estado()
    registros = RegistroUniformes.objects.filter(estado = 'PEDIDO').order_by('clvcontable','talla')
    context={
        'registros':registros,
    }

    if(request.method == 'POST'):
        Numero_envio = request.POST.getlist('Numero_envio')
        clvcont = request.POST.getlist('clvcont')
        nopersona = request.POST.getlist('nopersona')
        actualizar_numero_envio(clvcont,Numero_envio,nopersona)
        return HttpResponse("<html><script>alert('¡Se ha confirmado correctamente!'); window.location.replace('/confirmar_pedido/')</script></html>")

    return render(request,"confirmar_pedido.html", context)

def confirmar_talla(request,clvcont):
    clave=clvcont
    verificar_estado()
    registros = RegistroUniformes.objects.filter(clvcontable=clvcont,estado = 'SOLICITUD')
    context={
        'registros':registros,
        'clvcont':clave
    }
    if(request.method == 'POST'):
        Sexo = request.POST.getlist('Sexo')
        Talla = request.POST.getlist('Talla')
        actualizar_Talla(Sexo,Talla,registros)
        return HttpResponse("<html><script>alert('¡Se ha confirmado correctamente!'); window.location.replace('/confirmar_talla/{}')</script></html>".format(clvcont))

    
    return render(request,"confirmar_talla.html", context)

def confirmar_entrega(request,clvcont):
    clave=clvcont
    verificar_estado()
    registros = RegistroUniformes.objects.filter(clvcontable=clvcont,estado = 'ENVIO')
    context={
        'registros':registros,
        'clvcont':clave
    }
    if(request.method == 'POST'):
        Llego=[]
        for registro in registros:
            nopersona = str(registro.nopersona)
            print(nopersona)
            Llego.append(request.POST.get(nopersona))
        Aclaraciones = request.POST.getlist("Aclaraciones")
        actualizar_Entrega(Llego,registros,Aclaraciones)
        return HttpResponse("<html><script>alert('¡Se ha confirmado correctamente!'); window.location.replace('/confirmar_entrega/{}')</script></html>".format(clvcont))

    
    return render(request,"confirmar_entrega.html", context)

def redireccion(request):

    if(request.user.is_superuser):
        return redirect('dashboard')
    else:
        return redirect('confirmar_pedido')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            print(f'USURAIO {username} CREADO')
            messages.success(request, f'Usuario {username} creado')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    
    context = {'form':form}
    return render(request,'login.html',context)

@login_required(login_url='/login/')
def dashboard(request):
    #verificar_estado()
    t = threading.Thread(target=verificar_estado, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    if(request.user.is_superuser):
        Solicitudes = RegistroUniformes.objects.filter(estado="SOLICITUD").count()
        Pedidos = RegistroUniformes.objects.filter(estado="PEDIDO").count()
        Envios = RegistroUniformes.objects.filter(estado="ENVIO").count()
        Entregados = RegistroUniformes.objects.filter(estado="ENTREGADO").count()
        Aclaraciones = RegistroUniformes.objects.filter(estado="ACLARACION").count()
        Cancelados = RegistroUniformes.objects.filter(estado="CANCELADO").count()

        context={
        'Solicitudes':Solicitudes,
        'Pedidos':Pedidos,
        'Envios':Envios,
        'Entregados':Entregados,
        'Aclaraciones':Aclaraciones,
        'Cancelados':Cancelados,
        'title':'Dashboard'
        }
        return render(request,"Dashboard.html", context)
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")

@login_required(login_url='/login/')
def aplicaciones(request):
    #verificar_estado()
    t = threading.Thread(target=verificar_estado, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    if(request.user.is_superuser):
        return render(request,"Aplicaciones.html", {'title':'Aplicaciones'})
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")

@login_required(login_url='/login/')
def uniformes(request):
    #verificar_estado()
    t = threading.Thread(target=verificar_estado, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    registros = RegistroUniformes.objects.all()
    context={
        'registros':registros,
        'title':'Uniformes'
    }
    if(request.user.is_superuser):
        return render(request,"Uniformes.html", context)
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")


#FUNCIONES DE BOTONES
@login_required(login_url='/login/')
def bot_uniformes(request):
    if(request.user.is_superuser):
        print("Se ejecuto bot uniformes")
        cancelados,solicitudes = run_bot_uniformes()
        if(solicitudes > 0):
            messages.success(request, '¡Se han creado nuevas solicitudes!')
        if(cancelados > 0):
            messages.error(request, 'Hubo algunos problemas revisa los errores.')
        if(cancelados <= 0 and solicitudes <= 0):
            messages.warning(request, 'Ya no hay más solicitudes nuevas.')
        return redirect('aplicaciones')
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")

@login_required(login_url='/login/')
def bot_correos(request):
    if(request.user.is_superuser):
        connection = get_connection()
        cont = 0
        limit=50
        registros = RegistroUniformes.objects.filter(estado = 'SOLICITUD').order_by('-clvcontable')
        clvcontable = 0
        connection.open()
        for registro in registros:
            if(clvcontable != registro.clvcontable and cont <= limit and registro.correo_enviado == False):
                clvcontable = registro.clvcontable
                personas = RegistroUniformes.objects.filter(estado = 'SOLICITUD', clvcontable = clvcontable)
                mail='financieraprueba123@gmail.com'
                link=f'localhost:8000/confirmar_talla/{personas[0].clvcontable}'
                context = {
                    'registros':personas,
                    'link':link
                }
                template = get_template('correo.html')
                content = template.render(context)
                mensajes = send_email(mail,content,0)
                mensajes.send()
                print(f"se envio correo a {registro.correo}")
                cont += 1
            if cont <= limit:
                RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(correo_enviado="1")


        connection.close()
        print (f"se enviaron {cont} correos.")
        registros= RegistroUniformes.objects.filter(correo_enviado=0,estado="SOLICITUD")
        faltan=0
        clvcontable = []
        for registro in registros:
            if(registro.clvcontable not in clvcontable):
                clvcontable.append(registro.clvcontable)               
                faltan += 1

        if faltan>0:
            messages.warning(request, f'¡Aun faltan {faltan} correos por enviar por favor espera 1 minuto y vuelve a ejecutar el bot!')
        elif cont >0:
            messages.success(request, f'¡Se estan enviado {cont} correos porfavor espera 1 minuto antes de usar el bot.')
        else:
            messages.error(request, 'Ya no hay más correos para enviar')
        
        return redirect('aplicaciones')
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")

@login_required(login_url='/login/')
def Enviar_correo_almacen(request):
    if(request.user.is_superuser):
        print("SE ENVIO CORREO AL ALMACEN")
        connection = get_connection()
        connection.open()
        mensajes = []
        mail='financieraprueba123@gmail.com'
        link=f'localhost:8000/confirmar_pedido/'
        context = {
            'link':link
        }
        template = get_template('correo_almacen.html')
        content = template.render(context)
        mensajes.append(send_email(mail,content,1))
        connection.send_messages(mensajes)
        connection.close()
        messages.success(request, '¡Se ha enviado un correo al almacen!')
        return redirect('aplicaciones')
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")

@login_required(login_url='/login/')
def Enviar_correo_recordatorio(request,tipo,clvcont):
    if(request.user.is_superuser):
        print("SE ENVIO RECORDATORIO")
        connection = get_connection()
        connection.open()
        if tipo == 0:
            personas = RegistroUniformes.objects.filter(estado = 'SOLICITUD', clvcontable = clvcont)
            mensajes = []
            mail='financieraprueba123@gmail.com'
            link=f'localhost:8000/confirmar_talla/{personas[0].clvcontable}'
            context = {
                'link':link,
                'registros':personas
            }
            template = get_template('correo.html')
            content = template.render(context)
            mensajes.append(send_email(mail,content,3))

        elif tipo == 1:
            mensajes = []
            mail='financieraprueba123@gmail.com'
            link=f'localhost:8000/confirmar_pedido/'
            context = {
                'link':link,
            }
            template = get_template('correo_almacen.html')
            content = template.render(context)
            mensajes.append(send_email(mail,content,1))

        elif tipo == 2:
            personas = RegistroUniformes.objects.filter(estado = 'ENVIO', clvcontable = clvcont)
            mensajes = []
            mail='financieraprueba123@gmail.com'
            link=f'localhost:8000/confirmar_entrega/{personas[0].clvcontable}'
            context = {
                'link':link,
                'registros':personas
            }
            template = get_template('correo_confirmar.html')
            content = template.render(context)
            mensajes.append(send_email(mail,content,4))
        
        connection.send_messages(mensajes)
        connection.close()
        messages.success(request, '¡Se ha enviado correo correctamente!')
        return redirect('uniformes')
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")

@login_required(login_url='/login/')
def borrar_errores(request):
    if(request.user.is_superuser):
        print("Se borraron errores")
        count_errores = RegistroUniformes.objects.filter(estado='ERROR').count()
        RegistroUniformes.objects.filter(estado='ERROR').delete()
        if(count_errores > 0):
            messages.success(request, '¡Se han borrado todos los errores!')
        else:
            messages.warning(request, 'Ya no hay más errores por borrar.')
        return redirect('aplicaciones')
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")


#FUNCIONES
def send_email(mail,content,tipo):
    if(tipo==0):
        email= EmailMultiAlternatives(
            'UNIFORMES - Confirmar Sexo y Talla',
            '',
            settings.EMAIL_HOST_USER,
            [mail],
        )
    elif tipo == 1:
        email= EmailMultiAlternatives(
            'UNIFORMES - Confirmar pedido y envios',
            '',
            settings.EMAIL_HOST_USER,
            [mail],
        )
    elif tipo == 2:
        email= EmailMultiAlternatives(
            'UNIFORMES - Confirmar entrega',
            '',
            settings.EMAIL_HOST_USER,
            [mail],
        )
    elif tipo == 3:
        email= EmailMultiAlternatives(
            '(RECORDATORIO) UNIFORMES - Confirmar Sexo y Talla',
            '',
            settings.EMAIL_HOST_USER,
            [mail],
        )
    elif tipo == 4:
        email= EmailMultiAlternatives(
            '(RECORDATORIO) UNIFORMES - Confirmar entrega',
            '',
            settings.EMAIL_HOST_USER,
            [mail],
        )
    

    email.attach_alternative(content,'text/html')
    return email  

def actualizar_Talla(Sexo,Talla,registros):
    cont=0
    hoy = datetime.datetime.now()
    for registro in registros:
        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(sexo=Sexo[cont])
        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(talla=Talla[cont])
        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(estado="PEDIDO")
        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(fechaconfirmacion=hoy.date())
        cont += 1

def actualizar_Entrega(Llego,registros,Aclaraciones):
    cont=0
    hoy = datetime.datetime.now()
    for registro in registros:
        if(Llego[cont]=="true"):
            RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(estado="ENTREGADO")
        else:
            RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(estado="ACLARACION")
        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(descripcion=Aclaraciones[cont])
        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(fechaentrega=hoy.date())
        cont += 1

def actualizar_numero_envio(clvcont,numero_envio,nopersonas):
    hoy = datetime.datetime.now()
    connection = get_connection()
    cont = 0
    limit = 50
    clvcontable = []
    registros = []
    connection.open()
    for clave,numero,nopersona in zip(clvcont,numero_envio,nopersonas):
        validar_numero = numero.translate({ord(c): None for c in string.whitespace})
        print(validar_numero)
        if cont <= limit and validar_numero:
            RegistroUniformes.objects.filter(clvcontable = clave, estado = "PEDIDO", nopersona=nopersona).update(fechapedido = hoy.date(), noseguimiento = numero, estado = "ENVIO")
            registros.append(RegistroUniformes.objects.filter(clvcontable = clave, nopersona=nopersona))
            if(clave not in clvcontable):
                clvcontable.append(clave)               
                cont += 1
    
    clvcontable.clear()
    cont = 0
    for registro in registros:
        print(registro[0].clvcontable)
        if(registro[0].clvcontable not in clvcontable):
            clvcontable.append(registro[0].clvcontable)               
            personas = RegistroUniformes.objects.filter(clvcontable = registro[0].clvcontable, estado = "ENVIO")
            mail='financieraprueba123@gmail.com'
            link=f'localhost:8000/confirmar_entrega/{registro[0].clvcontable}'
            context = {
                'registros':personas,
                'link':link
            }
            template = get_template('correo_confirmar.html')
            content = template.render(context)
            mensajes = send_email(mail,content,2)
            try:
                mensajes.send()
                print(f"se envio correo a {personas[0].correo}")
            except:
                print(f"NO se pudo enviar correo a {personas[0].correo}")
            cont += 1
    connection.close()
    print (f"se enviaron {cont} correos.")
        

def verificar_estado():
    registros = RegistroUniformes.objects.exclude(estado='CANCELADO')
    registros = registros.exclude(estado="ENTREGADO")
    registros = registros.exclude(estado="ERROR")
    for registro in registros:
        estado1 = PlantillaFinanciera.objects.filter(nopersona = registro.nopersona)
        estado2 =  PlantillaApoyo.objects.filter(nopersona = registro.nopersona)
        if(estado1):
            if(estado1[0].estado == 'Baja' or estado1[0].estado == 'Inactivo'):
                if(registro.empresa == 'FISA'):
                    if(registro.estado == 'ENVIO'):
                        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(estado="CANCELADO", descripcion="SE DIO DE BAJA EN ENVIO (DEBE HACER DEVOLUCIÓN)")
                    else:
                        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(estado="CANCELADO", descripcion="SE DIO DE BAJA")

        if(estado2):    
            if(estado2[0].estado == 'Baja' or estado2[0].estado == 'Inactivo'):
                if(registro.empresa == 'AEF'):
                    if(registro.estado == 'ENVIO'):
                        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(estado="CANCELADO", descripcion="SE DIO DE BAJA EN ENVIO (DEBE HACER DEVOLUCIÓN)")
                    else:
                        RegistroUniformes.objects.filter(nopersona=registro.nopersona).update(estado="CANCELADO", descripcion="SE DIO DE BAJA")


#FUNCION EXTRALARGA (SE PUEDE MEJORAR)
@login_required(login_url='/login/')
def reporte_general(request):
    if(request.user.is_superuser):
        talla_XCH = 0
        talla_CH = 0
        talla_M = 0
        talla_G = 0
        talla_XG = 0
        talla_2XG = 0
        talla_3XG = 0
        talla_4XG = 0
        talla_5XG = 0
        talla_6XG = 0

        registros = RegistroUniformes.objects.exclude(estado='ERROR')
        registros = registros.exclude(estado='CANCELADO')

        #REGISTROS AL AÑO
        hoy = datetime.datetime.now()
        solicitud_Enero = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='01', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='01', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='01', tiposolicitud='NUEVO').count())
        solicitud_Febrero = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='02', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='02', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='02', tiposolicitud='NUEVO').count())
        solicitud_Marzo = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='03', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='03', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='03', tiposolicitud='NUEVO').count())
        solicitud_Abril = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='04', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='04', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='04', tiposolicitud='NUEVO').count())
        solicitud_Mayo = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='05', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='05', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='05', tiposolicitud='NUEVO').count())
        solicitud_Junio = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='06', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='06', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='06', tiposolicitud='NUEVO').count())
        solicitud_Julio = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='07', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='07', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='07', tiposolicitud='NUEVO').count())
        solicitud_Agosto = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='08', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='08', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='08', tiposolicitud='NUEVO').count())
        solicitud_Septiembre = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='09', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='09', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='09', tiposolicitud='NUEVO').count())
        solicitud_Octubre = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='10', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='10', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='10', tiposolicitud='NUEVO').count())
        solicitud_Noviembre = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='11', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='11', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='11', tiposolicitud='NUEVO').count())
        solicitud_Diciembre = (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='12', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='12', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechasolicitud__year=hoy.year, fechasolicitud__month='12', tiposolicitud='NUEVO').count())
        
        entregados_Enero = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='01', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='01', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='01', tiposolicitud='NUEVO').count())
        entregados_Febrero = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='02', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='02', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='02', tiposolicitud='NUEVO').count())
        entregados_Marzo = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='03', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='03', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='03', tiposolicitud='NUEVO').count())
        entregados_Abril = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='04', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='04', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='04', tiposolicitud='NUEVO').count())
        entregados_Mayo = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='05', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='05', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='05', tiposolicitud='NUEVO').count())
        entregados_Junio = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='06', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='06', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='06', tiposolicitud='NUEVO').count())
        entregados_Julio = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='07', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='07', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='07', tiposolicitud='NUEVO').count())
        entregados_Agosto = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='08', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='08', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='08', tiposolicitud='NUEVO').count())
        entregados_Septiembre = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='09', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='09', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='09', tiposolicitud='NUEVO').count())
        entregados_Octubre = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='10', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='10', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='10', tiposolicitud='NUEVO').count())
        entregados_Noviembre = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='11', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='11', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='11', tiposolicitud='NUEVO').count())
        entregados_Diciembre = (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='12', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='12', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(fechaentrega__year=hoy.year, fechaentrega__month='12', tiposolicitud='NUEVO').count())

        #CONTAR TALLAS GENERALES

        talla_XCH += (registros.filter(talla='XCH', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='XCH', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='XCH', tiposolicitud='NUEVO').count())

        talla_CH = (registros.filter(talla='CH', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='CH', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='CH', tiposolicitud='NUEVO').count())

        talla_M = (registros.filter(talla='M', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='M', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='M', tiposolicitud='NUEVO').count())

        talla_G = (registros.filter(talla='G', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='G', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='G', tiposolicitud='NUEVO').count())

        talla_XG = (registros.filter(talla='XG', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='XG', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='XG', tiposolicitud='NUEVO').count())

        talla_2XG = (registros.filter(talla='2XG', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='2XG', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='2XG', tiposolicitud='NUEVO').count())

        talla_3XG = (registros.filter(talla='3XG', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='3XG', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='3XG', tiposolicitud='NUEVO').count())

        talla_4XG = (registros.filter(talla='4XG', tiposolicitud='3MESES').count() * 3)
        + (registros.filter(talla='4XG', tiposolicitud='AÑO').count() * 3)
        + (registros.filter(talla='4XG', tiposolicitud='NUEVO').count())

        talla_5XG = (registros.filter(talla='5XG', tiposolicitud='3MESES').count()) * 3 
        + (registros.filter(talla='5XG', tiposolicitud='AÑO').count() * 3) 
        + (registros.filter(talla='5XG', tiposolicitud='NUEVO').count())

        talla_6XG = (registros.filter(talla='6XG', tiposolicitud='3MESES').count() * 3) 
        + (registros.filter(talla='6XG', tiposolicitud='AÑO').count() * 3) 
        + (registros.filter(talla='6XG', tiposolicitud='NUEVO').count())

        #CONTAR TALLAS MUJER
        registros_mujer = registros.filter(sexo='Mujer')
        talla_XCH_M = (registros_mujer.filter(talla='XCH', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='XCH', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='XCH', tiposolicitud='NUEVO').count())

        talla_CH_M = (registros_mujer.filter(talla='CH', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='CH', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='CH', tiposolicitud='NUEVO').count())

        talla_M_M = (registros_mujer.filter(talla='M', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='M', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='M', tiposolicitud='NUEVO').count())

        talla_G_M = (registros_mujer.filter(talla='G', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='G', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='G', tiposolicitud='NUEVO').count())

        talla_XG_M = (registros_mujer.filter(talla='XG', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='XG', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='XG', tiposolicitud='NUEVO').count())

        talla_2XG_M = (registros_mujer.filter(talla='2XG', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='2XG', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='2XG', tiposolicitud='NUEVO').count())

        talla_3XG_M = (registros_mujer.filter(talla='3XG', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='3XG', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='3XG', tiposolicitud='NUEVO').count())

        talla_4XG_M = (registros_mujer.filter(talla='4XG', tiposolicitud='3MESES').count() * 3)
        + (registros_mujer.filter(talla='4XG', tiposolicitud='AÑO').count() * 3)
        + (registros_mujer.filter(talla='4XG', tiposolicitud='NUEVO').count())

        talla_5XG_M = (registros_mujer.filter(talla='5XG', tiposolicitud='3MESES').count()) * 3 
        + (registros_mujer.filter(talla='5XG', tiposolicitud='AÑO').count() * 3) 
        + (registros_mujer.filter(talla='5XG', tiposolicitud='NUEVO').count())

        talla_6XG_M = (registros_mujer.filter(talla='6XG', tiposolicitud='3MESES').count() * 3) 
        + (registros_mujer.filter(talla='6XG', tiposolicitud='AÑO').count() * 3) 
        + (registros_mujer.filter(talla='6XG', tiposolicitud='NUEVO').count())

        #CONTAR TALLAS HOMBRE
        registros_hombre = registros.filter(sexo='Hombre')
        talla_XCH_H = (registros_hombre.filter(talla='XCH', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='XCH', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='XCH', tiposolicitud='NUEVO').count())

        talla_CH_H = (registros_hombre.filter(talla='CH', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='CH', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='CH', tiposolicitud='NUEVO').count())

        talla_M_H = (registros_hombre.filter(talla='M', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='M', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='M', tiposolicitud='NUEVO').count())

        talla_G_H = (registros_hombre.filter(talla='G', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='G', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='G', tiposolicitud='NUEVO').count())

        talla_XG_H = (registros_hombre.filter(talla='XG', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='XG', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='XG', tiposolicitud='NUEVO').count())

        talla_2XG_H = (registros_hombre.filter(talla='2XG', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='2XG', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='2XG', tiposolicitud='NUEVO').count())

        talla_3XG_H = (registros_hombre.filter(talla='3XG', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='3XG', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='3XG', tiposolicitud='NUEVO').count())

        talla_4XG_H = (registros_hombre.filter(talla='4XG', tiposolicitud='3MESES').count() * 3)
        + (registros_hombre.filter(talla='4XG', tiposolicitud='AÑO').count() * 3)
        + (registros_hombre.filter(talla='4XG', tiposolicitud='NUEVO').count())

        talla_5XG_H = (registros_hombre.filter(talla='5XG', tiposolicitud='3MESES').count()) * 3 
        + (registros_hombre.filter(talla='5XG', tiposolicitud='AÑO').count() * 3) 
        + (registros_hombre.filter(talla='5XG', tiposolicitud='NUEVO').count())

        talla_6XG_H = (registros_hombre.filter(talla='6XG', tiposolicitud='3MESES').count() * 3) 
        + (registros_hombre.filter(talla='6XG', tiposolicitud='AÑO').count() * 3) 
        + (registros_hombre.filter(talla='6XG', tiposolicitud='NUEVO').count())

        hombre = registros.filter(sexo='Hombre').count()
        mujer = registros.filter(sexo='Mujer').count()

        Solicitudes = RegistroUniformes.objects.filter(estado="SOLICITUD").count()
        Entregados = RegistroUniformes.objects.filter(estado="ENTREGADO").count()
        Aclaraciones = RegistroUniformes.objects.filter(estado="ACLARACION").count()
        Cancelados = RegistroUniformes.objects.filter(estado="CANCELADO").count()
        context={
        'Registros':registros,
        'Solicitudes':Solicitudes,
        'Entregados':Entregados,
        'Aclaraciones':Aclaraciones,
        'solicitud_Enero':solicitud_Enero,
        'solicitud_Febrero':solicitud_Febrero,
        'solicitud_Marzo':solicitud_Marzo,
        'solicitud_Abril':solicitud_Abril,
        'solicitud_Mayo':solicitud_Mayo,
        'solicitud_Junio':solicitud_Junio,
        'solicitud_Julio':solicitud_Julio,
        'solicitud_Agosto':solicitud_Agosto,
        'solicitud_Septiembre':solicitud_Septiembre,
        'solicitud_Octubre':solicitud_Octubre,
        'solicitud_Noviembre':solicitud_Noviembre,
        'solicitud_Diciembre':solicitud_Diciembre,
        'entregados_Enero':entregados_Enero,
        'entregados_Febrero':entregados_Febrero,
        'entregados_Marzo':entregados_Marzo,
        'entregados_Abril':entregados_Abril,
        'entregados_Mayo':entregados_Mayo,
        'entregados_Junio':entregados_Junio,
        'entregados_Julio':entregados_Julio,
        'entregados_Agosto':entregados_Agosto,
        'entregados_Septiembre':entregados_Septiembre,
        'entregados_Octubre':entregados_Octubre,
        'entregados_Noviembre':entregados_Noviembre,
        'entregados_Diciembre':entregados_Diciembre,
        'Cancelados':Cancelados,
        'Talla_XCH':talla_XCH,
        'Talla_CH':talla_CH,
        'Talla_M':talla_M,
        'Talla_G':talla_G,
        'Talla_XG':talla_XG,
        'Talla_2XG':talla_2XG,
        'Talla_3XG':talla_3XG,
        'Talla_4XG':talla_4XG,
        'Talla_5XG':talla_5XG,
        'Talla_6XG':talla_6XG,

        'Talla_XCH_M':talla_XCH_M,
        'Talla_CH_M':talla_CH_M,
        'Talla_M_M':talla_M_M,
        'Talla_G_M':talla_G_M,
        'Talla_XG_M':talla_XG_M,
        'Talla_2XG_M':talla_2XG_M,
        'Talla_3XG_M':talla_3XG_M,
        'Talla_4XG_M':talla_4XG_M,
        'Talla_5XG_M':talla_5XG_M,
        'Talla_6XG_M':talla_6XG_M,

        'Talla_XCH_H':talla_XCH_H,
        'Talla_CH_H':talla_CH_H,
        'Talla_M_H':talla_M_H,
        'Talla_G_H':talla_G_H,
        'Talla_XG_H':talla_XG_H,
        'Talla_2XG_H':talla_2XG_H,
        'Talla_3XG_H':talla_3XG_H,
        'Talla_4XG_H':talla_4XG_H,
        'Talla_5XG_H':talla_5XG_H,
        'Talla_6XG_H':talla_6XG_H,
        'Hombre':hombre,
        'Mujer':mujer,

        'title':'Reporte General'
        }
        return render(request,"reporte_general.html", context)
    else:
        return HttpResponse("<html><h1>Acceso Denegado</h1></html>")