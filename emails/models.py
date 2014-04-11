#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import os
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from zipreader import fileiterator
import re
from bs4 import BeautifulSoup

class Email(models.Model):
    email = models.EmailField()
    nombre = models.CharField(max_length=200, null=True,blank=True)
    apellido = models.CharField(max_length=200, null=True,blank=True)
    apellido2 = models.CharField(max_length=200, null=True,blank=True)
    telefono = models.CharField(max_length=200, null=True,blank=True)
    rut = models.CharField(max_length=200, null=True,blank=True)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    direccion = models.CharField(max_length=200,null=True,blank=True)
    comuna = models.CharField(max_length=200,null=True,blank=True)
    
    
    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'


class EmailTemplate(models.Model):
    nombre = models.CharField(max_length=200,null=True,blank=True)
    zipFile = models.FileField(upload_to=os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates') + '/adjuntos/')
    subject = models.CharField(max_length=200,null=True,blank=True)
    from_email = models.CharField(max_length=200,null=True,blank=True)
    
    @property
    def urlZipFile (self):
        if self.zipFile and hasattr(self.zipFile, 'url'):
            u = 'ADJUNTOS/' + os.path.basename(self.zipFile.url)
        else:
            u =''
        return u


    def save(self, *args, **kwargs):
        super(EmailTemplate, self).save(*args, **kwargs)
        self.uncompress()
    
    
    def uncompress(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates') + '/adjuntos/'
        zipfilename = path + os.path.basename(self.zipFile.url)
        path = path +'/zipfile/'+ os.path.basename(self.zipFile.url) + '/'
        os.makedirs(path)
        for filename,content in fileiterator(zipfilename):
            try:
                f= open(path + filename,'w')
                f.write(content)
                f.close()
            except:
                os.makedirs(path + filename)
                
        
    @property
    def attachedFiles(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates') + '/adjuntos/'
        zipfilename = path + os.path.basename(self.zipFile.url)
        pathfile = path +'/zipfile/'+ os.path.basename(self.zipFile.url) + '/'
        return [pathfile + filename for (filename,content) in fileiterator(zipfilename)]
        
    @property    
    def htmlContentOuter(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates') + '/adjuntos/'
        zipfilename = path + os.path.basename(self.zipFile.url)
        path = path +'/zipfile/'+ os.path.basename(self.zipFile.url) + '/'
        f= open(path + 'index.html','r')
        html_content = f.read()
        return html_content
    
    @property
    def htmlContent(self):
        soup = BeautifulSoup(self.htmlContentOuter)
        images = soup.body.find_all('img')
        for i in range (0,images.__len__()-1):
            if not images[i]['src'].startswith('cid:'):
                images[i]['src']= 'cid:%s' % os.path.basename(images[i]['src'])
        html_content = soup.body.decode_contents(formatter='html')
        return html_content

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Plantilla de Email'
        verbose_name_plural = 'Plantillas de Email'
        
        
class Delivery(models.Model):
    fecha = models.DateTimeField()
    plantilla = models.ForeignKey(EmailTemplate)

    def __unicode__(self):
        return '%s %s' % (str(self.fecha), self.plantilla.nombre)

    def save(self, *args, **kwargs):
        super(Delivery, self).save(*args, **kwargs)
        emails  = Email.objects.all()
        for email in emails:
            dq = DeliveryQueue(email=email)
            self.deliveryqueue_set.add(dq)

    class Meta:
        verbose_name = u'Envío Programado'
        verbose_name_plural = u'Envíos Programados'

class DeliveryQueue(models.Model):
    delivery = models.ForeignKey(Delivery)
    email = models.ForeignKey(Email)
    enviado = models.NullBooleanField(editable=False,null=True,blank=True)
    
    def __unicode__(self):
        return '%s %s' % (unicode(self.delivery),unicode(self.email))
    
    @property
    def htmlContent(self):
        return self.delivery.plantilla.htmlContent
    
    @property
    def plainContent(self):
        html_content = self.htmlContent
        try:
            text_content = re.sub(r'(<!--.*?-->|<[^>]*>)', '', html_content.replace('<br>', '\n').replace('<BR>', '\n').replace('<br/>', '\n'.replace('<BR/>', '\n')))
        except:
            text_content = 'No se puede obtener el contenido del mensaje'
        return text_content
    
    @property
    def from_email(self):
        return self.delivery.plantilla.from_email if not self.delivery.plantilla.from_email is None else 'admin@quickmail.cl'
    
    @property
    def subject(self):
        return self.delivery.plantilla.subject if not self.delivery.plantilla.subject is None else '[QuickMail] Email Message'
    
    @property
    def attachedFiles(self):
        return self.delivery.plantilla.attachedFiles
    
    class Meta:
        verbose_name = u'Cola de Envío'
        verbose_name_plural = u'Cola de Envíos'

