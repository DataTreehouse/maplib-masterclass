import polars as pl
pl.Config.set_fmt_str_lengths(150)

from maplib import Model
from maplib import explore
from maplib import IRI
from utils import write_output

import parse_data as data


# Serialise data frame to RDF using OTTR templates
with open("tpl/tpl-planets.ttl", "r") as file:
    tpl = file.read()


m = Model()
m.add_template(tpl)

# Show default templateing
# tmp_tpl = m.expand_default(df_planets, "planet_uri")
# print(tmp_tpl)


m.map(data.ns_tpl + "Planet", data.planets())
m.map(data.ns_tpl + "Satellite", data.satellites())


######################################## STARS

df_stars = pl.read_csv("data/stars.csv")
print(df_stars.columns)

######################################## RULES

with open("ttl/rule.dl", "r") as file:
    rules = file.read()

m.infer(rules)

####################################### MERGE IN ONTOLOGY

m.read("ttl/ast.ttl")


####################################### VALIDATION

m.read("ttl/sh.ttl", graph=data.ns_sh)
report = m.validate(shape_graph=data.ns_sh)
#print(report.results())


write_output(m, "ttl/out.ttl")