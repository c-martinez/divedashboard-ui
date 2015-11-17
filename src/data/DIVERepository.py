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
		self.SEM = 'http://semanticweb.cs.vu.nl/2009/11/sem/'

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

	"""-----------------------------------------------------------------------
	--------COLLECTION STATS FUNCTIONS----------------------------------------
	-----------------------------------------------------------------------"""

	def getCollectionStats(self, collection):
		problems = {
			'no-source' : self.getMediaObjectsWithoutSource(collection),
			'broken-events' : self.getIncompleteEvents(collection)
		}
		return problems

	def getMediaObjectsWithoutSource(self, collection):
		items = []
		results = self.executeQuery("""
			SELECT ?item ?title WHERE {
				?item dive:inCollection <%s> .
				?item a ?type .
				?type rdfs:subClassOf* dive:MediaObject .
				?item am:title ?title .
				FILTER NOT EXISTS {?item dive:source ?src}
			}
			LIMIT 100
			""" % collection)
		for result in results["results"]["bindings"]:
			items.append({
				'uri' : result["item"]["value"],
				'title' : result["title"]["value"]
			})
		return items

	def getIncompleteEvents(self, collection):
		items = []
		results = self.executeQuery("""
			PREFIX sem: <%s>
			SELECT DISTINCT ?event ?mo ?title ?actor ?actorName ?place ?placeName WHERE {
				?event a sem:Event .
				?event dive:depictedBy ?mo .
				?mo dive:inCollection <%s> .
				OPTIONAL {?mo am:title ?title }
				OPTIONAL {?mo rdfs:label ?title }
				OPTIONAL {?event sem:hasPlace ?place . ?place rdfs:label ?placeName}
 				OPTIONAL {?event sem:hasActor ?actor . ?actor rdfs:label ?actorName}
				FILTER NOT EXISTS {?event sem:hasPlace ?place ; sem:hasActor ?actor}
			}
			LIMIT 3900
			""" % (self.SEM, collection) )
		print results
		for result in results["results"]["bindings"]:
			item = {
				'uri' : result["event"]["value"],
				'mediaUri' : result["mo"]["value"],
				'mediaTitle' : result["title"]["value"]
			}
			if result.has_key('actor'):
				item['actor'] = result["actor"]["value"]
				item['actorName'] = result["actorName"]["value"]
			if result.has_key('place'):
				item['place'] = result["place"]["value"]
				item['placeName'] = result["placeName"]["value"]
			items.append(item)
		return items

	def executeQuery(self, query):
		sparql = SPARQLWrapper(self.config['DIVE_SPARQL'])
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		return results


if __name__ == '__main__':
	conf = {
		'DIVE_SPARQL' : 'http://data.dive.beeldengeluid.nl/sparql/'
	}
	d = DIVERepository(conf)
	print d.listCollections()
