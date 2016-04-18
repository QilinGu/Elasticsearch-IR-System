import web
from web import form
from build_es_movies_index_Yao import MyElasticsearch
import json
from pprint import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

#open and read a json file into "data"
with open('2015_movies.json') as data_file:
    data = json.load(data_file)

#schema contains "settings" and "mappings"
with open('es_mapping_file.json') as mapping_file:
    schema = json.load(mapping_file)
#create an elasticsearch object so that we can do queries
myElasticsearch = MyElasticsearch(data, schema)
#create index
myElasticsearch.create_movie_index()
#bulk document loading
myElasticsearch.bulk_insert()

render = web.template.render('templates/')

urls = ('/', 'index',
		'/results', 'results')
app = web.application(urls, globals())

myform = form.Form(form.Textbox("language:"),
			       form.Textbox("title:"),
				   form.Textbox("country:"),
				   form.Textbox("time:"),
				   form.Textbox("director:"),
				   form.Textbox("location:"),
				   form.Textbox("starring:"),
				   form.Textbox("text:"),
				   form.Textbox("runtime:"),
				   form.Textbox("categories:"))
new_myform = form.Form(form.Textbox("language.:"),
			       form.Textbox("title.:"),
				   form.Textbox("country.:"),
				   form.Textbox("time.:"),
				   form.Textbox("director.:"),
				   form.Textbox("location.:"),
				   form.Textbox("starring.:"),
				   form.Textbox("text.:"),
				   form.Textbox("runtime.:"),
				   form.Textbox("categories.:"))
new_button_myform = form.Form(form.Button("Next 10 relevant films"))

class index:
    def GET(self):
        form = myform()
        return render.page_1(form)

class results:
    def GET(self):
        form = myform()
        new_button_form = new_button_myform()
        new_form = new_myform()
        if not form.validates():
            return render.page_1(form)
        #define a dictionary to collect the data from user input
        input_dic = {}
        related_fields = []
        if form["language:"].value:
            input_dic['language'] = str(form["language:"].value)
            related_fields.append('language')
        if form["title:"].value:
            input_dic['title'] = str(form["title:"].value)
            related_fields.append('title')
        if form["country:"].value:
            input_dic['country'] = str(form["country:"].value)
            related_fields.append('country')
        if form["time:"].value:
            input_dic['time'] = str(form["time:"].value)
            related_fields.append('time')
        if form["director:"].value:
            input_dic['director'] = str(form["director:"].value)
            related_fields.append('director')
        if form["location:"].value:
            input_dic['location'] = str(form["location:"].value)
            related_fields.append('location')
        if form["starring:"].value:
            input_dic['starring'] = str(form["starring:"].value)
            related_fields.append('starring')
        if form["text:"].value:
            input_dic['text'] = str(form["text:"].value)
            related_fields.append('text')
        if form["runtime:"].value:
            input_dic['runtime'] = str(form["runtime:"].value)
            related_fields.append('runtime')
        if form["categories:"].value:
            input_dic['categories'] = str(form["categories:"].value)
            related_fields.append('categories')
        #do search query
        hits, content_list = myElasticsearch.q_fs(input_dic)
        if hits <= 10:
            return render.page_2(hits, content_list, related_fields, new_form, None)
        else:
            return render.page_2(hits, content_list, related_fields, new_form, new_button_form)

    def POST(self):
        form = new_myform()
        if not form.validates():
            return render.page_1(form)
        new_button_form = new_button_myform()
        new_form = new_myform()
        #define a dictionary to collect the data from user input
        input_dic = {}
        related_fields = []
        if form["language.:"].value:
            input_dic['language'] = str(form["language.:"].value)
            related_fields.append('language')
        if form["title.:"].value:
            input_dic['title'] = str(form["title.:"].value)
            related_fields.append('title')
        if form["country.:"].value:
            input_dic['country'] = str(form["country.:"].value)
            related_fields.append('country')
        if form["time.:"].value:
            input_dic['time'] = str(form["time.:"].value)
            related_fields.append('time')
        if form["director.:"].value:
            input_dic['director'] = str(form["director.:"].value)
            related_fields.append('director')
        if form["location.:"].value:
            input_dic['location'] = str(form["location.:"].value)
            related_fields.append('location')
        if form["starring.:"].value:
            input_dic['starring'] = str(form["starring.:"].value)
            related_fields.append('starring')
        if form["text.:"].value:
            input_dic['text'] = str(form["text.:"].value)
            related_fields.append('text')
        if form["runtime.:"].value:
            input_dic['runtime'] = str(form["runtime.:"].value)
            related_fields.append('runtime')
        if form["categories.:"].value:
            input_dic['categories'] = str(form["categories.:"].value)
            related_fields.append('categories')
        #do search query
        hits, content_list = myElasticsearch.q_fs(input_dic)
        if hits <= 10:
            return render.page_2(hits, content_list, related_fields, new_form, None)
        else:
            return render.page_2(hits, content_list, related_fields, new_form, new_button_form)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
