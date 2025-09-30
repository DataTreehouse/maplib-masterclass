from rdflib import Graph

def write_output(m, output_file: str):

    with open(output_file, "w") as file:
        pass

    m.write_triples(output_file, format="turtle")

    g = Graph()
    g.bind("dt", "http://data.treehouse.example/")
    g.parse(output_file, format="turtle")

    g.serialize(output_file, format="turtle")