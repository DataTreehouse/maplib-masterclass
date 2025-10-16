from rdflib import Graph

def write_output(m, output_file: str):

    with open(output_file, "w") as file:
        pass

    m.write(output_file, format="turtle")

    g = Graph()
    g.bind("dt", "http://data.treehouse.example/")
    g.bind("shapes", "http://data.treehouse.example/sh/")
    g.parse(output_file, format="turtle")

    g.serialize(output_file, format="turtle")

def print_count(msg: str, m):
    
    count = """
        SELECT (COUNT(?s) AS ?count)
        WHERE { ?s ?p ?o . }
    """
    print("Graph size after ", msg, ": ", m.query(count)["count"][0])