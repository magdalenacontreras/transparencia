# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess

from django.db import models
from tinymce.models import HTMLField
from colorful.fields import RGBColorField
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.encoding import smart_text
from django.conf import settings

# Create your models here.

class NivelGobierno(models.Model):
    nombre = models.CharField(max_length=512)
    color = RGBColorField(null=True)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre


class Periodo(models.Model):
    nombre = models.CharField(max_length=512)
    color = RGBColorField(null=True)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre


class Ley(models.Model):
    nombre = models.CharField(max_length=512)
    descripcion = HTMLField()
    color = RGBColorField(null=True)
    anio = models.IntegerField()
    nivel = models.ForeignKey(NivelGobierno)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre

class Responsable(models.Model):
    nombre = models.CharField(max_length=512)
    unidad_administrativa = models.CharField(max_length=1024)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    mes = ((instance.actualizacion.month-1)/3)+1


    mes = "T"+str(mes) ##str(instance.actualizacion.month).zfill(2)
    art=str(instance.articulo).replace(" ","").replace("-","/").replace(".","").lower()

    return '{0}/{1}/{2}/{3}'.format(instance.anio,mes,art,filename)

class Articulo(models.Model):
    nombre = models.CharField(max_length=1024)
    titulo = models.CharField(max_length=1024, default="Marco legal aplicable")
    descripcion = HTMLField()



    ley = models.ForeignKey(Ley, related_name='articulos')
    articulo = models.ForeignKey('self', null=True, blank=True, related_name='fracciones')
    orden = models.IntegerField(default=1)
    responsable = models.ForeignKey(Responsable, null=True)
    def __str__(self):
        if self.articulo:
            return smart_text(self.articulo) + " - " + smart_text(self.nombre)
        return self.nombre

    def __unicode__(self):
        nmb = self.nombre
        if self.articulo:
            nmb = smart_text(self.articulo) + " - " + smart_text(self.nombre)
        return nmb

    def arbol(self):
        return Archivo.objects.raw("select max(id) as id from captura_archivo WHERE articulo_id=" + str(
            self.pk) + "  group by anio order  by anio desc")

    def anual(self):
        return Archivo.objects.raw("select max(id) as id from captura_archivo WHERE articulo_id=" + str(
            self.pk) + "  group by anio order by anio desc")

    class Meta:
        ordering = ('orden',)


class Archivo(models.Model):
    actualizacion = models.DateField(null=True, blank=True )
    inicio_actualizacion = models.DateField(null=True, blank=True )
    subida = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    validacion = models.DateField(null=True, blank=True)
    articulo = models.ForeignKey(Articulo, null=True, related_name='archivo')
    documento = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    #documento = models.FileField(upload_to='fs/%Y/%m', null=True, blank=True)
    anio = models.IntegerField(default=2019)
    trimestre = models.IntegerField(default=0)
    responsable = models.ForeignKey(Responsable, null=True)
    autor = models.ForeignKey(User, null=True, blank=True)
    html = HTMLField(default='')

    class Meta:
        ordering = ('-subida',)

    def __str__(self):
        return str(self.documento)  ##.encode('ascii', errors='replace')

    def __unicode__(self):
        return u"%s" % self.documento

    def extract(self):
        ext = smart_text(self.documento)
        filename =  settings.MEDIA_ROOT+smart_text(ext)
        name = ext.split('/')[-1].replace(".xlsx", '.html').\
                                  replace(".xls", '.html').\
                                  replace(".docx",'.html').\
                                  replace(".doc", '.html')

        if ext.endswith((".xls", ".xlsx", ".docx", ".doc")):
            try:
                cmd = settings.BASE_DIR + '/extract.sh %s %s' % (filename, name)
                result = subprocess.Popen((cmd))
                result.wait()

                with open("/tmp/mpt/%s_clean.html" % (name), 'r') as cnt:

                    self.html = cnt.read()
                    self.save()


            except Exception as e:
                print e



class Vinculo(models.Model):
    nombre = models.CharField(max_length=1024)
    descripcion = HTMLField()
    documento = models.FileField(upload_to='ls/%Y/%m/%d', null=True, blank=True)
    subida = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    autor = models.ForeignKey(User, null=True, blank=True)
    uuid=models.CharField(max_length=254,default="0000-00000-000000-000000")
    html = HTMLField(default="")

    class Meta:
        ordering = ('-subida',)
