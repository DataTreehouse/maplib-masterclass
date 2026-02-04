from maplib import Model
from maplib import explore
from utils import print_count

import parse_data as data
import time



# Serialise data frame to RDF using OTTR template for planets
with open("tpl/tpl.stottr", "r") as file:
    tpl = file.read()

m = Model()
m.add_template(tpl)

# Kick-start building templates with expand_default
#tmp_tpl = m.map_default(data.planets(), "planet_uri")
#print(tmp_tpl)

m.map(data.ns_tpl + "Planet", data.planets())
m.map(data.ns_tpl + "Satellite", data.satellites())

#print_count("mapping", m)


####################################### MERGE IN ONTOLOGY

#m.read("ttl/ast.ttl")
#print_count("merge with ontology", m)

# Note to self: validate

####################################### INSERT

with open("queries/insert_planets_to_solar_system.rq", "r") as file:
    insert_planets_to_solar_system = file.read()

#m.insert(insert_planets_to_solar_system)

with open("queries/insert_individual.rq", "r") as file:
    insert_individual = file.read()

#m.update(insert_individual)

#print_count("insert queries", m)


####################################### RULES


with open("ttl/rule.dlog", "r") as file:
    rules = file.read()

#m.infer(rules)
#print_count("inference", m)


####################################### VALIDATION

#m.read("ttl/sh.ttl", graph=data.ns_sh)
#report = m.validate(shape_graph=data.ns_sh, include_shape_graph=False)

#write_output(report.graph(), "ttl/report.ttl")

#print_count("validation report", report.graph())

#print(report.performance)

with open("queries/focus_node_violations.rq", "r") as file:
    focus_node_violations = file.read()

#print(report.graph().query(focus_node_violations)["focusNode"])

####################################### EXPLORE

#explore(m)
#time.sleep(222)

####################################### WRITE TO FILE

m.write("out.ttl", format="turtle")

