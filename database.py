import pandas as pd
import sqlite3


data = pd.read_csv("data.csv", names=["id", "name", "good_with", "good_against", "primary"])

create_hero = """
CREATE TABLE HEROES (
    hero_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hero_name TEXT NOT NULL,
    hero_main_attr TEXT NOT NULL,
    hero_image TEXT,
    external_hero_id INTEGER NOT NULL
);
"""

create_synergy_with = """
CREATE TABLE SYNERGY_WITH (
    syn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hero_id_1 INTEGER NOT NULL,
    hero_id_2 INTEGER NOT NULL,
);
"""

create_synergy_against = """
CREATE TABLE SYNERGY_AGAINST (
    syn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hero_id_1 INTEGER NOT NULL,
    hero_id_2 INTEGER NOT NULL,
);
"""

insert_hero = """
INSERT INTO HEROES (
    hero_name,
    hero_main_attr,
    hero_image,
    external_hero_id
) VALUES
{};
"""

insert_syn_1 = """
INSERT INTO SYNERGY_WITH (
    hero_id_1,
    hero_id_2
) VALUES
{};
"""

insert_syn_2 = """
INSERT INTO SYNERGY_AGAINST (
    hero_id_1,
    hero_id_2
) VALUES
{};
"""

insert_data = []
insert_syn_data_1 = []
insert_syn_data_2 = []

for _, row in data.iterrows():
    insert_data.append(
        "({}, {}, {}, {})".format(
            row["name"],
            row["primary"],
            "MISSING",
            row["id"]
        )
    )

    try:
        gw = row["good_with"].split("|")
    except AttributeError:
        gw = []

    for g_id in gw:
        if g_id == "nan":
            continue
        insert_syn_data_1.append("({}, {})".format(row["id"], g_id))
        insert_syn_data_1.append("({}, {})".format(g_id, row["id"]))

    try:
        ga = row["good_against"].split("|")
    except AttributeError:
        ga = []

    for g_id in ga:
        if g_id == "nan":
            continue
        insert_syn_data_2.append("({}, {})".format(row["id"], g_id))
        insert_syn_data_2.append("({}, {})".format(g_id, row["id"]))

query_0 = insert_hero.format(
    ",\n".join(insert_data)
)
query_1 = insert_syn_1.format(
    ",\n".join(insert_syn_data_1)
)
query_2 = insert_syn_2.format(
    ",\n".join(insert_syn_data_2)
)

conn = sqlite3.connect("hero_database.db")
c = conn.cursor()

c.execute(create_hero)
c.execute(create_synergy_with)
c.execute(create_synergy_against)

c.execute(query_0)
c.execute(query_1)
c.execute(query_2)

conn.commit()
conn.close()
