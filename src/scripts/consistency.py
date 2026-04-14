import pandas as pd
import numpy as np

# -------------------------
# DOG SIZE
# -------------------------
def fix_dog_size(df):
    df = df.copy()

    mapping = {
        "s": "Small",
        "smallish": "Small",
        "m": "Medium",
        "medium sized": "Medium",
        "l": "Large",
        "large": "Large",
        "xl": "Extra Large",
        "xs": "Extra Small"
    }

    s = df["dog_size"].astype(str).str.lower().str.strip()

    # handle multi-values like S,L,L
    s = s.str.split(",").str[0]

    df["dog_size"] = s.map(mapping).fillna("Unknown")

    return df


# -------------------------
# DOG GENDER
# -------------------------
def fix_dog_gender(df):
    df = df.copy()

    s = df["dog_gender"].astype(str).str.lower().str.strip()

    mapping = {
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female",
        "femlae": "Female",
        "unkown": "Unknown",
        "unknown": "Unknown",
        "don't know": "Unknown"
    }

    # handle weird combos
    s = s.str.replace(r"[^a-z, ]", "", regex=True)
    s = s.str.split(",").str[0]

    df["dog_gender"] = s.map(mapping).fillna("Unknown")

    return df


# -------------------------
# EMAIL
# -------------------------
def fix_email(df):
    df = df.copy()

    s = df["email"].astype(str).str.strip()

    mask = ~s.str.contains(r"^[^@]+@[^@]+\.[^@]+$", na=False)

    df.loc[mask, "email"] = "invalid@email.com"

    return df


# # -------------------------
# # DOG AGE
# # -------------------------
# def fix_dog_age(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()

#     if "dog_age" not in df.columns:
#         return df

#     # extract first number found
#     df["dog_age"] = (
#         df["dog_age"]
#         .astype(str)
#         .str.extract(r"(\d+)", expand=False)
#     )

#     df["dog_age"] = pd.to_numeric(df["dog_age"], errors="coerce")

#     return df


# # -------------------------
# # AMOUNT
# # -------------------------
# def fix_amount(df):
#     df = df.copy()

#     s = df["amount_spent_on_dog_food"].astype(str)

#     s = s.str.replace("£", "", regex=False)
#     s = s.str.replace(",", "")
#     s = s.str.strip()

#     df["amount_spent_on_dog_food"] = pd.to_numeric(s, errors="coerce")

#     return df