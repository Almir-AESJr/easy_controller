from django.urls import path
import sys



sys.path.insert(0, './paginas/controller/')

from chamadamatriz import *
from chamadas import *
from chamadas2 import *
from .views import IndexView
from .views import LoginView
from .views import ModeloView
from .views import EscolhaView
from .views import Modelo2View
urlpatterns = [
    path('inicio/',IndexView.as_view(),name= 'index'),
    path('login/',LoginView.as_view(),name= 'login'),
    path('modelo/',ModeloView.as_view(),name= 'modelo'),
    path('escolha/',EscolhaView.as_view(),name= 'escolha'),
    path('modelo2/',Modelo2View.as_view(),name= 'modelo2'),
    path('modelo2/chamadamatriz/dadosmatriz', dadosmatriz, name='dados-matriz'),
    path('modelo/chamadas/dadosgrafico', dadosgrafico, name='dados-grafico'),
    path('modelo/chamadas2/dadosgrafico2', dadosgrafico2, name='dados-grafico2')
]
