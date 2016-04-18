import json
from pprint import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

class MyElasticsearch:
    #defind an elasticsearch
    def __init__(self, data, schema):
        self.es = Elasticsearch()
        self.data = data
        self.schema = schema

    ##############create index#################
    def create_movie_index(self):
        if not self.es.indices.exists("es_movie_yao"):
            moive_index = self.es.indices.create(index = "es_movie_yao", body = self.schema)
            return "es_movie_yao"
        return "es_movie_yao"

    ############## bulk document loading #################
    def format_action(self, id, value):
        return {
            "_index": "es_movie_yao",
            "_type": "movie",
            "_id": id,
            "_source": value
        }

    def bulk_insert(self):
        actions = []
        for key, value in self.data.iteritems():
            actions.append(self.format_action(key, value))
        helpers.bulk(self.es, actions, stats_only=True)


    ############## search #################
    #total docs (size of index) : q_total()
    #Return doc count, (i.e., matching all docs)
    def q_totall(self):
        res = self.es.search(index="es_movie_yao", body={"query": {"match_all": {}}})
        return res['hits']['total']

    #Range query: q_time_range(year1, year2)
    #Return doc count with time within range
    def q_time_range(self, year1, year2):
        doc_count = 0
        for i in self.data:
            res = self.es.get(index="es_movie_yao", doc_type='movie', id=i)
            for time in res['_source']['time']:
                if int(time) >= year1 or int(time) <= year2:
                    doc_count = doc_count + 1
        return doc_count


    #Search within specific fields (e.g., director, country): q_field(field_name, value)
    #Return docs and their field values (for specified field)
    def q_field(self, field_name, value):
        query_body={
            "query": {
                "match": {
                    field_name: value
                }
            }
        }
        res = self.es.search(index="es_movie_yao", body=query_body)
        return res['hits']['hits']

    #Search text using multiword queries: q_mw(string)
    #Match over title and text fields only
    #Test ranking  of results
    #Test analysis on those fields (tokenization, stemming, case...)
    def q_mw(self, query_string, fields_list=["title", "text"]):
        query_body={
            "from":0, "size":10,
            "query":{
                    "multi_match":{
                        "query":query_string,
                        "fields":fields_list
                    }
            },
            "highlight":{"fields":{
                    "text":{},
                    "title":{}
                }
            }
        }
        res = self.es.search(index="es_movie_yao", doc_type='movie', body=query_body)
        return res['hits']['hits']

    #Search text using a phrase: q_phr(phrase)
    #Test phrase match
    #Compare to result for multiword query of same phrase
    def q_phr(self, phrase):
        query_body={
            "query": {
                "match_phrase": {
                    "text": phrase
                }
            }
        }
        res = self.es.search(index="es_movie_yao", doc_type='movie', body=query_body)
        return res['hits']['hits']

    #Search on a combination of fields: q_fs([field, value]*)
    #Enforce conjunctive queries (all terms within a field, except noisewords, and all fields must match)
    def q_fs(self, fields_values):
        query_body={
            "query": {
                "bool": {
                    "must": []
                }
            },
            "highlight":{
                "pre_tags" : ["<em style=\"background-color: red\">"],
                "post_tags" : ["</em>"],
                "fields":{
                    "text":{"type":"plain"},
                    "title":{"type":"plain"},
                    "language":{"type":"plain"},
                    "runtime":{"type":"plain"},
                    "starring":{"type":"plain"},
                    "categories":{"type":"plain"},
                    "country":{"type":"plain"},
                    "time":{"type":"plain"},
                    "location":{"type":"plain"},
                    "director":{"type":"plain"}
                }
            }
        }
        for field,value in fields_values.iteritems():
            if "\"" in value and field == "text":
                value.replace('\"','')
                query_body["query"]["bool"]["must"].append({"match_phrase":{field:value}})
            else:
                query_body["query"]["bool"]["must"].append({"match":{field:value}})
        res = self.es.search(index="es_movie_yao", body=query_body)
        return res['hits']['total'], res['hits']['hits']
