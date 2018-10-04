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
    print(model.pages[0].title)

    pages = model.pages
    pages1 = []
    for page in pages:
        pageElements = page.pageElements
        dict = {}
        dict['page'] = page.title
        dict['pageElements'] = pageElements
        print(dict)
        pages1.append(dict)

    print(pages1)
    #Generator html stranice

    def test(page):
        # for page in pages:
            string = '<!DOCTYPE html>\n'
            string += '<html>\n'
            string += '<head>\n'
            string += '<title>' + str(page['page']) + '</title>\n'
            string += '</head>'
            string += '<body>'

            for pageElement in page['pageElements']:
                if pageElement.elementType.heading is not None:
                    level = str(pageElement.elementType.heading.level)
                    print(level)
                    string += '<h' + level + '>'
                    headText = pageElement.elementType.heading.parameters[0].text.content
                    print(headText)
                    if headText is not None:
                        string += headText
                        string += '</h' + level + '>'

                if pageElement.elementType.paragraph is not None:
                    parText = pageElement.elementType.paragraph.parameters[0].text.content
                    print(parText)
                    string += '<p>' + parText + '</p>'
                    string += '/<body>'
                    string += '/<html>'

                    return string

    for page in pages1:
        with open('E:/Jovana/Desktop/test/' + str(page['page']) + '.html', 'w') as f:
            a = test(page)
            # a = model.pages[0].title
            f.write(a)

