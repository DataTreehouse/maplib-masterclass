# maplib masterclass

Materials from two iterations of a [maplib](https://github.com/DataTreehouse/maplib) masterclass: building knowledge graphs from tabular data using Polars and OTTR templates.

## Contents

### [`cdl25/`](./cdl25) Connected Data London 2025
The original masterclass, using a dataset of planets and their satellites.

### [`kgc26/`](./kgc26) Knowledge Graph Conference 2026
An updated and expanded version. Uses a dataset of fantasy and science fiction books and adds SPARQL CONSTRUCT inference (with recursion and arithmetic), SHACL validation, SKOS vocabularies, and DCAT cataloguing.

Each folder is self-contained, with its own README and run instructions.

## Going deeper: the article series

For a more thorough treatment of the same ideas, aimed squarely at data engineers, see the Substack series **From Data Engineering to Knowledge Engineering**:

- **Part 0** — [Why should you care about Knowledge Graphs](https://substack.com/home/post/p-188465277)
- **Part 1** — [From Data Engineering to Knowledge Engineering](https://veronahe.substack.com/p/from-data-engineering-to-knowledge)
- **Part 2** — [Data Engineering Ontologies](https://substack.com/home/post/p-184015627)
- **Part 3** — [SPARQL for SQL Developers](https://veronahe.substack.com/p/sparql-for-sql-developers-a-translation)
- **Part 4** — [From SQL Constraints to SHACL Shapes](https://substack.com/@veronahe/p-185832762)
- **Part 5** — [Putting it all together](https://substack.com/@veronahe/p-191015846)

The series has a companion code repository: [veleda/data-engineering-to-knowledge-engineering](https://github.com/veleda/data-engineering-to-knowledge-engineering) with a richer CRM-domain pipeline that handles Parquet, Excel, CSV, and SQL sources side by side.
