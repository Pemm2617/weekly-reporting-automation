import pandas as pd
import numpy as np
import os

# ── Generate Sample Index Files ───────────────────────────────────────────────
def generate_index_file(index_name, num_constituents=20):
    np.random.seed(42)
    data = {
        "Security_ID":      [f"SEC{str(i).zfill(4)}" for i in range(1, num_constituents + 1)],
        "Security_Name":    [f"Company {i} Ltd" for i in range(1, num_constituents + 1)],
        "ISIN":             [f"IN{str(i).zfill(10)}" for i in range(1, num_constituents + 1)],
        "Weight":           np.round(np.random.dirichlet(np.ones(num_constituents)) * 100, 4),
        "Market_Cap":       np.round(np.random.uniform(1000, 50000, num_constituents), 2),
        "Close_Price":      np.round(np.random.uniform(100, 5000, num_constituents), 2),
        "Daily_Return_Pct": np.round(np.random.uniform(-3, 3, num_constituents), 4),
        "Sector":           np.random.choice(["Technology", "Finance", "Energy", "Healthcare", "Consumer"], num_constituents),
        "Country":          np.random.choice(["India", "Japan", "Australia", "Singapore"], num_constituents),
    }
    return pd.DataFrame(data)

os.makedirs("sample_input_files", exist_ok=True)

df1 = generate_index_file("APAC_TECH_INDEX")
df1.to_csv("sample_input_files/APAC_TECH_INDEX_Wednesday.csv", index=False)

df2 = generate_index_file("APAC_FINANCE_INDEX")
df2.to_csv("sample_input_files/APAC_FINANCE_INDEX_Wednesday.csv", index=False)

df3 = generate_index_file("CEEMEA_ENERGY_INDEX")
df3.to_csv("sample_input_files/CEEMEA_ENERGY_INDEX_Friday.csv", index=False)

df4 = generate_index_file("CEEMEA_CONSUMER_INDEX")
df4.to_csv("sample_input_files/CEEMEA_CONSUMER_INDEX_Friday.csv", index=False)

print("Sample input files generated successfully.")
