import pandas as pd
from math import log
import matplotlib.pyplot as plt

df = pd.read_csv("../processed_data/parlementaires_with_age.csv", index_col=0)
AGE_SPANS = [(0, 40), (40, 50), (50, 60), (60, 70), (70, 100)]
LEFT = ["VERT-E-S", "PdT", "PSS"]


def get_age_cat(age):
    for cat in AGE_SPANS:
        if age < cat[1]:
            return cat
    return False


df["age_cat"] = df["Age"].apply(get_age_cat)
df["position"] = df["party"].apply(lambda x: "left" if x in LEFT else "center/right")

rows = []
for cat, group in df.groupby("age_cat"):
    result = group["position"].value_counts().to_dict()
    rows.append(
        {
            "age span": str(cat),
            "left": result["left"],
            "center/right": result["center/right"],
        }
    )
dfr = pd.DataFrame(rows)
dfr.set_index("age span").plot(kind="bar")
plt.title('Political orientation per age span')
plt.tight_layout()
plt.savefig("../charts/how_meaningful_is_age/position_per_age_span.png")
plt.clf()

df["cat_str"] = df["age_cat"].astype(str)

df.groupby("position")["cat_str"].hist(legend=True, alpha=0.5)
plt.title("Age span distribution per political orientation")
plt.tight_layout()
plt.savefig("../charts/how_meaningful_is_age/position_cat_hist.png")
plt.clf()

df.groupby("position")["Age"].hist(legend=True, alpha=0.5)
plt.title("Age distribution per political orientation")
plt.tight_layout()
plt.savefig("../charts/how_meaningful_is_age/position_age_hist.png")
plt.clf()