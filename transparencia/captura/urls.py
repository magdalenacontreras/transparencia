from django.conf.urls import url
from .  import views

urlpatterns = [
	url(r'^login',views.login_user ,name='login-user-1'),
	url(r'^login/$',views.login_user ,name='login-user'),
	url(r'^logout',views.logout_user ,name='logout-user-1'),
	url(r'^logout/$',views.logout_user ,name='logout-user'),
	url(r'^nuevo/$',views.nuevo ,name='nuevo'),
	url(r'^leyes/$',views.laws ,name='leyes'),
	url(r'^vinculos/$',views.links ,name='vinculos'),
	url(r'^buscar/$',views.search ,name='busqueda'),
	url(r'^busqueda/(?P<pk>[0-9]+)/$',views.search_public ,name='busqueda-publica'),
	url(r'^bloque/$',views.bloque ,name='bloque'),

	url(r'^desglose/(?P<pk>[0-9]+)/$',views.tree ,name='desglose'),
	url(r'^articulo/html/(?P<pk>[0-9]+)/$',views.articulo_html ,name='articulo_html'),
	url(r'^vinculo/html/(?P<pk>[0-9]+)/$',views.vinculo_html ,name='vinculo_html'),
	url(r'^sincronizar/(?P<pk>[0-9]+)$',views.sync ,name='sincronizar'),
	url(r'^indexar/', views.reindex, name='indexar'),
	url(r'^archivos/', views.archivos, name='archivos-subir'),
	url(r'^rarchivos/', views.rarchivos, name='archivos-subir'),
	url(r'^',views.home ,name='inicio'),
]

