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
"""

class DIVERepository():

	def __init__(self, config):
		self.config = config

	def listCollections(self):
		collections = []
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
	conf = {}
	d = DIVERepository(conf)
	print d.listCollections()