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
        modelElements = model.modelElements
        dict = {}
        dict['model'] = model.name
        dict['modelElements'] = modelElements
        print(dict)
        models1.append(dict)

    print(models1)

    # Kreiranje generated deirektorojuma
    newpath = r'E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Funkcija kojoj se prosledjuje prvi i drugi parametar elementa
    # prosledjuje se i boolean indicator dateTimeField koji ukazuje na to da li je dateTime
    # (potrebno jer je defaultna vrednost razlicita u tom slucaju)
    # endElement je string kojim se zavrsava red, oznacava kraj elementa
    def getStringFor2Parameters(firstParameter, secondParameter, dateTimeField, endElement):
        string = ''

        # First parameter is max_length
        if firstParameter.max_length and secondParameter.null is not None:
            string += 'max_length=' + firstParameter.max_length.number + ", "
            string += 'null=' + secondParameter.null.booleanValue + endElement
        elif firstParameter.max_length and secondParameter.default is not None:
            string += 'max_length=' + firstParameter.max_length.number + ", "
            if not dateTimeField:
                string += 'default=' + secondParameter.default.defaultValue.number + endElement
            else:
                string += 'default=timezone.' + \
                          secondParameter.default.defaultValue.timezone.var + endElement

        # First parameter is null
        elif firstParameter.null and secondParameter.max_length is not None:
            string += 'null=' + firstParameter.null.booleanValue + ", "
            string += 'max_length=' + secondParameter.max_length.number + endElement
        elif firstParameter.null and secondParameter.default is not None:
            string += 'null=' + firstParameter.null.booleanValue + ", "
            if not dateTimeField:
                string += 'default=' + secondParameter.default.defaultValue.number + endElement
            else:
                string += 'default=timezone.' + \
                          secondParameter.default.defaultValue.timezone.var + endElement

        # First parameter is default
        elif firstParameter.default and secondParameter.max_length is not None:
            if not dateTimeField:
                string += 'default=' + firstParameter.default.defaultValue.number + ", "
            else:
                string += 'default=timezone.' + \
                          firstParameter.default.defaultValue.timezone.var + ", "
            # string += 'default=' + firstParameter.default.defaultValue.number + ", "
            string += 'max_length=' + secondParameter.max_length.number + endElement
        elif firstParameter.default and secondParameter.null is not None:
            if not dateTimeField:
                string += 'default=' + firstParameter.default.defaultValue.number + ", "
            else:
                string += 'default=timezone.' + \
                          firstParameter.default.defaultValue.timezone.var + ", "
            # string += 'default=' + firstParameter.default.defaultValue.number + ", "
            string += 'null=' + secondParameter.null.booleanValue + endElement
        return string

    #Generator koda za initial.py

    def test(models):
        string = 'from __future__ import unicode_literals\nfrom django.db import migrations, models\nimport django.db.models.deletion\nfrom django.utils import timezone\n\n\nclass Migration(migrations.Migration):\n\n\tinitial = True\n\n\tdependencies = [\n\t]\n\n\toperations = ['
        for model in models:
            string += '\n\t\t'
            string += 'migrations.CreateModel('
            string += '\n\t\t\tname=' + "'" + str(model['model']) + "',"
            string += '\n\t\t\tfields=['
            string += '\n\t\t\t\t(' + "'id'" + ", models.AutoField" + "(auto_created=True, primary_key=True, serialize=False, verbose_name=" + "'ID')),"
            for modelElement in model['modelElements']:
                string += '\n\t\t\t\t(' + "'"
                string += modelElement.name + "'," + " models."
                endElement = ")),"

                foreignKey = modelElement.elementType.foreignKey
                charField = modelElement.elementType.charField
                emailField = modelElement.elementType.emailField
                dateTimeField = modelElement.elementType.dateTimeField
                integerField = modelElement.elementType.integerField
                booleanField = modelElement.elementType.booleanField

                isDateTimeField = False
                if foreignKey is not None:
                    string += 'ForeignKey('
                    defaultParameter = foreignKey.parameters[0].default
                    onDeleteParameter = foreignKey.parameters[0].on_delete
                    if defaultParameter is not None:
                        string += 'default=' + defaultParameter.defaultValue.number
                    if onDeleteParameter is not None:
                        string += 'on_delete=django.db.models.deletion.CASCADE, '
                    string += 'to=' + "'" + 'myapp.' + foreignKey.className + "'" + endElement

                elif charField is not None:
                    numOfCharParameters = len(charField.parameters)
                    string += 'CharField' + "("
                    if numOfCharParameters == 0:
                        string += endElement
                    elif numOfCharParameters == 1:
                        maxLengthParameter = charField.parameters[0].max_length
                        nullParameter = charField.parameters[0].null
                        defaultParameter = charField.parameters[0].default

                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfCharParameters == 3:
                        maxLengthParameter = charField.parameters[0].max_length
                        nullParameter = charField.parameters[1].null
                        defaultParameter = charField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfCharParameters == 2:
                        firstParameter = charField.parameters[0]
                        secondParameter = charField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField, endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif emailField is not None:
                    numOfEmailParameters = len(emailField.parameters)
                    string += 'EmailField' + "("

                    if numOfEmailParameters == 0:
                        string += endElement

                    elif numOfEmailParameters == 1:
                        maxLengthParameter = emailField.parameters[0].max_length
                        nullParameter = emailField.parameters[0].null
                        defaultParameter = emailField.parameters[0].default

                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfEmailParameters == 3:
                        maxLengthParameter = emailField.parameters[0].max_length
                        nullParameter = emailField.parameters[1].null
                        defaultParameter = emailField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfEmailParameters == 2:
                        firstParameter = emailField.parameters[0]
                        secondParameter = emailField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField, endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif dateTimeField is not None:
                    numOfDateParameters = len(dateTimeField.parameters)
                    string += 'DateTimeField' + "("
                    isDateTimeField = True
                    if numOfDateParameters == 0:
                        string += endElement

                    elif numOfDateParameters == 1:
                        maxLengthParameter = dateTimeField.parameters[0].max_length
                        nullParameter = dateTimeField.parameters[0].null
                        defaultParameter = dateTimeField.parameters[0].default
                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            print(defaultParameter.defaultValue.timezone.var)
                            string += 'default=timezone.' + \
                                      defaultParameter.defaultValue.timezone.var + endElement

                    elif numOfDateParameters == 3:
                        maxLengthParameter = dateTimeField.parameters[0].max_length
                        nullParameter = dateTimeField.parameters[1].null
                        defaultParameter = dateTimeField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=timezone.' + \
                                  defaultParameter.defaultValue.timezone.var + endElement

                    elif numOfDateParameters == 2:
                        firstParameter = dateTimeField.parameters[0]
                        secondParameter = dateTimeField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField,
                                                                    endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif integerField is not None:
                    numOfIntegerParameters = len(integerField.parameters)
                    string += 'IntegerField' + "("

                    if numOfIntegerParameters == 0:
                        string += endElement

                    elif numOfIntegerParameters == 1:
                        maxLengthParameter = integerField.parameters[0].max_length
                        nullParameter = integerField.parameters[0].null
                        defaultParameter = integerField.parameters[0].default

                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfIntegerParameters == 3:
                        maxLengthParameter = integerField.parameters[0].max_length
                        nullParameter = integerField.parameters[1].null
                        defaultParameter = integerField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfIntegerParameters == 2:
                        firstParameter = integerField.parameters[0]
                        secondParameter = integerField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField, endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif booleanField is not None:
                    numOfBooleanParameters = len(booleanField.parameters)
                    string += 'BooleanField' + "("

                    if numOfBooleanParameters == 0:
                        string += endElement

                    elif numOfBooleanParameters == 1:
                        defaultParameter = booleanField.parameters[0].default
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement

            string += '\n\t\t\t],'
            string += '\n\t\t),'
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
            for modelElement in model['modelElements']:
                string += '\n\t'
                string += modelElement.name + "=" + "models."
                endElement = ")"

                foreignKey = modelElement.elementType.foreignKey
                charField = modelElement.elementType.charField
                emailField = modelElement.elementType.emailField
                dateTimeField = modelElement.elementType.dateTimeField
                integerField = modelElement.elementType.integerField
                booleanField = modelElement.elementType.booleanField

                isDateTimeField = False
                if foreignKey is not None:
                    string += 'ForeignKey(' + foreignKey.className + ', ' + 'on_delete=models.CASCADE'
                    defaultParameter = foreignKey.parameters[0].default
                    if defaultParameter is not None:
                        string += ', ' + 'default=' + defaultParameter.defaultValue.number + ')'
                    else:
                        string += endElement

                elif charField is not None:
                    numOfCharParameters = len(charField.parameters)
                    string += 'CharField' + "("
                    if numOfCharParameters == 0:
                        string += endElement
                    elif numOfCharParameters == 1:
                        maxLengthParameter = charField.parameters[0].max_length
                        nullParameter = charField.parameters[0].null
                        defaultParameter = charField.parameters[0].default

                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement
                    elif numOfCharParameters == 3:
                        maxLengthParameter = charField.parameters[0].max_length
                        nullParameter = charField.parameters[1].null
                        defaultParameter = charField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfCharParameters == 2:
                        firstParameter = charField.parameters[0]
                        secondParameter = charField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField, endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif emailField is not None:
                    numOfEmailParameters = len(emailField.parameters)
                    string += 'EmailField' + "("

                    if numOfEmailParameters == 0:
                        string += endElement

                    elif numOfEmailParameters == 1:
                        maxLengthParameter = emailField.parameters[0].max_length
                        nullParameter = emailField.parameters[0].null
                        defaultParameter = emailField.parameters[0].default

                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfEmailParameters == 3:
                        maxLengthParameter = emailField.parameters[0].max_length
                        nullParameter = emailField.parameters[1].null
                        defaultParameter = emailField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfEmailParameters == 2:
                        firstParameter = emailField.parameters[0]
                        secondParameter = emailField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField, endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif dateTimeField is not None:
                    numOfDateParameters = len(dateTimeField.parameters)
                    string += 'DateTimeField' + "("
                    isDateTimeField = True
                    if numOfDateParameters == 0:
                        string += endElement

                    elif numOfDateParameters == 1:
                        maxLengthParameter = dateTimeField.parameters[0].max_length
                        nullParameter = dateTimeField.parameters[0].null
                        defaultParameter = dateTimeField.parameters[0].default
                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            print(defaultParameter.defaultValue.timezone.var)
                            string += 'default=timezone.' + \
                                      defaultParameter.defaultValue.timezone.var + endElement

                    elif numOfDateParameters == 3:
                        maxLengthParameter = dateTimeField.parameters[0].max_length
                        nullParameter = dateTimeField.parameters[1].null
                        defaultParameter = dateTimeField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=timezone.' + \
                                  defaultParameter.defaultValue.timezone.var + endElement

                    elif numOfDateParameters == 2:
                        firstParameter = dateTimeField.parameters[0]
                        secondParameter = dateTimeField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField,
                                                                    endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif integerField is not None:
                    numOfIntegerParameters = len(integerField.parameters)
                    string += 'IntegerField' + "("

                    if numOfIntegerParameters == 0:
                        string += endElement

                    elif numOfIntegerParameters == 1:
                        maxLengthParameter = integerField.parameters[0].max_length
                        nullParameter = integerField.parameters[0].null
                        defaultParameter = integerField.parameters[0].default

                        if maxLengthParameter is not None:
                            string += 'max_length=' + maxLengthParameter.number + endElement
                        if nullParameter is not None:
                            string += 'null=' + nullParameter.booleanValue + endElement
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfIntegerParameters == 3:
                        maxLengthParameter = integerField.parameters[0].max_length
                        nullParameter = integerField.parameters[1].null
                        defaultParameter = integerField.parameters[2].default

                        string += 'max_length=' + maxLengthParameter.number + ", "
                        string += 'null=' + nullParameter.booleanValue + ", "
                        string += 'default=' + defaultParameter.defaultValue.number + endElement

                    elif numOfIntegerParameters == 2:
                        firstParameter = integerField.parameters[0]
                        secondParameter = integerField.parameters[1]

                        string2Parameters = getStringFor2Parameters(firstParameter, secondParameter, isDateTimeField, endElement)
                        # print(string2Parameters)
                        string += string2Parameters

                elif booleanField is not None:
                    numOfBooleanParameters = len(booleanField.parameters)
                    string += 'BooleanField' + "("

                    if numOfBooleanParameters == 0:
                        string += endElement

                    elif numOfBooleanParameters == 1:
                        defaultParameter = booleanField.parameters[0].default
                        if defaultParameter is not None:
                            string += 'default=' + defaultParameter.defaultValue.number + endElement

            string += '\n\n\t'
            string += "'''"
            string += '\n\tYou can chose one of these atributes to be returned instead of type object!'
            string += '\n\tdef __str__(self):'
            for modelElement in model['modelElements']:
                string += '\n\t\treturn self.' + modelElement.name
            string += '\n\t' + "'''"
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
            string += '\n\n\n'
            string += '# Create view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'CreateView' + '(CreateView):'
            string += '\n    template_name = ' + "'" + '.html' + "'"
            string += '\n    model = ' + str(model['model'])
            string += '\n    fields = ['
            last = len(model['modelElements']) - 1
            for i, modelElement in enumerate(model['modelElements']):
                string += "'" + modelElement.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '
            string += '\n    success_url = reverse_lazy(' + "'" + "'" + ")"

            # UpdateView generator
            string += '\n\n\n'
            string += '# Update view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'UpdateView' + '(UpdateView):'
            string += '\n    template_name = ' + "'" + '.html' + "'"
            string += '\n    model = ' + str(model['model'])
            string += '\n    fields = ['
            last = len(model['modelElements']) - 1
            for i, modelElement in enumerate(model['modelElements']):
                string += "'" + modelElement.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '

            # DeleteView generator
            string += '\n\n\n'
            string += '# Delete view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'DeleteView' + '(DeleteView):'
            string += '\n    template_name = ' + "'" + '.html' + "'"
            string += '\n    model = ' + str(model['model'])
            string += '\n    success_url = reverse_lazy(' + "'" + "'" + ")"

            # ListView generator
            string += '\n\n\n'
            string += '# List view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'ListView' + '(generic.ListView):'
            string += '\n    template_name = ' + "'" + '.html' + "'"
            string += '\n    context_object_name = ' + "'" + 'all_' + str(model['model']) + "'"
            string += '\n\n    def get_queryset(self):'
            string += '\n        return ' + str(model['model']) + '.object.all'

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

    # Kreiranje template i layout deirektorojuma
    newpath = r'E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/templates/layout'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Generator index.html stranice
    def test6(models):
        string = '<!DOCTYPE html>\n'
        string += '<html lang = "en">\n'
        string += '<head>\n'
        string += '\t<meta charset = "UTF-8">\n'
        string += '\t<title> {% block title %}MyApp{% endblock %} </title>\n'
        string += '\t{% load staticfiles %}\n'
        string += '\t<script src = "https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>\n'
        string += '\t<script src = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n'
        string += '</head>\n'
        string += '<body>\n'
        for model in models:
            string += '<p>' + str(model['model']) + '</p>\n'
        string += '</body>\n'

        return string

    with open('E:/Jovana/Desktop/zavrsi/jsd2017/JSD/generated/templates/layout/index.html', 'w') as f:
        a = test6(models1)
        f.write(a)

