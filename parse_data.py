import polars as pl
pl.Config.set_fmt_str_lengths(150)


ns = "http://data.treehouse.example/"
ns_tpl = "http://data.treehouse.example/tpl/"
ns_sh = "http://data.treehouse.example/sh/"

# DATA FROM: https://github.com/devstronomy/nasa-data-scraper/tree/master
# STARS: https://www.kaggle.com/datasets/waqi786/stars-dataset/data

def planets():

    # Read planet CSV
    df_planets = pl.read_csv("data/planets.csv")

    # Create subject URI for planets
    df_planets = df_planets.with_columns(
        (pl.lit(ns) + pl.col("planet")).alias("planet_uri")
        )

    # Chose columns to play with
    df_planets = df_planets.select(
        ["planet", 
        "planet_uri", 
        "mean_temperature",
        "length_of_day",
        "orbital_period"
        ])
    
    return df_planets


def satellites():
    
    df_satellites = pl.read_csv("data/satellites.csv")
    df_satellites = df_satellites.with_columns(
        (pl.lit(ns) + pl.col("planet")).alias("planet_uri")
    )
    df_satellites = df_satellites.with_columns(
        (pl.lit(ns) + pl.col("name")
        .str.replace_all("/", "-"))
        .str.replace_all(" ", "-")
        .alias("satellite_uri")
    )
    df_satellites = df_satellites.select(
        ["name", "planet_uri", "satellite_uri", "albedo", "radius"]
        )
    
    return df_satellites

def stars():
    df_stars = pl.read_csv("data/stars.csv")
    return df_stars