def print_count(msg: str, m):
    
    count = """
        SELECT (COUNT(?s) AS ?count)
        WHERE { ?s ?p ?o . }
    """
    print("Graph size after", msg, ": ", m.query(count)["count"][0])