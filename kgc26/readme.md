# Fantasy & Sci-Fi Knowledge Graph--a maplib masterclass

A 1.5-hour walkthrough of the [maplib](https://github.com/DataTreehouse/maplib) pipeline, built around a small dataset of books, authors, series, and adaptations from fantasy and science fiction.

Presented at KGC 2026.

## What's in here

The masterclass takes four messy data files (a Parquet, three CSVs) and turns them into a single in-memory knowledge graph: aligned to a common ontology, enriched with vocabularies linked through SKOS, sources catalogued with DCAT, validated with SHACL, and reasoned over with both Datalog and SPARQL CONSTRUCT rules.

The whole pipeline is a maplib RDF `Model()` plus a handful of method calls.

```
masterclass-creative-works/
├── masterclass.ipynb        # 🎯 the notebook to follow along with
├── data/
│   ├── authors.parquet      # master data, lakehouse-style
│   ├── series.csv           # editorial catalog
│   ├── books.csv            # the catalog itself
│   └── adaptations.csv      # films, TV, radio, animation
├── tpl/
│   └── tpl.stottr           # OTTR templates: Author, Series, Book, NextInSeriesLink, Adaptation
├── ttl/
│   ├── ontology.ttl         # OWL classes & properties (aligned to BIBO + Schema.org)
│   ├── vocab.ttl            # SKOS schemes: Genre, Era, AdaptationType
│   ├── catalog.ttl          # DCAT description of the data sources
│   ├── sh.ttl               # SHACL shapes (incl. ISBN-13 regex)
│   └── rule.dlog            # Datalog inference rules
├── queries/
│   ├── skos updates/        # SPARQL UPDATEs that swap string literals for SKOS concept IRIs
│   ├── infer queries/       # SPARQL CONSTRUCT inference rules (the recursive :readingOrder one)
│   └── *.rq                 # exploration & verification queries
├── data_engineering.py      # Polars pipeline, one function per source
├── knowledge_engineering.py # the same masterclass as a script
├── utils.py                 # tiny helper for graph-size readouts
└── README.md
```

## How to run

```bash
pip install maplib 
jupyter notebook masterclass.ipynb
```

Run top-to-bottom, or use it as a reference and jump to a section. There's also `knowledge_engineering.py` if you'd rather see the whole pipeline as a single script.



## Notes on the licensed parts

`m.infer()` and `m.validate()` are part of the maplib enterprise add-on. They're free for academics and personal exploration. Reach out to the Data Treehouse team for more information.

## Going further

For a more substantial example of the same pipeline applied to a CRM domain (Parquet, Excel, CSV, and SQL sources), see [veleda/data-engineering-to-knowledge-engineering](https://github.com/veleda/data-engineering-to-knowledge-engineering).

## Credits

Data is fictional but draws on real books by J.R.R. Tolkien, Terry Pratchett, Isaac Asimov, Frank Herbert, Ursula K. Le Guin, and Douglas Adams.

Built with [maplib](https://github.com/DataTreehouse/maplib) and [Polars](https://pola.rs/).