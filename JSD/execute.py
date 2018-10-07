'''
Created on 29.9.2018

@author: Jovana
'''

from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
import pydot, os


class Proba(object):
    def __init__(self):
        self.query_set = []

    def interpreter(self, model):

        return self.query_set


def execute(path, grammar_file_name, example_file_name, export_dot, export_png):
    '''U svrhe brzeg testiranja, metoda koja prima putanju do foldera, naziv fajla gde je gramatika i naziv fajla gde je
        primer programa u nasem jeziku i indikator da li da se eksportuju .dot i .png fajlovi'''

    meta_path = os.path.join(path, grammar_file_name)
    meta_name = os.path.splitext(meta_path)[0]
    metamodel = metamodel_from_file(meta_path)

    if export_dot:
        metamodel_export(metamodel, meta_name + '.dot')
        if export_png:
            graph = pydot.graph_from_dot_file(meta_name + '.dot')
            #graph[0].write_png(meta_name + '.png')

    model_path = os.path.join(path, example_file_name)
    model_name = os.path.splitext(model_path)[0]

    model = metamodel.model_from_file(model_path)

    if export_dot:
        model_export(model, model_name + '.dot')
    if export_png:
        graph = pydot.graph_from_dot_file(model_name + '.dot')
        #graph[0].write_png(model_name + '.png')

    #print(model.models[0].elements[0].datatype.charfield.parameters[0].max_length.number)
    '''proba = Proba()
    query_set = []
    query_set = proba.interpreter(model)'''

    print('ICF')
    print(model.models[0].name)

    models = model.models
    models1 = []
    for model in models:
        # pageElements = page.pageElements
        dict = {}
        dict['model'] = model.name
        # dict['pageElements'] = pageElements
        print(dict)
        models1.append(dict)

    print(models1)

    # Kreiranje generated deirektorojuma
    newpath = r'E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    #Generator koda za initial.py

    def test(models):
        string = 'from __future__ import unicode_literals\nfrom django.db import migrations, models\nimport django.db.models.deletion\nimport django.utils.timezone\n\n\nclass Migration(migrations.Migration):\n\n\tinitial = True\n\n\tdependencies = [\n\t]\n\n\toperations = ['
        for model in models:
            string += '\n\t\t'
            string += 'migrations.CreateModel('
            string += '\n\t\t\tname=' + "'" + str(model['model']) + "',"
            string += '),'
        string += '\n\t]'
        return string

    with open('E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/initial.py', 'w') as f:
        a = test(models1)
        f.write(a)

    # Generator koda za models.py
    def test1(models):
        string = 'import os\nfrom django.db import models\nfrom django.utils import timezone'
        for model in models:
            string += '\n\nclass '
            string += str(model['model']) + "(" + 'models.Model' + "):"

            string += '\n\n\t'
        return string

    with open('E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/models.py', 'w') as f:
        a = test1(models1)
        f.write(a)

    # Generator koda za views.py
    def test2(models):
        string = 'from django.views import generic\nfrom django.views.generic.edit import CreateView, UpdateView, DeleteView\nfrom django.urls import reverse_lazy, reverse\n'
        for model in models:
            string += '\n'
            string += 'from .models import ' + str(model['model'])
        for model in models:
            # CreateView generator
            string += '\n\n'
            string += '#Create view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'CreateView' + '(CreateView):'
            string += '\n\ttemplate_name=' + "'" + '.html' + "'"
            string += '\n\tmodel=' + str(model['model'])

            # DeleteView generator
            string += '\n\n'
            string += '#Delete view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'DeleteView' + '(DeleteView):'
            string += '\n\ttemplate_name=' + "'" + '.html' + "'"
            string += '\n\tmodel=' + str(model['model'])
            string += '\n\tsuccess_url=reverse_lazy(' + "'" + "'" + ")"

            # ListView generator
            string += '\n\n'
            string += '#List view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'ListView' + '(generic.ListView):'
            string += '\n\ttemplate_name=' + "'" + '.html' + "'"
            string += '\n\tcontext_object_name=' + "'" + 'all_' + str(model['model']) + "'"
            string += '\n\tdef get_queryset(self):'
            string += '\n\t\treturn ' + str(model['model']) + '.object.all'

        return string

    with open('E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/views.py', 'w') as f:
        a = test2(models1)
        f.write(a)

    # Generator koda za urls.py u okviru aplikacije
    def test3(models):
        string = 'from django.conf.urls import url\nfrom . import views\n'
        string += '\n' + 'app_name = ' + "'" + 'myapp' + "'"
        string += '\n\nurlspaterns = [' + '\n\n' + ']'

        return string

    with open('E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/urls.py', 'w') as f:
        a = test3(models1)
        f.write(a)

    # Generator koda za admin.py
    def test4(models):
        string = 'from django.contrib import admin\nfrom .models import '
        last = len(models) - 1
        for i, model in enumerate(models):
            string += str(model['model'])
            if i == last:
                string += '' + '\n'
            else:
                string += ', '
        for model in models:
            string += '\n'
            string += 'admin.site.register(' + str(model['model']) + ')'

        return string

    with open('E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/admin.py', 'w') as f:
        a = test4(models1)
        f.write(a)

    def test5(models):
        string = '"""prject URL Configuration\n\n'
        string += 'The `urlpatterns` list routes URLs to views. For more information please see:\n\t'
        string += 'The `urlpatterns` list routes URLs to views. For more information please see:\n'
        string += 'Examples:\n'
        string += 'Function views\n\t'
        string += '1. Add an import:  from my_app import views\n\t'
        string += '2. Add a URL to urlpatterns:  url(r' + "'" + '^$' + "'" +', views.home, name=' + "'" + 'home' + "'" + ')\n'
        string += 'Class-based views\n\t'
        string += '1. Add an import:  from other_app.views import Home\n\t'
        string += '2. Add a URL to urlpatterns:  url(r' + "'" + '^$' + "'" + ', Home.as_view(), name=' + "'" + 'home' + "'" + ')\n'
        string += 'Including another URLconf\n\t'
        string += '1. Import the include() function: from django.conf.urls import url, include\n\t'
        string += '2. Add a URL to urlpatterns:  url(r' + "'" '^blog/' + "'" + ', include(' + "'" + 'blog.urls' + "'" + '))\n'
        string += '"""\n'
        string += 'from django.conf.urls import include, url\n'
        string += 'from django.contrib import admin\n\n'
        string += 'urlpatterns = [\n\t'
        string += 'url(r' + "'" + '^admin/' + "', " + 'admin.site.urls),\n\t'
        string += 'url(r' + "'" + '^myapp/' + "', " + 'include(' + "'myapp.urls'" + ')),\n'
        string += ']'

        return string


    with open('E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/urls.py', 'w') as f:
        a = test5(models1)
        f.write(a)

