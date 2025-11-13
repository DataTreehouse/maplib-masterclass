- This page serves as a draft for #maplib documentation.
- Update #[[maplib terminology]] as I go.
- I need help with: 
  * sprout
- Extra documentation/tutorials to go with this;
  collapsed:: true
	- OTTR
	- Sem.tech. stack
	- SHACL
	- Datalog
- ## OTTR Templates
	- Note to self: This needs an explaination in the documentation. Since the documentation provided at [ottr.xyz](https://ottr.xyz) is way too poor.
	- OTTR Templates are written in a syntax called stOTTR. It provides a list of input parameters, and instructions on how to serialise. The instructions are other template signatures. The most used instruction is `ottr:Triple`.
	- ```stottr
	  @prefix : <http://data.treehouse.example/> .
	  @prefix tpl: <http://data.treehouse.example/tpl/> .
	  @prefix ottr: <http://ns.ottr.xyz/0.4/> .
	  @prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
	  @prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
	  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	  @prefix owl: <http://www.w3.org/2002/07/owl#> .
	  
	  tpl:Planet[ 
	      ! ottr:IRI ?planet_uri,
	      xsd:string ?planet,
	      xsd:long ?mean_temperature,
	      xsd:double ?length_of_day,
	      xsd:double ?orbital_period
	   ] :: {
	      ottr:Triple(?planet_uri, rdf:type, :Planet), 
	      ottr:Triple(?planet_uri, rdfs:label, ?planet),
	      ottr:Triple(?planet_uri, :meanTemperature, ?mean_temperature),
	      ottr:Triple(?planet_uri, :lengthOfDay, ?length_of_day),
	      ottr:Triple(?planet_uri, :orbitalPeriod, ?orbital_period)
	  } .
	  
	  ```
	  First there is a list of declared namespaces in use in the template.
	  Then follow the template header `tpl:Planet`, and its list of input parameters in square brackets (`[ ]`). Further is the sytax `::` followed by the block of serialisation instructions (`{ }`). In this case, we have five instructions on serialising the input parameters intro RDF triples.
- ## Model
  collapsed:: true
	- Mapping serves like a RDF model. It supports OTTR mappings, SPARQL and SHACL among other functions.
	- ```python
	  from maplib import Model
	  ```
	- `Mapping` takes in one or more OTTR templates, and an optional indexing of these.
- ### Creating a Model
	- ```python
	  m = Model()
	  ```
	  Loads a template into a `Model` variable. Triple count at this stage is 0. The parameter `tpl` needs to be a string.
	- ```python
	  with open("tpl.ttl", "r") as file:
	    tpl = file.read()
	  
	  m.add_template(tpl)
	  ```
- ### Map a data frame to RDF using a template
	- To serialize instance data into RDF using Model, one have to use the function `m.map(tpl, data)`, where the data is given as a data frame.
	- ```python
	  m.expand("http://data.treehouse.example/tpl/Planet", df_planet)
	  ```
	- It is important that the template signature parameters are corresponding to the data frame column headers. Example data frame that corresponds to `tpl:Planet`.
	  ```python
	  df_planet = pl.DataFrame({
	    "planet_uri":[ns + "Mars", ns + "Saturn"],
	    "planet":["Mars", "Saturn"],
	    "mean_temperature":["-65", "-140"],
	    "length_of_day":["24.7", "10.7"],
	    "orbital_period":["687.0", "10747.0"]
	  })
	  ```
	- After mapping, the Model instance `m` contains the serialised triples. The RDF Turtle for `m` is the following. 
	  ```turtle
	  @prefix dt: <http://data.treehouse.example/> .
	  @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	  
	  dt:Mars a dt:Planet ;
	      rdfs:label "Mars" ;
	      dt:lengthOfDay 24.7 ;
	      dt:meanTemperature "-65"^^xsd:long ;
	      dt:orbitalPeriod 687.0 .
	  
	  dt:Saturn a dt:Planet ;
	      rdfs:label "Saturn" ;
	      dt:lengthOfDay 10.7 ;
	      dt:meanTemperature "-140"^^xsd:long ;
	      dt:orbitalPeriod 10747.0 .
	  ```
- ### Adding another template stored in a separate file
	- One can add another triple by using `m.add_template(tpl)`, where `tpl` is a string that contains the new template.
	  ```python
	  with open("tpl/tpl-satellite.ttl", "r") as file:
	      tpl_satellite = file.read()
	  
	  m.add_template(tpl_satellite)
	  ```
	- ```stottr
	  @prefix : <http://data.treehouse.example/> .
	  @prefix tpl: <http://data.treehouse.example/tpl/> .
	  @prefix ottr: <http://ns.ottr.xyz/0.4/> .
	  @prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
	  @prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
	  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	  @prefix owl: <http://www.w3.org/2002/07/owl#> .
	  
	  
	  tpl:Satellite[ 
	      ottr:IRI ?planet_uri,
	      ! ottr:IRI ?satellite_uri,
	      xsd:string ?name,
	      ? ?albedo, 
	      ? ?radius
	   ] :: {
	      ottr:Triple(?satellite_uri, rdf:type, :NaturalSatellite), 
	      ottr:Triple(?satellite_uri, :orbits, ?planet_uri), 
	      ottr:Triple(?satellite_uri, rdfs:label, ?name),
	      ottr:Triple(?satellite_uri, :albedo, ?albedo), 
	      ottr:Triple(?satellite_uri, :radius, ?radius)
	  } .
	  ```
	  The new template contains information about the Artist, as name and genre.
	- One can then add data as a data frame and expand as in the previous example. 
	  ```python
	  # Reading satellite data from csv
	  df_satellites = pl.read_csv("data/satellites.csv")
	  
	  m.map(ns + "tpl/Satellite", df_satellite)
	  ```
	- The RDF Turtle is now appended with information about natural satellites.
	  ```turtle
	  ...
	  dt:Deimos a dt:NaturalSatellite ;
	      rdfs:label "Deimos" ;
	      dt:orbits dt:Mars .
	  
	  ...
	  
	  dt:Farbauti a dt:NaturalSatellite ;
	      rdfs:label "Farbauti" ;
	      dt:albedo 4e-02 ;
	      dt:orbits dt:Saturn ;
	      dt:radius 2.5e+00 .
	  ...
	  ```
- ### Generating templates
	- If you need a kick-start in defining templates, you can generate templates based on your data frame.
	- ```python
	  tmp_tpl = m.map_default(df_planets, "planets_uri")
	  print(tmp_tpl)
	  ```
	- This function will then generate a template based on the input data frame `df_planets`, using the parameter `planet_uri` as subject URI. The resulting template is the following.
	  ```stottr
	  <urn:maplib_default:default_template_0> [
	       <http://www.w3.org/2001/XMLSchema#string> ?planet, 
	       <http://ns.ottr.xyz/0.4/IRI> ?planet_uri, 
	       <http://www.w3.org/2001/XMLSchema#long> ?mean_temperature, 
	       <http://www.w3.org/2001/XMLSchema#double> ?length_of_day, 
	       <http://www.w3.org/2001/XMLSchema#double> ?orbital_period ] :: {
	    ottr:Triple(?planet_uri, <urn:maplib_default:planet>, ?planet) ,
	    ottr:Triple(?planet_uri, <urn:maplib_default:mean_temperature>, ?mean_temperature) ,
	    ottr:Triple(?planet_uri, <urn:maplib_default:length_of_day>, ?length_of_day) ,
	    ottr:Triple(?planet_uri, <urn:maplib_default:orbital_period>, ?orbital_period)
	  } . 
	  ```
	- **Careful!** When using `m.map_default`, it will not only generate a template and store it as string in the variable, it will also expand the serialisation into your Model `m`. The serialisation will re-use data frame column headers as fragment names for properties.
- ### Query a Model
	- You can query both the data frame and the Model using #SPARQL.
	- Queries in maplib supports `SELECT`, `CONSTRUCT` and `INSERT`.
	- **NB!** Usage of `*` is still under development.
	- ```python
	  tmp_df = m.query("""SELECT DISTINCT ?s WHERE {?s ?p "Saturn" .}""")
	  print(tmp_df)
	  ```
	  In this query, we are asking for all subjects, where the object value is the literal `"Saturn"`. When we print the results, it will contain one URI. 
	  ```bash
	  shape: (1, 1)
	  ┌────────────────────────────────────────┐
	  │ s                                      │
	  │ ---                                    │
	  │ str                                    │
	  ╞════════════════════════════════════════╡
	  │ <http://data.treehouse.example/Saturn> │
	  └────────────────────────────────────────┘
	  ```
	- The result of a query is stored in a data frame.
- ### Update a Model using SPARQL INSERT
	- ```python
	  update_query = """
	  PREFIX : <http://data.treehouse.example/> 
	  PREFIX owl: <http://www.w3.org/2002/07/owl#> 
	  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	  
	  # Insert everything that has some rdf:type to anything except for owl:Class 
	  # to be rdf:type of owl:NamedIndividual
	  
	  INSERT {
	      ?s rdf:type owl:NamedIndividual .
	  } 
	  WHERE {
	    ?s rdf:type ?o .
	    FILTER(?o != owl:Class)
	  }
	  """
	  m.update(update_query)
	  ```
	- This query will add the statement `?s rdf:type owl:NamedIndividual` for all _things_ in the current mapping that has the property `rdf:type` to something that is not `owl:Class`. Example of one planet and one natural satellite:
	  ```turtle
	  dt:Mars a dt:Planet,
	          owl:NamedIndividual ;
	      rdfs:label "Mars" ;
	      dt:lengthOfDay 2.47e+01 ;
	      dt:meanTemperature "-65"^^xsd:long ;
	      dt:orbitalPeriod 6.87e+02 .
	  
	  dt:Deimos a dt:NaturalSatellite,
	          owl:NamedIndividual ;
	      rdfs:label "Deimos" ;
	      dt:orbits dt:Mars .
	  ```
- ### Insert data into a mapping using SPARQL CONSTRUCT
	- Will insert data as described in a SPARQL CONSTRUCT query.
	- ```python
	  insert_query = """
	  PREFIX : <http://data.treehouse.example/> 
	  PREFIX owl: <http://www.w3.org/2002/07/owl#> 
	  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
	  
	  # Insert the planets of the Solar System as members of the Solar System.
	  
	  CONSTRUCT {
	      :SolarSystem rdf:type :PlanetarySystem .
	      ?s :memberOf :SolarSystem .
	  } 
	  WHERE {
	    ?s rdf:type :Planet ;
	      rdfs:label ?label .
	  
	      FILTER(STR(?label) IN 
	        ("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")
	      ) 
	  }
	  """
	  m.insert(insert_query)
	  ```
	  This query will add the fact that all planets with the label listed in the filter-list will be enriched with the fact that it is also a member of the Solar System.
	- Resulting triples will then contain the following. 
	  ```turtle
	  dt:Mars a dt:Planet,
	          owl:NamedIndividual ;
	      rdfs:label "Mars" ;
	      dt:lengthOfDay 2.47e+01 ;
	      dt:meanTemperature "-65"^^xsd:long ;
	      dt:memberOf dt:SolarSystem ;
	      dt:orbitalPeriod 6.87e+02 .
	  ```
- ### Reading
	- Reading triples into your mapping instance will append the new triples onto your current knowledge graph.
	- In this example, I will read in an ontology describing my classes and properties used in the data graph.
	  ```python
	  m.read("ttl/ont.ttl")
	  ```
	- Resulting graph after this operation will now contain both my data (ABox) and my ontology (TBox).
	  An excerpt of the resulting graph is following.
- ### Writing
	- In order to write to file, you need to specify the output file and the format you want your knowledge graph to be serialised to.
	- ```python
	  m.write("ttl/out.ttl", format="turtle")
	  ```
	- The supported formats are `ntriples`, `turtle` and `rdf/xml`.
- ### Get all predicates
	- The function `get_predicate_iris()` will return a list of all property URIs from your knowledge graph as a list of IRIs.
	- ```python
	  predicates = m.get_predicate_iris()
	  for p in predicates:
	      print(p.iri)
	  ```
	  This example will return the following on the graph we have been building through this documentation. 
	  ```bash
	  /> python main.py 
	  http://www.w3.org/2000/01/rdf-schema#range
	  http://www.w3.org/2000/01/rdf-schema#label
	  http://data.eksempel.no/title
	  http://www.w3.org/2000/01/rdf-schema#domain
	  http://data.eksempel.no/artist
	  http://data.eksempel.no/name
	  http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	  http://data.eksempel.no/genre
	  ```
- ### Get a specific predicate
	- One can fetch usage of a specific property by using `m.get_predicate(iri)`.
	- ```python
	  p_iri = IRI("http://data.treehouse.example/meanTemperature")
	  p = m.get_predicate(p_iri)
	  for x in p:
	      print(x.mappings)
	  ```
	  Here we established a new variable `p_iri` where we store the specific IRI of the property we want to fetch a result for. **NB!** remember to `from maplib import IRI`.
	  The result of `m.get_predicate(p_iri)` is a `SolutionMappings`, that we have stored in the variable `p` in this case. Then we can iterate over `p`, printing out the `mappings` stored in the list. `mappings` holds data frames with the result.
	- The result of this example is the following. 
	  ```bash
	  /> python main.py 
	  shape: (9, 2)
	  ┌───────────────────────────────────────┬────────┐
	  │ subject                               ┆ object │
	  │ ---                                   ┆ ---    │
	  │ str                                   ┆ i64    │
	  ╞═══════════════════════════════════════╪════════╡
	  │ http://data.treehouse.example/Earth   ┆ 15     │
	  │ http://data.treehouse.example/Jupiter ┆ -110   │
	  │ http://data.treehouse.example/Mars    ┆ -65    │
	  │ http://data.treehouse.example/Mercury ┆ 167    │
	  │ http://data.treehouse.example/Neptune ┆ -200   │
	  │ http://data.treehouse.example/Pluto   ┆ -225   │
	  │ http://data.treehouse.example/Saturn  ┆ -140   │
	  │ http://data.treehouse.example/Uranus  ┆ -195   │
	  │ http://data.treehouse.example/Venus   ┆ 464    │
	  └───────────────────────────────────────┴────────┘
	  ```
	  We see that the usage of `:meanTemperature` is present for all of our Planets (+ Pluto).
	-
- ### Datalog rules and inference
	- Inference rules are defined using Datalog with syntax from [Oxford Semantic Technologies](https://www.oxfordsemantic.tech/blog/datalog-basics-and-rdfox).
	- ```datalog
	  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
	  PREFIX : <http://data.treehouse.example/>
	  
	  # Inverse of orbits is moon
	  [?x, :moon, ?y] :- [?y, :orbits, ?x] .
	  ```
	  This is an example of a single Datalog rule, defining a new property `:moon`. If something orbits another thing, then that other thing must be the moon of something.
	- ```python
	  with open("ttl/rule.dl", "r") as file:
	      rules = file.read()
	  
	  m.infer(rules)
	  ```
	  We read our datalog file into a string, and pass this along to `m.infer()`.
	- The result of the reasoning is then added to our existing Model. In this snippet, we see `dt:moon` added for `dt:Mars`. Since `dt:Deimos` and `dt:Phobos` `dt:orbits dt:Mars`, then those two resources must be object values for `dt:moon` for `dt:Mars`.
	  ```turtle
	  dt:Mars a dt:Planet,
	          owl:NamedIndividual ;
	      rdfs:label "Mars" ;
	      dt:lengthOfDay 2.47e+01 ;
	      dt:meanTemperature "-65"^^xsd:long ;
	      dt:memberOf dt:SolarSystem ;
	      dt:moon dt:Deimos,
	          dt:Phobos ;
	      dt:orbitalPeriod 6.87e+02 .
	  ```
	-
