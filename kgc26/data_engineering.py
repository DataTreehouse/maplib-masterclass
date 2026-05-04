import polars as pl
pl.Config.set_fmt_str_lengths(150)

# Namespaces
ns = "http://data.treehouse.example/"
ns_tpl = "http://data.treehouse.example/tpl/" # for OTTR templates
ns_sh = "http://data.treehouse.example/sh/"   # for SHACL shapes

###
# DATA SOURCES:
# - Authors:      Parquet   (master data, lakehouse-style)
# - Series:       CSV       (curated by editors, exchanged as flat files)
# - Books:        CSV       (the catalog, classic flat-file)
# - Adaptations:  CSV       (films, TV, radio, animation)
#
# ENTITY HARMONISATION:
# In real datasets, the same entity (a book, an author, a series) appears
# under different column names depending on who built the table:
#
#   authors.parquet     →  "author_id",        "full_name",       "birth_year"
#   books.csv           →  "book_id",          "title",           "author_ref"
#   series.csv          →  "series_id",        "series_name",     "started_year"
#   adaptations.csv     →  "adaptation_id",    "adaptation_title", "source_book_ref"
#
# The OTTR template in tpl.stottr expects ONE shared name per concept
# (e.g. always "?author_iri"), so we rename in this module before mapping.
###


def authors():

    df_authors = pl.read_parquet("data/authors.parquet")

    # harmonise
    df_authors = df_authors.rename({
        "full_name": "name",     # full_name → name (OTTR template expects "name")
    })

    # Create IRIs for each author and for their nationality (a country)
    df_authors = df_authors.with_columns(
        (ns + "author/" + pl.col("author_id")).alias("author_iri"),
        (ns + "country/" + pl.col("nationality")).alias("nationality"),
    )

    df_authors = df_authors.select([
        "name",
        "author_iri",
        "birth_year",
        "death_year",
        "nationality",
        "era",
    ])

    return df_authors


def series():

    df_series = pl.read_csv("data/series.csv")

    # Create IRI for each series
    df_series = df_series.with_columns(
        (ns + "series/" + pl.col("series_id")).alias("series_iri")
    )

    df_series = df_series.select([
        "series_name",
        "series_iri",
        "started_year",
        "status",
        "description",
    ])

    return df_series


def books():

    df_books = pl.read_csv("data/books.csv")

    # harmonise
    df_books = df_books.rename({
        "position_in_series": "position",
    })

    # Build IRIs from the *_ref columns. 
    df_books = df_books.with_columns(
        (ns + "book/"   + pl.col("book_id")).alias("book_iri"),
        (ns + "author/" + pl.col("author_ref")).alias("author_iri"),
        (ns + "series/" + pl.col("series_ref")).alias("series_iri"),
    )

    # Make sure numeric columns are the types the OTTR template expects,
    # and that ISBN stays a string (Polars infers it as int otherwise —
    # all-digit columns are tempting targets for type inference).
    df_books = df_books.with_columns(
        pl.col("position").cast(pl.Int64, strict=False),
        pl.col("publication_year").cast(pl.Int64, strict=False),
        pl.col("page_count").cast(pl.Int64, strict=False),
        pl.col("isbn").cast(pl.Utf8, strict=False),
    )

    df_books = df_books.select([
        "title",
        "book_iri",
        "author_iri",
        "series_iri",
        "position",
        "publication_year",
        "genre",
        "isbn",
    ])

    return df_books


def next_in_series():

    df = books().sort(["series_iri", "position"])

    # Add a dense rank within each series (1, 2, 3, …) — this gives us
    # a clean sequential index regardless of gaps in the source positions.
    df = df.with_columns(
        pl.col("position")
          .rank("dense")
          .over("series_iri")
          .cast(pl.Int64)
          .alias("rank"),
    )

    # The "left" side keeps the current book; the "right" side is the same
    # DataFrame, renamed so columns don't collide.
    right = df.select([
        pl.col("book_iri").alias("next_book_iri"),
        pl.col("series_iri"),
        (pl.col("rank") - 1).alias("rank"),  # join rank N -> rank N+1
    ])

    pairs = (
        df.select(["book_iri", "series_iri", "rank"])
          .join(right, on=["series_iri", "rank"], how="inner")
          .select(["book_iri", "next_book_iri"])
    )

    return pairs


def adaptations():

    df_adaptations = pl.read_csv("data/adaptations.csv")

    # Create IRIs
    df_adaptations = df_adaptations.with_columns(
        (ns + "adaptation/" + pl.col("adaptation_id")).alias("adaptation_iri"),
        (ns + "book/"       + pl.col("source_book_ref")).alias("book_iri"),
    )

    # Numeric casts
    df_adaptations = df_adaptations.with_columns(
        pl.col("release_year").cast(pl.Int64, strict=False),
        pl.col("runtime_minutes").cast(pl.Int64, strict=False),
        pl.col("imdb_rating").cast(pl.Float64, strict=False),
    )

    df_adaptations = df_adaptations.select([
        "adaptation_title",
        "adaptation_iri",
        "book_iri",
        "adaptation_type",
        "release_year",
        "director",
        "runtime_minutes",
        "imdb_rating",
    ])

    return df_adaptations

