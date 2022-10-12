from src.griddingmachine import update_GM, query_collection
import pandas as pd
import numpy as np

update_GM()

COMBOS = [
    "TROPOMI_740_12X_8D_2018_V1",
    "TROPOMI_740DC_12X_8D_2018_V1",
    "TROPOMI_740_12X_8D_2019_V1",
    "TROPOMI_740DC_12X_8D_2019_V1",
    "TROPOMI_740_12X_8D_2020_V1",
    "TROPOMI_740DC_12X_8D_2020_V1",
    "TROPOMI_740_12X_8D_2021_V1",
    "TROPOMI_740DC_12X_8D_2021_V1",
    "TROPOMI_683_5X_8D_2018_V2",
    "TROPOMI_683DC_5X_8D_2018_V2",
    "TROPOMI_683_5X_8D_2019_V2",
    "TROPOMI_683DC_5X_8D_2019_V2",
    "TROPOMI_683_5X_8D_2020_V2",
    "TROPOMI_683DC_5X_8D_2020_V2"
]

COMBOS = ["SIF_" + COMBO for COMBO in COMBOS]

paths = []

for COMBO in COMBOS:
    path = query_collection(COMBO)
    paths.append(path)
    
df = pd.DataFrame({
    "combo": COMBOS,
    "path": paths
})