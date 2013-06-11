#!/usr/bin/python2.7

from SPARQLWrapper import SPARQLWrapper, JSON
from Levenshtein import ratio
import math

sparql = SPARQLWrapper("http://94.23.12.201:3030/stcn/sparql")
sparql.setQuery("""
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT DISTINCT ?title ?author ?publisher ?year ?s
FROM <http://knuttel.data2semantics.org>
WHERE {
?s dc:title ?title .
}
""")

sparql.setReturnFormat(JSON)
print 'Launching SPARQL query...'
resultsKnuttel = sparql.query().convert()
print 'Done.'

sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>

SELECT DISTINCT ?title ?p
FROM <http://stcn.data2semantics.org> 
WHERE {
?p rdf:type vocab:Publicatie ;
            rdfs:label ?title .
}
""")

sparql.setReturnFormat(JSON)
print 'Launching SPARQL query...'
resultsSTCN = sparql.query().convert()
print 'Done.'

print "Computing similarities"
for y in resultsKnuttel["results"]["bindings"]:
    max_r = 0
    knuttel_title = y["title"]["value"]
    close_title = ""
    for x in resultsSTCN["results"]["bindings"]:
        stcn_title = x["title"]["value"]
        r_title = ratio(knuttel_title,
                        stcn_title)
        print knuttel_title, stcn_title, r_title
        if r_title > max_r:
            max_r = r
            close_title = stcn_title
    print "Best match of", knuttel_title, "is", close_title
