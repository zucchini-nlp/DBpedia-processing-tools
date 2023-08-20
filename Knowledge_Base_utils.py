import typing import List
from hdt import HDTDocument
from rdflib import Graph
from rdflib_hdt import HDTStore


class Knowledge_Graph:

    def __init__(self, kb_path: str):
        self.kb = HDTDocument(kb_path)
        self.graph = Graph(store=HDTStore(kb_path))

        print(f"KB loaded, it has {self.kb.total_triples} triples")

    def get_relations_1hop(self, entity: str, limit: int=1000):
        """
        Get all relation that are one hop away from a given entity id. 
        """
        forw, _ = self.kb.search_triples(entity, "", "")
        back, _ = self.kb.search_triples("", "", entity)
        relations_1hop = set()
        for triplet in forw:
            subj, rel, obj = triplet
            relations_1hop.update([rel])
        
        for triplet in back:
            subj, rel, obj = triplet
            relations_1hop.update([rel])

        return list(relations_1hop)[:limit]


    def get_neighbors_1hop(self, entity: str):
        """
        Get all neighboring entities that are one hop away from a given entity id. 
        """
        forw, _ = self.kb.search_triples(entity, "", "")
        back, _ = self.kb.search_triples("", "", entity)
        neighbors_1hop = set()
        for triplet in forw:
            subj, rel, obj = triplet
            neighbors_1hop.update([obj])
        
        for triplet in back:
            subj, rel, obj = triplet
            neighbors_1hop.update([subj])

        return list(neighbors_1hop)[:limit]
        
    
    def get_frequency(self, entity: str):
        """
        Finds the frequency of an entity by counting how many triplets contain the entity
        """
        _, car = self.kb.search_triples(entity, "", "")
        _, car2 = self.kb.search_triples("", "", entity)
        return car + car2


    def get_connection_1hop(self, src: str, trg: str):
        """
        Finds all one hop paths between two entities, if there exists any such path.
        """
        res, _ = self.kb.search_triples(src, "", trg)
        res2, _ = self.kb.search_triples(trg, "", src)
        return list(res) + list(res2)

    
    def get_connection_2hop(self, src: str, trg: str):
        """
        Finds all two hop paths between two entities, if there exists any such path.
        """
        neighbors1 = get_neighbors_1hop(src)
        neighbors2 = get_neighbors_1hop(trg)
        intersection_entities = neighbors1 & neighbors2
        if not intersection_entities:
            return []

        connections = []
        for entity in intersection_entities:
            if self.get_frequency(entity) > 100000:
                continue
            connections1 = self.get_connection_1hop(src, entity)
            connections2 = self.get_connection_1hop(entity, trg)
            connections.append((connections1 + connections2))
        return connections


    def get_subgraph_triplets(self, topic_entity: str, curr_path: List[str], limit: int=1000):
        """
        Find a subgraph given a topic entity and a path of relations (max 2hop) from that entity.
        """
        if len(curr_path) == 1:
            rel = curr_path[0]
            triplets, _ = self.kb.search_triples(topic_entity, rel, "")
        
        elif len(curr_path) == 2:
            query = f"""
                SELECT DISTINCT * WHERE {{
                    {topic_entity} {curr_path[0]} ?obj1 .
                    ?obj1 {curr_path[1]} ?obj2 .
                }} LIMIT {limit}
            """
            res = self.graph.query(query)
            triplets = []
            for r in res:
                cand = r.asdict()
                filled_triplets = [[topic_entity, curr_path[0], "?obj1"], ["?obj1", curr_path[1], "?obj2"]]
                for unk_uri, unk_uri_lbl in cand.items():
                    unk_uri_label = str(unk_uri_lbl.toPython())
                    filled_triplets = [tuple(el.replace(unk_uri, unk_uri_lbl) for el in triplet) for triplet in filled_triplets]
                triplets += filled_triplets
        return triplets

    def execute_sparql(self, query: str):
        res = self.graph.query(query)
        return res


    def deduce_triplets_from_sparql(self, query: str):
        """
        Finds all triplets that a given sparql query uses while being executed and replaces unknown variables with the real values foudn after execution.
        Can be used to deduce triplets list from a sparql query in KBQA datasets like LC-QUaD.
        """
        
        prefixes = """
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT * WHERE {
        """
        body = re.findall(r'\{(.*)\}', sparql)[0]
        sparql_parts = re.findall(r'\{(.*?)\s?(?:FILTER.*)?\}', sparql, re.IGNORECASE)[0].split(". ")
        triplets, unk_triplets = [], []
        for query_triplet in sparql_parts:
            if not query_triplet:
                continue
            subj, rel, obj = query_triplet.split()[:3]:
            if not subj.startswith("?") and not obj.startswith("?"):
                triplets.append((subj, rel, obj))
            else:
                unk_triplets.append([subj, rel, obj])

        res = graph.query(prefixes + body + "}")
        for r in res:
            cand = r.asdict()
            filled_triplets = unk_triplets.copy()
            for unk_uri, unk_uri_lbl in cand.items():
                unk_uri_label = str(unk_uri_lbl.toPython())
                filled_triplets = [tuple(el.replace(unk_uri, unk_uri_lbl) for el in triplet) for triplet in filled_triplets]
            triplets += filled_triplets
        return set(triplets)