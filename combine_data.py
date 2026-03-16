import pandas as pd

snupit = pd.read_csv("snupit_leads.csv")
cylex = pd.read_csv("cylex_leads.csv")
maps = pd.read_csv("maps_leads.csv")

all_leads = pd.concat([snupit, cylex, maps])

all_leads.drop_duplicates(subset="name", inplace=True)

all_leads.to_csv("leads.csv", index=False)

print("Combined leads saved to leads.csv")