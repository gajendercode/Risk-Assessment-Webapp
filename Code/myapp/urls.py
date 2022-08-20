from django.urls import path,include
from .import views
urlpatterns=[
    path('', views.index, name='index'),
	path('Home', views.home, name='home'),
	path('Team', views.team, name='team'),
    path('Assets', views.assets, name='assets'),
    path('',views.index,name='index'),
    path('Vulnerabilities',views.vulnerabilities,name='vulnerabilities'),
    path('show_vul_list',views.show_vul_list,name='show_vul_list'),
    path('threats',views.threats,name='threats'),
    path('Threats_input',views.Threats_input,name='Threats_input'),
    path('tableForm',views.tableForm,name='tableForm'),
    path('consequence_matrix',views.consequence_matrix,name='consequence_matrix'),
    
]