#!/usr/bin/python

import rdflib
from rdflib.namespace import RDF, FOAF, DC, DCTERMS
from rdflib import URIRef, BNode, Literal
from rdflib import Graph, ConjunctiveGraph, Namespace
from rdflib.plugins.stores import sparqlstore
from SPARQLWrapper import SPARQLWrapper, JSON

"""
Used libs:
- rdflib
- https://rdflib.github.io/sparqlwrapper/

Get the collection provenance relation

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?obj WHERE {
  ?sub dive:inCollection ?obj .
}
LIMIT 10
"""

class DIVERepository():

	def __init__(self, config):
		self.config = config
		self.DIVE = 'http://purl.org/collections/nl/dive/'
		self.PROV = 'http://www.w3.org/ns/prov#'
		self.RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
		self.RDFS = 'http://www.w3.org/2000/01/rdf-schema#'

	def getCollections(self, user):
		collections = []
		sparql = SPARQLWrapper(self.config['DIVE_SPARQL'])
		sparql.setQuery("""
			SELECT DISTINCT ?col ?label WHERE {
  				?col a dive:Collection .
  				?col rdfs:label ?label
			}
			LIMIT 30
			""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		print results
		for result in results["results"]["bindings"]:
			collections.append({
				'uri' : result["col"]["value"],
				'label' : result["label"]["value"]
			})
		return collections

	def getCollectionStats(self, collection):
		stats = {
			'orphaned' : ['1', '2', '3'],
			'no-entities' : ['2', '3']
		}
		sparql = SPARQLWrapper(self.config['DIVE_SPARQL'])
		sparql.setQuery("""
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			SELECT ?label
			WHERE { ?res rdfs:label ?label } LIMIT 5
		""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		print results
		for result in results["results"]["bindings"]:
			print(result["label"]["value"])
		return stats

if __name__ == '__main__':
	conf = {
		'DIVE_SPARQL' : 'http://data.dive.beeldengeluid.nl/sparql/'
	}
	d = DIVERepository(conf)
	print d.listCollections()
