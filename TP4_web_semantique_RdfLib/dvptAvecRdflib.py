import isodate
from SPARQLWrapper import SPARQLWrapper, JSON, N3, TURTLE
from rdflib import Graph, URIRef, Literal
import json
import ssl


class RdfDev:
    def __init__(self):
        """__init__
        Initialise la session de collecte
        :return: Object of class Collecte
        """
        # NE PAS MODIFIER
        self.basename = "rdfsparql.step"

    def rdfdev(self):
        """collectes
        Plusieurs étapes de collectes. VOTRE CODE VA VENIR CI-DESSOUS
        COMPLETER les méthodes stepX.
        """
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()

    def step1(self):
        stepfilename = self.basename+"1"
        result = {"typelist": []}
        # votre code ici
        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX dbo: <http://dbpedia.org>
            SELECT DISTINCT ?t
            WHERE {
                ?h a ?t
            }
            LIMIT 10
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                result["typelist"].append(r["t"]["value"])
        except Exception as e:
            print(e)
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step2(self):
        stepfilename = self.basename+"2"
        result = {}
        # votre code ici
        result['prefix'] = "http://xmlns.com/foaf/0.1/"
        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT (count(?p) as ?count)
            WHERE {
                ?p a foaf:Person
            }
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            result["personcount"] = ret["results"]["bindings"][0]["count"]["value"]
        except Exception as e:
            print(e)

        result["firstten"] = []
        sparql.setQuery("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?p
            WHERE {
                ?p a foaf:Person
            }
            LIMIT 10
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                result["firstten"].append(r["p"]["value"])
        except Exception as e:
            print(e)

        result["tenothers"] = []
        sparql.setQuery("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?p
            WHERE {
                ?p a foaf:Person
            }
            OFFSET 100
            LIMIT 10
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                result["tenothers"].append(r["p"]["value"])
        except Exception as e:
            print(e)

        result["urlhtml"] = "https://dbpedia.org/page/"

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step3(self):
        stepfilename = self.basename+"3"
        result = {}
        # votre code ici
        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT (COUNT (DISTINCT ?predicats) as ?count) 
            WHERE {
                {SELECT ?pers WHERE { ?pers a foaf:Person} limit 1000}
                ?pers ?predicats ?o
            }
        """)
        result[
            "rqcount"] = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT (COUNT(DISTINCT ?predicats) as ?count) WHERE {{SELECT ?pers WHERE {{ ?pers a foaf:Person}} limit 1000}} ?pers ?predicats ?o"
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            result["predicatescount"] = ret["results"]["bindings"][0]["count"]["value"]
        except Exception as e:
            print(e)

        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT ?predicats 
            WHERE {
                {SELECT ?pers WHERE { ?pers a foaf:Person} limit 1000}
                ?pers ?predicats ?o
            }
            LIMIT 20
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            result["predicates"] = []
            for r in ret["results"]["bindings"]:
                result["predicates"].append(r["predicats"]["value"])
        except Exception as e:
            print(e)

        result["rqpredicates"] = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT DISTINCT ?predicats WHERE {{SELECT ?pers WHERE {{ ?pers a foaf:Person}} limit 1000}} ?pers ?predicats ?o LIMIT 20"

        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT (COUNT(?p) as ?count) 
            WHERE {
                {?p a foaf:Person}   
                ?p <http://dbpedia.org/ontology/deathPlace> ?o
            }
        """)
        result[
            "rqplacecount"] = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT (COUNT(?p) as ?count) WHERE {{?p a foaf:Person} ?p <http://dbpedia.org/ontology/deathPlace> ?o}"
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            result["placecount"] = ret["results"]["bindings"][0]["count"]["value"]
        except Exception as e:
            print(e)
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step4(self):
        stepfilename = self.basename+"4"
        result = {}
        # votre code ici
        result["julesverne"] = []
        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?p
            WHERE {
                ?p a foaf:Person;
                rdfs:label "Jules Verne"@fr
            }
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                result["julesverne"].append(r["p"]["value"])
        except Exception as e:
            print(e)

        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            SELECT ?predicat
            WHERE {
                <http://dbpedia.org/resource/Jules_Verne> ?predicat  "Jules Verne"@fr
            }
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            result["jvpredicate"] = ret["results"]["bindings"][0]["predicat"]["value"]

        except Exception as e:
            print(e)

        result["jvdoc"] = []
        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            SELECT ?value
            WHERE {
                <http://dbpedia.org/resource/Jules_Verne> <http://dbpedia.org/property/notableworks> ?value
            }
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                result["jvdoc"].append(r["value"]["value"])
        except Exception as e:
            print(e)

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step5(self):
        stepfilename = self.basename+"5"
        result = {}
        # votre code ici
        result["jvpredicates"] = []
        ssl._create_default_https_context = ssl._create_unverified_context
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setQuery("""
            SELECT DISTINCT ?predicat
            WHERE {
                <http://dbpedia.org/resource/Jules_Verne> ?predicat ?o   
            }
        """)
        try:
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                result["jvpredicates"].append(r["predicat"]["value"])
        except Exception as e:
            print(e)

        nb_triplets = 0
        offset = 0
        limit = 100
        loop_on = True

        while loop_on:
            sparql.setQuery(f"""
                SELECT ?p ?o
                WHERE {{
                    <http://dbpedia.org/resource/Jules_Verne> ?p ?o
                }}
                LIMIT {limit} OFFSET {offset}
            """)
            try:
                sparql.setReturnFormat(JSON)
                ret = sparql.queryAndConvert()
                if ret["results"]["bindings"]:
                    nb_triplets += len(ret["results"]["bindings"])
                    offset += limit
                else:
                    loop_on = False
            except Exception as e:
                print(e)

        result["triplecount"] = nb_triplets

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)


if __name__ == "__main__":
    testeur = RdfDev()
    testeur.rdfdev()
