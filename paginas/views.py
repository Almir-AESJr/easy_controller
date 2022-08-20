from django.views.generic import TemplateView
from django.http import JsonResponse
import json

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
class LoginView(TemplateView):
    template_name = "login.html"
class ModeloView(TemplateView):
    template_name = "modelo.html"
class EscolhaView(TemplateView):
    template_name = "escolha.html"
class Modelo2View(TemplateView):
    template_name = "modelo2.html"