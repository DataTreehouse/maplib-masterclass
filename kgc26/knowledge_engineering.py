from maplib import Model
from utils import print_count

import data_engineering as data
import time

# init and load OTTR templates
m = Model()
m.add_template(open("tpl/tpl.stottr").read())

# Kick-start building templates with map_default
#tmp_tpl = m.map_default(data.authors(), "author_iri")
#print(tmp_tpl)

m.map(data.ns_tpl + "Author",            data.authors())
m.map(data.ns_tpl + "Series",            data.series())
m.map(data.ns_tpl + "Book",              data.books())
m.map(data.ns_tpl + "NextInSeriesLink",  data.next_in_series())
m.map(data.ns_tpl + "Adaptation",        data.adaptations())

print_count("mapping", m)


####################################### MERGE IN ONTOLOGY

m.read("ttl/ontology.ttl")
print_count("merge with ontology", m)


####################################### MERGE SKOS VOCABULARIES & DCAT CATALOG

m.read("ttl/vocab.ttl")
print_count("merge with SKOS vocabularies", m)

m.read("ttl/catalog.ttl")
print_count("merge with DCAT catalog", m)


####################################### LINK INSTANCES TO SKOS CONCEPTS

skos_queries = [
    "queries/skos updates/link_genres_to_skos.rq",            # Book -> SKOS genre
    "queries/skos updates/link_eras_to_skos.rq",              # Author -> SKOS era
    "queries/skos updates/link_adaptation_types_to_skos.rq",  # Adaptation -> SKOS type
]

for qf in skos_queries:
    with open(qf, "r") as file:
        m.update(file.read())

print_count("SKOS concept linking", m)


####################################### RULES

# NB! Both m.infer() and m.validate() are functions of maplib enterprise.
# However, personal exploration is always free. Reach out to get a license.



m.infer(open("ttl/rule.dlog").read())
m.infer(open("queries/infer queries/reading_order.rq").read())
print_count("inference", m)

####################################### VALIDATION

m.read("ttl/sh.ttl")
report = m.validate(report_graph="urn:report")

#df = report.results()
#print(df)

#print(report.performance)

with open("queries/focus_node_violations.rq", "r") as file:
    focus_node_violations = file.read()

print(m.query(focus_node_violations, graph="urn:report"))


####################################### SOME FUN QUERIES

print("\n--- Books by author ---")
print(m.query(open("queries/books_by_author.rq").read()))

print("\n--- Series book counts ---")
print(m.query(open("queries/series_book_count.rq").read()))

print("\n--- :nextInSeries chains ---")
print(m.query(open("queries/next_in_series_chain.rq").read()))

print("\n--- Adaptations and the authors they were inspired by ---")
print(m.query(open("queries/adaptations_with_authors.rq").read()))

print("\n--- Books that have been adapted ---")
print(m.query(open("queries/adapted_books.rq").read()))


####################################### EXPLORE

# Run the Treehouse explorer
#m.explore(port="1234")
#time.sleep(222)


####################################### WRITE TO FILE

p = {
    "":           "http://data.treehouse.example/",
    "author":     "http://data.treehouse.example/author/",
    "book":       "http://data.treehouse.example/book/",
    "series":     "http://data.treehouse.example/series/",
    "adaptation": "http://data.treehouse.example/adaptation/",
    "country":    "http://data.treehouse.example/country/",
}
m.write("ttl/out.ttl", format="turtle", prefixes=p)
