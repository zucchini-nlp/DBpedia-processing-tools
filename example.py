from Knowledge_base_utils import Knowledge_Graph


kb = Knowledge_Graph("DBpedia_files/dbpedia-2015-10.hdt")

# Get one hope relations
obama_relations = kb.get_relations_1hop("http://dbpedia.org/resource/Barack_Obama")
print(f"Entity of Barack Obama has the following relations in the kb: {obama_relations[:3]} etc.")


# Execute your sparql query
query = """
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX dbtype: <http://dbpedia.org/datatype/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT * WHERE {
        dbr:Barack_Obama ?rel ?obj .
}
"""
res = kb.execute_sparql(query)
for el in res:
    print(str(el.asdict()["rel"].toPython()))


# Get one hop connections between two entities
connections = kb.get_connection_1hop("http://dbpedia.org/resource/Barack_Obama", "http://dbpedia.org/resource/Michelle_Obama")
print(f"All paths between Barack Obama and Michelle Obama: {connections}")