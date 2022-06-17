from kloppy import datasets
import pandas as pd
dataset = datasets.load("wyscout", match_id=2499843)
dataset = dataset.to_pandas()
print(pd.read_json('teams.json').to_csv('temp.csv'))