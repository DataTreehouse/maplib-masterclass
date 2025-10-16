from maplib import Model
from maplib import explore
from maplib import IRI
from utils import write_output
from utils import print_count


import parse_data as data


# Serialise data frame to RDF using OTTR template for planets
with open("tpl/tpl.ttl", "r") as file:
    tpl = file.read()

m = Model()
m.add_template(tpl)

# Kick-start building templates with expand_default
# tmp_tpl = m.expand_default(data.planets(), "planet_uri")
# print(tmp_tpl)


m.map(data.ns_tpl + "Planet", data.planets())
m.map(data.ns_tpl + "Satellite", data.satellites())


print_count("mapping", m)

###########
## Rules ##
########### 

with open("ttl/rule.dlog", "r") as file:
    rules = file.read()

m.infer(rules)

print_count("inference", m)

####################################### MERGE IN ONTOLOGY

m.read("ttl/ast.ttl")

####################################### VALIDATION

m.read("ttl/sh.ttl", graph=data.ns_sh)
report = m.validate(shape_graph=data.ns_sh)

write_output(report.graph(), "ttl/report.ttl")


write_output(m, "ttl/out.ttl")