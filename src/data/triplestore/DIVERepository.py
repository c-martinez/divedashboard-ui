#!/usr/bin/python

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

	def getCollectionTestResults(self, collection):
		noSource = self.testMediaObjectsWithoutSource(collection)
		brokenEvents = self.testIncompleteEvents(collection)
		tests = {
			'no-source' : {'name' : 'Media objects with no source', 'results' : noSource},
			'broken-events' : {'name' : 'Events without both actors and places', 'results' : brokenEvents}
		}
		return tests

	#TODO add the edm:object check as well! (AM uses this)
	def testMediaObjectsWithoutSource(self, collection):
		results = self.executeQuery("""
			SELECT ?item ?title WHERE {
				?item dive:inCollection <%s> .
				?item a ?type .
				?type rdfs:subClassOf* dive:MediaObject .
				?item am:title ?title .
				OPTIONAL {?item dive:source ?src}
				OPTIONAL {?item edm:object ?src2}
				FILTER (!bound(?src) && !bound(?src2))
			}
			""" % collection)
		if results:
			items = []
			for result in results["results"]["bindings"]:
				items.append({
					'uri' : result["item"]["value"],
					'title' : result["title"]["value"]
				})
			return items
		return None

	def testIncompleteEvents(self, collection):
		results = self.executeQuery("""
			PREFIX sem: <%s>
			SELECT ?event ?mo ?title ?actor ?actorName ?place ?placeName WHERE {
				?event a sem:Event .
				?event dive:depictedBy ?mo .
				?mo dive:inCollection <%s> .
				?hasTitle rdfs:subClassOf* rdfs:label .
  				?mo ?hasTitle ?title .
				OPTIONAL {?event sem:hasPlace ?place . ?place rdfs:label ?placeName}
 				OPTIONAL {?event sem:hasActor ?actor . ?actor rdfs:label ?actorName}
				FILTER NOT EXISTS {?event sem:hasPlace ?place ; sem:hasActor ?actor}
			}
			""" % (self.SEM, collection) )
		if results:
			items = {}
			uri = None
			item = None
			for result in results["results"]["bindings"]:
				uri = result["event"]["value"]
				if items.has_key(uri):
					item = items[uri]
				else:
					item = {}
					item['mediaUri'] = result["mo"]["value"]
					item['mediaTitle'] = result["title"]["value"]
					item['actors'] = []
					item['places'] = []

				#add actor
				if result.has_key('actor'):
					item['actors'].append({
						'uri' : result["actor"]["value"],
						'name' : result["actorName"]["value"]
					})

				#add place
				if result.has_key('place'):
					item['places'].append({
						'uri' : result["place"]["value"],
						'name' : result["placeName"]["value"]
					})
				items[uri] = item
			return items
		return None


#    UNUSED CODE ??
	#get an overview of what was annotated
#	def testNotMachineAnnotated(self, collection):
#		results = self.executeQuery("""
#			SELECT ?mo ?prov WHERE {
#				?mo a ?type .
#				?type rdfs:subClassOf* dive:MediaObject .
#				?mo dive:inCollection <%s> .
 # 				OPTIONAL {?ann a oa:Annotation ; oa:hasTarget ?mo ; dive:prov ?prov . }
#				FILTER NOT EXISTS {
#					?ann a oa:Annotation ; oa:hasTarget ?mo ; dive:prov ?prov .
#					FILTER (regex(?prov, "NLP extractors"))
#				}
#
#			}
#			LIMIT 10
#			""" % collection
#		)

	def executeQuery(self, query):
		sparql = SPARQLWrapper(self.config['DIVE_SPARQL'])
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		if not results or len(results["results"]["bindings"]) == 0:
			return None
		return results


if __name__ == '__main__':
	conf = {
		'DIVE_SPARQL' : 'http://data.dive.beeldengeluid.nl/sparql/'
	}
	d = DIVERepository(conf)
	print d.listCollections()
