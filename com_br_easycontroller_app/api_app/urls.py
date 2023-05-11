from django.urls import path
from .views import EasyController
from .views import EasyControllerLqr
from .views import EasyControllerLqi
from .views import EasyControllerLqg
from .views import EasyControllerLqgi
from .views import Inicio
from .views import IndexView
from .views import CadastroView
from .views import SobreView
from .views import TutorialView
from .views import HomeView

urlpatterns = [
    path('inicio/', Inicio.as_view()),
    path('easy-controller/', EasyController.as_view()),
    path('easy-controller/lqr', EasyControllerLqr.as_view()),
    path('easy-controller/lqi', EasyControllerLqi.as_view()),
    path('easy-controller/lqg', EasyControllerLqg.as_view()),
    path('easy-controller/lqgi', EasyControllerLqgi.as_view()),
    path('home/', HomeView),
    path('index/', IndexView),
    path('cadastro/', CadastroView),
    path('sobre/', SobreView),
    path('tutorial/', TutorialView),
]
