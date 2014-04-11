# Create your views here.
from django.shortcuts import render_to_response
from .models import *
from simplejson.encoder import JSONEncoder
import simplejson
import urllib2
import urllib
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def GuardarMailView(request):
    fecha = request.POST['fecha_nacimiento'].split('/')
    email = request.POST['email']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    apellido2 = request.POST['apellido2']
    telefono = request.POST['telefono']
    rut = request.POST['rut']
    fecha_nacimiento = '%s-%s-%s' % (fecha[2],fecha[1],fecha[0] )
    direccion = request.POST['direccion']
    comuna = request.POST['comuna']
    categoria = request.POST['categoria']
    aporte = request.POST['aporte']
    aporteEspecifico = True if request.POST['aporteEspecifico']=='SI' else False
    deporte = request.POST['deporte']
    medioPago = request.POST['medioPago']
    recibirRetribucion = True if request.POST['recibirRetribucion']=='SI' else False
    
    em = Email(email=email,
               nombre=nombre,
               apellido=apellido,
               apellido2=apellido2,
               telefono=telefono,
               rut=rut,
               fecha_nacimiento=fecha_nacimiento,
               direccion=direccion,
               comuna=comuna,
               categoria=categoria,
               aporte=aporte,
               aporteEspecifico=aporteEspecifico,
               deporte=deporte,
               medioPago=medioPago,
               recibirRetribucion=recibirRetribucion
               )
    em.save()
    
    obj = {'respuesta':'OK'}

    callback= request.POST['callback']
    json = callback +  '(' + simplejson.dumps(obj) + ')'
    response = render_to_response('jsonList.html',{'json':json},content_type='application/json', mimetype='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
    