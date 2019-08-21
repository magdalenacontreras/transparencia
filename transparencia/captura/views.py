# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_text
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import rotate_token
from django.contrib.auth import authenticate, login, logout
from django.db import connection, transaction
from django.core.paginator import Paginator
from captura.forms import ArchivoForm, VinculoForm
from captura.models import Ley, Articulo, Vinculo, Archivo
from django.db.models import Q
from django.conf import settings
import subprocess
import os.path
import os
import codecs

import paramiko


# Create your views here.

def login_user(request):
    logout(request)
    username = password = ''
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/nuevo/')
    return render(request, 'login.html', {})


@login_required(login_url='/login/')
def nuevo(request):
    form = None
    url = None
    if request.method == 'GET':
        form = ArchivoForm()
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():

            doc=form.save()
            doc.extract()
            print '******'
            url = doc
            form = ArchivoForm()
        else:
            return render(request, 'nuevo.html', {'form': form})

    return render(request, 'nuevo.html', {'form': form,'link':url})

@login_required(login_url='/login/')
def reindex(request):

    for ar in Archivo.objects.all():
        if ar.html is None or ar.html =="":
            ar.extract()
    return HttpResponseRedirect('/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/nuevo/")
    else:
        return HttpResponseRedirect("/login/")


@login_required(login_url='/login/')
def laws(request):
    return render(request, 'leyes.html', {'leyes': Ley.objects.all()})



def tree(request, pk):
    ley = Ley.objects.get(id=pk)
    rst = Articulo.objects.filter(ley__pk=pk, articulo=None)
    return render(request, 'desglose.html', {'ley': ley, 'articulos': rst})


def articulo_html(request, pk):

    return render(request,'html.html',{'archivo':Archivo.objects.get(pk=pk)})

def vinculo_html(request, pk):

    return render(request,'html.html',{'archivo':Vinculo.objects.get(pk=pk)})


@login_required(login_url='/login/')
def links(request):
    form = None
    link = None
    if request.method == 'GET':
        form = VinculoForm()
    if request.method == 'POST':
        form = VinculoForm(request.POST, request.FILES)
        if form.is_valid():
            result = form.save()
            link = str(result.documento)
            form = VinculoForm()
        else:
            return render(request, 'vinculos.html', {'form': form})

    return render(request, 'vinculos.html', {'form': form, 'link': link})
@login_required(login_url='/login/')
def bloque(request):
    return render(request, 'bloque.html', {})


@login_required(login_url='/login/')
def search(request):
    if request.method == 'GET':
        q = str(request.GET.get('q'))
        rst = Vinculo.objects.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
        leyes = Archivo.objects.filter(Q(html__icontains=q) | Q(articulo__nombre__icontains=q))
        return render(request, 'resultado.html', {'result': rst,'leyes':leyes})


def search_public(request,pk):
    if request.method == 'GET':
        q = smart_text(request.GET.get('q'))
        rst = Vinculo.objects.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
        leyes = Archivo.objects.filter(Q(html__icontains=q) | Q(articulo__nombre__icontains=q))

        ley = Ley.objects.get(id=pk)
        rst2 = Articulo.objects.filter(ley__pk=pk, articulo=None)
        return render(request, 'busqueda.html', {'result': rst,'leyes':leyes,'ley':ley,'articulos':rst2})


@login_required(login_url='/login/')
def sync(request, pk):
    ley = Ley.objects.get(id=pk)
    rst = Articulo.objects.filter(ley__pk=pk, articulo=None).order_by('orden')
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
    content = render_to_string('desglose_2.html', {'ley': ley, 'articulos': rst})
    filetmp = '/var/www/mcontreras.gob.mx/htdocs/transparencia_' + str(pk) + '.php'


    #call(["rm",
    #      "/var/www/mcontreras.gob.mx/htdocs/wp-content/cache/supercache/mcontreras.gob.mx/transparencia-2/index-https.html"])
    #with codecs.open(filetmp, "w", "utf-8") as static_file:
    #    static_file.write(content)
    #    print "escrito?"

    #	with pysftp.Connection('www2.df.gob.mx', username='cuauhnew', password='chiomiamor') as sftp:
    #		content =  render_to_string('desglose_2.html',{'ley':ley,'articulos':rst})
    #		filetmp = '/tmp/transparencia_'+str(pk)+'.php'
    #		with codecs.open(filetmp, "w", "utf-8") as static_file:
    #			static_file.write(content)
    #		with sftp.cd("/home/cuauhtemoc/htdocs_cuauhtemoc/"):
    #			sftp.put(filetmp)
    #	sftp.close()
    #        cmd =SITE_ROOT+"/../copia.sh"
    #        print call([cmd, ""])

    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('www2.df.gob.mx', username='cuauhnew', password='chiomiamor')
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/home/cuauhtemoc/tranparencia.sh")
    # print ssh_stdout
    # print "**",str(ssh_stderr)
    # ssh.close()
    return tree(request, pk)
@login_required(login_url='/login/')
def archivos(request):
    """
    Photo upload / dropzone handler
    :param request:
    :param uid: Optional picture UID when re-uploading a file.
    :return:
    """
    try:
        # for img in request.FILES:
        #pk=int(request.POST.get('requisito'))
        vinculo = Vinculo(documento=request.FILES['file'])
        vinculo.uuid = request.POST.get('uuid')
        vinculo.autor= request.user
        vinculo.save()

        return JsonResponse({"status":"added","uuid":vinculo.uuid,"url":"https://transparencia.mcontreras.gob.mx/media/"+str(vinculo.documento)})
    except Exception as e:
        print e
        return HttpResponse("File upload form not valid.", status=500)


@login_required(login_url='/login/')
def rarchivos(request):
    """
    Photo upload / dropzone handler
    :param request:
    :param uid: Optional picture UID when re-uploading a file.
    :return:
    """
    try:
        uuid = request.POST['uuid']
        Vinculo.objects.filter(uuid=uuid).delete()
        return HttpResponse("{'status':'removed','uuid':'"+uuid+"'}")
    except Exception as e:
        print e
        return HttpResponse("File removed form not valid.", status=500)
