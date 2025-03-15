import pandas as pd
import json

# df = pd.read_csv("board_games.csv")
df = pd.read_csv("mehreens.csv")
print(df.head())  # Check structure

# Convert to dictionary format suitable for JavaScript
graph_data = {
    "nodes": [{"id": game} for game in set(df["source"]).union(set(df["target"]))],
    "links": [
        {"source": row["source"], "target": row["target"], "value": row["value"]}
        for _, row in df.iterrows()
    ],
}

# Save as JavaScript file
with open("mehreens.js", "w") as f:
    f.write(f"const graphData = {json.dumps(graph_data, indent=2)};")
