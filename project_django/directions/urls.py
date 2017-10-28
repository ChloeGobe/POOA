from django.conf.urls import url
from django.views.generic import TemplateView
from directions import views

urlpatterns = [
url(r'^welcome', views.index, name='index'),
url(r'^index', TemplateView.as_view(template_name="index.html")),
url(r'^results',  views.results, name='results'),

]
