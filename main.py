import polars as pl
pl.Config.set_fmt_str_lengths(150)

from maplib import Mapping
from maplib import explore
from maplib import IRI
from utils import write_output

ns = "http://data.treehouse.example/"
ns_tpl = "http://data.treehouse.example/tpl/"


# DATA FROM: https://github.com/devstronomy/nasa-data-scraper/tree/master

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


# Serialise data frame to RDF using OTTR templates
with open("tpl/tpl-planets.ttl", "r") as file:
    tpl = file.read()
m = Mapping(tpl)

# Show default templateing
# tmp_tpl = m.expand_default(df_planets, "planet_uri")
# print(tmp_tpl)

m.expand(ns_tpl + "Planet", df_planets)


########################################################### NAT.SAT.

df_satellites = pl.read_csv("data/satellites.csv")
df_satellites = df_satellites.with_columns(
    (pl.lit(ns) + pl.col("planet")).alias("planet_uri")
)
df_satellites = df_satellites.with_columns(
    (pl.lit(ns) + pl.col("name").str.replace_all("/", "-")).str.replace_all(" ", "-").alias("satellite_uri")
)
df_satellites = df_satellites.select(
    ["name", "planet_uri", "satellite_uri", "albedo", "radius"]
    )

m.expand(ns_tpl + "Satellite", df_satellites)


write_output(m, "ttl/out_merged.ttl")


######################################## RULES

with open("ttl/rule.dl", "r") as file:
    rules = file.read()

m.add_ruleset(rules)
m.infer()

write_output(m, "ttl/out_inferred.ttl")

