#from os import write
#import smtplib
#import config
import datetime
from os import error
import dateutil
import numpy as np
from openpyxl import load_workbook
import pandas as pd
import pymysql
from sqlalchemy import create_engine

"""def enviar_correo(mensaje, correo): 
    server = smtplib.SMTP('smtp.gmail.com',587)
    try:
        server.starttls()
        server.login(config.fromaddr, config.password)
        server.sendmail(config.fromaddr,correo,mensaje)
    finally:
        server.quit()"""

def run_bot_uniformes():
    db = pymysql.connect(host='localhost',
            user='root',
            password='',
            db='proyecto1',
            charset='utf8mb4')
    pd.options.mode.chained_assignment = None  # default='warn'
    cursor = db.cursor()
    Errores = ""
    Log=""
    

    cursor.execute('SELECT NOPERSONA,NOMBRE,NOSUCURSAL,NOMBRESUCURSAL,CLVCONTABLE,FECHAINGRESO FROM plantilla_financiera WHERE ESTADO="Activo"')
    pFISA = pd.DataFrame(cursor.fetchall(),columns=['NOPERSONA','NOMBRE','NOSUCURSAL','NOMBRESUCURSAL','CLVCONTABLE','FECHAINGRESO'])

    cursor.execute('SELECT NOPERSONA,NOMBRE,NOSUCURSAL,NOMBRESUCURSAL,CLVCONTABLE,FECHAINGRESO FROM plantilla_apoyo WHERE ESTADO="Activo"')
    pAEF = pd.DataFrame(cursor.fetchall(),columns=['NOPERSONA','NOMBRE','NOSUCURSAL','NOMBRESUCURSAL','CLVCONTABLE','FECHAINGRESO'])

    pFISA['FECHAINGRESO'] = pd.to_datetime(pFISA['FECHAINGRESO'], format='%d/%m/%Y')

    hoy = datetime.datetime.now()

    #CREAR REGISTRO PARA FISA
    nuevosFISA = pFISA.loc[(pFISA['FECHAINGRESO'] < hoy) & (pFISA['FECHAINGRESO'] > (hoy + dateutil.relativedelta.relativedelta(days=-14)) ) ]
    meses3FISA =  pFISA.loc[(pFISA['FECHAINGRESO']  > hoy + dateutil.relativedelta.relativedelta(months=-3)) & (pFISA['FECHAINGRESO'] < hoy + dateutil.relativedelta.relativedelta(months=-3,days=14))]
    anioFISA = pFISA.loc[(pFISA['FECHAINGRESO']  > hoy + dateutil.relativedelta.relativedelta(years=-1)) & (pFISA['FECHAINGRESO'] < hoy + dateutil.relativedelta.relativedelta(years=-1,days=14))]

    nuevosFISA.insert(0,'TIPOSOLICITUD','NUEVO')
    meses3FISA.insert(0,'TIPOSOLICITUD','3MESES')
    anioFISA.insert(0,'TIPOSOLICITUD','AÑO')

    RegistroFISA = pd.concat([nuevosFISA,meses3FISA,anioFISA])
    RegistroFISA.insert(0,'EMPRESA','FISA')
    RegistroFISA.insert(2,'FECHASOLICITUD',hoy.date())
    RegistroFISA.insert(9,'CORREO', np.nan)
    RegistroFISA.insert(10,'CORREO_ENVIADO', 0)
    RegistroFISA.insert(11,'FECHACONFIRMACION', np.nan)
    RegistroFISA.insert(12,'FECHAPEDIDO', np.nan)
    RegistroFISA.insert(13,'NOSEGUIMIENTO', np.nan)
    RegistroFISA.insert(14,'FECHAENTREGA', np.nan)
    RegistroFISA.insert(15,'DESCRIPCION', np.nan)
    RegistroFISA.insert(16,'ESTADO', 'SOLICITUD')
    for index,persona in RegistroFISA.iterrows():
        rows = cursor.execute('SELECT * FROM sucursalesfisa WHERE Numero_Sucursal IN ( SELECT NOSUCURSAL FROM plantilla_financiera WHERE NOPERSONA = %s )',persona[3])
        correoFISA = cursor.fetchall()
        if rows > 0:
            if (correoFISA[0][3] != None):
                RegistroFISA.CORREO[index] = correoFISA[0][3]
            elif (correoFISA[0][4] != None):
                RegistroFISA.CORREO[index] = correoFISA[0][4]
            elif (correoFISA[0][5] != None):
                RegistroFISA.CORREO[index] = correoFISA[0][5]
            elif (correoFISA[0][6] != None):
                RegistroFISA.CORREO[index] = correoFISA[0][6]
            else:
                RegistroFISA.ESTADO[index] = 'ERROR'
                RegistroFISA.FECHASOLICITUD[index] = np.nan
                Log = "NO TIENE CORREO DONDE ENVIAR"
                RegistroFISA.DESCRIPCION[index] = Log
                print(f'PEDIDO CANCELADO DE { RegistroFISA.NOMBRE[index]} NO TIENE CORREO DONDE ENVIAR')
        else:
            RegistroFISA.ESTADO[index] = 'ERROR'
            RegistroFISA.FECHASOLICITUD[index] = np.nan
            Log = "NO EXISTE LA SUCURSAL EN LA TABLA sucursalesfisa"
            RegistroFISA.DESCRIPCION[index] = Log
            print(f'PEDIDO CANCELADO DE { RegistroFISA.NOMBRE[index]} NO EXISTE LA SUCURSAL EN LA TABLA sucursalesfisa')
        

    #CREAR REGISTRO PARA AEF
    pAEF['FECHAINGRESO'] = pd.to_datetime(pAEF['FECHAINGRESO'], format='%m/%d/%Y')

    nuevosAEF = pAEF.loc[(pAEF['FECHAINGRESO'] < hoy) & (pAEF['FECHAINGRESO'] > (hoy + dateutil.relativedelta.relativedelta(days=-14)) ) ]
    meses3AEF =  pAEF.loc[(pAEF['FECHAINGRESO']  > hoy + dateutil.relativedelta.relativedelta(months=-3)) & (pAEF['FECHAINGRESO'] < hoy + dateutil.relativedelta.relativedelta(months=-3,days=14))]
    anioAEF = pAEF.loc[(pAEF['FECHAINGRESO']  > hoy + dateutil.relativedelta.relativedelta(years=-1)) & (pAEF['FECHAINGRESO'] < hoy + dateutil.relativedelta.relativedelta(years=-1,days=14))]

    nuevosAEF.insert(0,'TIPOSOLICITUD','NUEVO')
    meses3AEF.insert(0,'TIPOSOLICITUD','3MESES')
    anioAEF.insert(0,'TIPOSOLICITUD','AÑO')

    RegistroAEF = pd.concat([nuevosAEF,meses3AEF,anioAEF])
    RegistroAEF.insert(0,'EMPRESA','AEF')
    RegistroAEF.insert(2,'FECHASOLICITUD',hoy.date())
    RegistroAEF.insert(9,'CORREO', np.nan)
    RegistroAEF.insert(10,'CORREO_ENVIADO', 0)
    RegistroAEF.insert(11,'FECHACONFIRMACION', np.nan)
    RegistroAEF.insert(12,'FECHAPEDIDO', np.nan)
    RegistroAEF.insert(13,'NOSEGUIMIENTO', np.nan)
    RegistroAEF.insert(14,'FECHAENTREGA', np.nan)
    RegistroAEF.insert(15,'DESCRIPCION', np.nan)
    RegistroAEF.insert(16,'ESTADO', 'SOLICITUD')

    for index,persona in RegistroAEF.iterrows():
        rows = cursor.execute('SELECT * FROM sucursalesaef WHERE Num_Sucursal IN ( SELECT Num_Sucursal FROM traductor_aef WHERE Clave_contable IN ( SELECT CLVCONTABLE FROM plantilla_apoyo WHERE NOPERSONA = %s ) )',persona[3])
        correoAEF = cursor.fetchall()
        if rows > 0:
            if (correoAEF[0][5] != np.nan):
                RegistroAEF.CORREO[index] = correoAEF[0][5]
            elif (correoAEF[0][4] != np.nan):
                RegistroAEF.CORREO[index] = correoAEF[0][4]
            elif (correoAEF[0][3] != np.nan):
                RegistroAEF.CORREO[index] = correoAEF[0][3]
            else:
                RegistroAEF.ESTADO[index] = 'ERROR'
                RegistroAEF.FECHASOLICITUD[index] = np.nan
                Log = "NO TIENE CORREO DONDE ENVIAR"
                RegistroAEF.DESCRIPCION[index] = Log
                print(f'PEDIDO CANCELADO DE { RegistroAEF.NOMBRE[index]} NO TIENE CORREO DONDE ENVIAR')
        else:
            RegistroAEF.ESTADO[index] = 'ERROR'
            RegistroAEF.FECHASOLICITUD[index] = np.nan
            Log = "NO EXISTE LA SUCURSAL EN LA TABLA sucursalesaef"
            RegistroAEF.DESCRIPCION[index] = Log
            print(f'PEDIDO CANCELADO DE { RegistroAEF.NOMBRE[index]} NO EXISTE LA SUCURSAL EN LA TABLA sucursalesaef')
        

    #RegistroAEF = RegistroAEF[RegistroAEF.ESTADO != 'CANCELADO']
    #print(RegistroAEF)

    Registro_uniformes = pd.concat([RegistroFISA,RegistroAEF])
    #print(Registro_uniformes)
    fecha = hoy + dateutil.relativedelta.relativedelta(days=-14)
    fecha = fecha.strftime("%m/%d/%Y")
    print("STRING DATE:  " + fecha)
    cursor.execute('SELECT NOPERSONA FROM registro_uniformes WHERE ESTADO="SOLICITUD" OR FECHASOLICITUD > %s ',fecha)
    registrodb = pd.DataFrame(cursor.fetchall(),columns=['NOPERSONA'])
    #print(registrodb)

    Registro_uniformes = Registro_uniformes[~Registro_uniformes["NOPERSONA"].isin(registrodb.NOPERSONA)]
    print("FILTRO PERSONAS")
    print(Registro_uniformes)


    engine = create_engine('mysql+pymysql://root:@localhost/proyecto1')
    dbConn = engine.connect()
    Registro_uniformes.to_sql('registro_uniformes', dbConn, if_exists='append', index=False)

    cancelados = Registro_uniformes.loc[Registro_uniformes['ESTADO'] == 'ERROR'].shape[0]
    solicitudes = Registro_uniformes.loc[Registro_uniformes['ESTADO'] == 'SOLICITUD'].shape[0]

    return cancelados,solicitudes
