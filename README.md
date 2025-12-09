# maplib masterclass

Woho! 💥 

Welcome to the _maplib masterclass_, in here you'll find all you need to get up to speed on **maplib**. 

### Masterclass contents
| Folder | Content |
|--------|---------|
| `data` | csvs about planets, satellites and stars |
| `notebook` | the masterclass in a jupyter notebook |
| `queries` | a few SPARQL queries |
| `slides` | the PDF version of the masterclass |
| `tpl` | st[OTTR](https://ottr.xyz/) template for planet and satellites |
| `ttl` | all RDF turtle files (ontology, shapes, output, validation report), including datalog rules |

* `utils.py` contains helper functions as `print_count(msg: str, Model)` and `write_output(Model, output_file: str)`.
* `parse_data.py` contains static variables for namespaces and functions for data engineering with data frames for instance data.
* `main.py` where the magic happens ✨ --- maplib knowledge graph construction, including querying, validation and reasoning.

### Resources
* [Tutorial documentation](https://datatreehouse.github.io/documentation/#/page/maplib%20docs)
* [maplib API documentation](https://datatreehouse.github.io/maplib/maplib.html)
* [OTTR masterclass](https://github.com/veleda/ottr-masterclass)
