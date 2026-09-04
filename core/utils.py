#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from django.utils import timezone

from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

def content_file_name(instance, filename):
    ext = filename.split('.')
    filename = "%s_%s.%s" % (instance.empresa.id, ext[0], ext[-1])
    return os.path.join('items', filename)


def content_file_name_ecommerce(instance, filename):
    ext = filename.split('.')
    filename = "%s_%s.%s" % (instance.empresa.id, ext[0], ext[-1])
    return os.path.join('ecommerce', filename)

def separador_de_miles(numero):
    numero=str(format(float(numero), '.3f'))
    vector=numero.split(".")
    s=vector[0]
    for i in range(len(vector[0]),0,-3):
        if i == 1 and s[0] == "-":
            s=s[:i]+s[i:]
        else:
            s=s[:i]+"."+s[i:]
    a=s[:len(s)-1]
    if len(vector) == 2:
        a+= ","+vector[1]
    return a

def separador_de_miles_entero(numero):
    numero=str(numero)
    vector=numero.split(".")
    s=vector[0]
    for i in range(len(vector[0]),0,-3):
        if i == 1 and s[0] == "-":
            s=s[:i]+s[i:]
        else:
            s=s[:i]+"."+s[i:]
    a=s[:len(s)-1]
    return a


# def numero_recibo(user, tipo=None):
#     if not tipo:
#         ultimo = Talonario.objects.get(cajero=user, tipo='FACTURA', activo=True)
#     else:
#         ultimo = Talonario.objects.get(cajero=user, tipo=tipo, activo=True)
#     if int(ultimo.ultimo) == ultimo.fin:
#         return "Sin Recibo fiscal disponible"
#     elif ultimo.vencimiento < timezone.now().date():
#         return "Timbrado del Recibo fiscal vencido"
#     else:
#         current = str(int(ultimo.ultimo)+1)
#         while len(str(current))<7:
#             current = "0"+str(current)
#     return [ultimo, ultimo.puntoExpedicion.sucursal.sucursal+'-'+ultimo.puntoExpedicion.puntoExpedicion+'-'+current]


__author__ = 'efrenfuentes'


MONEDA_SINGULAR = 'bolivar'
MONEDA_PLURAL = 'bolivares'

CENTIMOS_SINGULAR = 'centimo'
CENTIMOS_PLURAL = 'centimos'

MAX_NUMERO = 999999999999

UNIDADES = (
    'cero',
    'uno',
    'dos',
    'tres',
    'cuatro',
    'cinco',
    'seis',
    'siete',
    'ocho',
    'nueve'
)

DECENAS = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciseis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)

DIEZ_DIEZ = (
    'cero',
    'diez',
    'veinte',
    'treinta',
    'cuarenta',
    'cincuenta',
    'sesenta',
    'setenta',
    'ochenta',
    'noventa'
)

CIENTOS = (
    '_',
    'ciento',
    'doscientos',
    'trescientos',
    'cuatroscientos',
    'quinientos',
    'seiscientos',
    'setecientos',
    'ochocientos',
    'novecientos'
)

def numero_a_letras(numero):
    numero_entero = int(numero)
    if numero_entero > MAX_NUMERO:
        raise OverflowError('Número demasiado alto')
    if numero_entero < 0:
        return 'menos %s' % numero_a_letras(abs(numero))
    letras_decimal = ''
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    if parte_decimal > 9:
        letras_decimal = 'punto %s' % numero_a_letras(parte_decimal)
    elif parte_decimal > 0:
        letras_decimal = 'punto cero %s' % numero_a_letras(parte_decimal)
    if (numero_entero <= 99):
        resultado = leer_decenas(numero_entero)
    elif (numero_entero <= 999):
        resultado = leer_centenas(numero_entero)
    elif (numero_entero <= 999999):
        resultado = leer_miles(numero_entero)
    elif (numero_entero <= 999999999):
        resultado = leer_millones(numero_entero)
    else:
        resultado = leer_millardos(numero_entero)
    resultado = resultado.replace('uno mil', 'un mil')
    resultado = resultado.strip()
    resultado = resultado.replace(' _ ', ' ')
    resultado = resultado.replace('  ', ' ')
    if parte_decimal > 0:
        resultado = '%s %s' % (resultado, letras_decimal)
    return resultado

def numero_a_moneda(numero):
    numero_entero = int(numero)
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    centimos = ''
    if parte_decimal == 1:
        centimos = CENTIMOS_SINGULAR
    else:
        centimos = CENTIMOS_PLURAL
    moneda = ''
    if numero_entero == 1:
        moneda = MONEDA_SINGULAR
    else:
        moneda = MONEDA_PLURAL
    letras = numero_a_letras(numero_entero)
    letras = letras.replace('uno', 'un')
    letras_decimal = 'con %s %s' % (numero_a_letras(parte_decimal).replace('uno', 'un'), centimos)
    letras = '%s %s %s' % (letras, moneda, letras_decimal)
    return letras

def leer_decenas(numero):
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero == 20:
        resultado = 'veinte'
    elif numero <= 29:
        resultado = 'veinti%s' % UNIDADES[unidad]
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = '%s y %s' % (resultado, UNIDADES[unidad])
    return resultado

def leer_centenas(numero):
    centena, decena = divmod(numero, 100)
    if numero == 100:
        resultado = 'cien'
    else:
        resultado = CIENTOS[centena]
        if decena > 0:
            resultado = '%s %s' % (resultado, leer_decenas(decena))
    return resultado

def leer_miles(numero):
    millar, centena = divmod(numero, 1000)
    resultado = ''
    if (millar == 1):
        resultado = ''
    if (millar >= 2) and (millar <= 9):
        resultado = UNIDADES[millar]
    elif (millar >= 10) and (millar <= 99):
        resultado = leer_decenas(millar)
    elif (millar >= 100) and (millar <= 999):
        resultado = leer_centenas(millar)
    resultado = '%s mil' % resultado
    if centena > 0:
        resultado = '%s %s' % (resultado, leer_centenas(centena))
    return resultado

def leer_millones(numero):
    millon, millar = divmod(numero, 1000000)
    resultado = ''
    if (millon == 1):
        resultado = ' un millon '
    if (millon >= 2) and (millon <= 9):
        resultado = UNIDADES[millon]
    elif (millon >= 10) and (millon <= 99):
        resultado = leer_decenas(millon)
    elif (millon >= 100) and (millon <= 999):
        resultado = leer_centenas(millon)
    if millon > 1:
        resultado = '%s millones' % resultado
    if (millar > 0) and (millar <= 999):
        resultado = '%s %s' % (resultado, leer_centenas(millar))
    elif (millar >= 1000) and (millar <= 999999):
        resultado = '%s %s' % (resultado, leer_miles(millar))
    return resultado

def leer_millardos(numero):
    millardo, millon = divmod(numero, 1000000)
    return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))