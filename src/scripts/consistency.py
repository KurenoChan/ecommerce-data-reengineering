import pandas as pd
import numpy as np
import re


# -------------------------
# INCONSISTENCY REPORT
# -------------------------
# def inconsistency_report(df, name):
#     issues = {}

#     valid_size = {"Small", "Medium", "Large", "Extra Large", "Extra Small", "Unknown"}
#     valid_gender = {"Male", "Female", "Unknown"}

#     # =========================
#     # SIZE / GENDER
#     # =========================
#     issues["dog_size"] = df[
#         ~df["dog_size"].astype(str).str.strip().str.title().isin(valid_size)
#     ]

#     issues["dog_gender"] = df[
#         ~df["dog_gender"].astype(str).str.strip().str.title().isin(valid_gender)
#     ]

#     # =========================
#     # DOG AGE
#     # =========================
#     raw_age = df["dog_age"].astype(str)

#     issues["dog_age_format"] = df[
#         raw_age.str.contains(r"[^\d\.]", na=False) & raw_age.notna()
#     ]

#     # NOTE: removed range-based validation (accuracy, not consistency rule)

#     # =========================
#     # AMOUNT
#     # =========================
#     raw_amount = df["amount_spent_on_dog_food"].astype(str)

#     issues["amount_format"] = df[raw_amount.str.contains(r"[^\d\.\£,]", na=False)]

#     # NOTE: removed range-based validation (accuracy, not consistency rule)

#     # =========================
#     # EMAIL
#     # =========================
#     issues["email"] = df[
#         ~df["email"]
#         .astype(str)
#         .str.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", na=False)
#     ]

#     # =========================
#     # REPORT
#     # =========================
#     print(f"\n=== INCONSISTENCY REPORT: {name} ===")

#     total = sum(len(v) for v in issues.values())
#     print(f"Total Issues Found: {total}")

#     summary = []
#     for k, v in issues.items():
#         summary.append([k, len(v), round(len(v) / len(df) * 100, 2)])

#     print("\n--- SUMMARY TABLE ---")
#     print(pd.DataFrame(summary, columns=["Column", "Count", "Rate %"]))

#     print("\n--- FULL INCONSISTENT RECORDS ---")
#     for k, v in issues.items():
#         print("\n" + "=" * 80)
#         print(f"ISSUE CATEGORY: {k}")
#         print(f"Total rows affected: {len(v)}")
#         print("=" * 80)
#         print(v.sort_index())

#     return issues

def inconsistency_summary(df: pd.DataFrame) -> pd.DataFrame:
    valid_size = {"Small", "Medium", "Large", "Extra Large", "Extra Small", "Unknown"}
    valid_gender = {"Male", "Female", "Unknown"}

    issues = {}

    # -------------------------
    # SIZE
    # -------------------------
    size_invalid = ~df["dog_size"].astype(str).str.strip().str.title().isin(valid_size)

    # -------------------------
    # GENDER
    # -------------------------
    gender_invalid = ~df["dog_gender"].astype(str).str.strip().str.title().isin(valid_gender)

    # -------------------------
    # AGE FORMAT
    # -------------------------
    raw_age = df["dog_age"].astype(str)
    age_invalid = raw_age.str.contains(r"[^\d\.]", na=False) & raw_age.notna()

    # -------------------------
    # AMOUNT FORMAT
    # -------------------------
    raw_amount = df["amount_spent_on_dog_food"].astype(str)
    amount_invalid = raw_amount.str.contains(r"[^\d\.\£,]", na=False)

    # -------------------------
    # EMAIL FORMAT
    # -------------------------
    email_invalid = ~df["email"].astype(str).str.match(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        na=False
    )

    # -------------------------
    # BUILD SUMMARY TABLE
    # -------------------------
    result = pd.DataFrame({
        "dog_size": size_invalid,
        "dog_gender": gender_invalid,
        "dog_age_format": age_invalid,
        "amount_format": amount_invalid,
        "email": email_invalid
    })

    summary = pd.DataFrame({
        "Issue Count": result.sum(),
        "Issue %": (result.mean() * 100).round(2)
    }).sort_values("Issue Count", ascending=False)

    return summary, result

def inconsistency_report(df: pd.DataFrame, name: str, show_samples=True):
    summary, mask_df = inconsistency_summary(df)

    print(f"\n=== INCONSISTENCY REPORT: {name} ===")
    print(f"Rows: {len(df)}")

    print("\n--- SUMMARY TABLE ---")
    print(summary)

    if show_samples:
        print("\n--- SAMPLE INCONSISTENT RECORDS ---")

        for col in mask_df.columns:
            invalid_rows = df[mask_df[col]]

            if len(invalid_rows) > 0:
                print("\n" + "=" * 70)
                print(f"[{col}] ({len(invalid_rows)} rows)")
                print("=" * 70)
                print(invalid_rows.head(3))

    return summary




def fix_title_consistency(df):
    df = df.copy()

    s = df["title"].astype("string")

    s = s.str.strip().str.title()

    valid = {"Mr", "Mrs", "Ms", "Dr", "Rev", "Honorable"}

    df["title"] = s.where(s.isin(valid), "Unknown")

    return df


def fix_email_consistency(df):
    df = df.copy()

    s = df["email"].astype(str).str.strip()

    mask = ~s.str.match(r"^[^@]+@[^@]+\.[^@]+$", na=False)

    df.loc[mask, "email"] = "invalid@email.com"

    return df


def fix_amount_consistency(df):
    df = df.copy()

    s = df["amount_spent_on_dog_food"].astype(str)

    s = (
        s.str.replace("£", "", regex=False)
         .str.replace(",", "", regex=False)
         .str.strip()
    )

    s = pd.to_numeric(s, errors="coerce")

    s = s.where(s > 0, np.nan)

    df["amount_spent_on_dog_food"] = s.fillna(s.median())

    return df


def fix_dog_size_consistency(df):
    df = df.copy()

    mapping = {
        "s": "Small",
        "small": "Small",
        "smallish": "Small",
        "m": "Medium",
        "medium": "Medium",
        "medium sized": "Medium",
        "l": "Large",
        "large": "Large",
        "xl": "Extra Large",
        "xs": "Extra Small"
    }

    s = df["dog_size"].astype(str).str.lower().str.strip()
    s = s.str.split(",").str[0]

    df["dog_size"] = s.map(mapping).fillna("Unknown")

    return df


def fix_dog_gender_consistency(df):
    df = df.copy()

    s = df["dog_gender"].astype(str).str.lower().str.strip()

    s = s.str.replace(r"[^a-z, ]", "", regex=True)
    s = s.str.split(",").str[0]

    mapping = {
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female",
        "femlae": "Female",
        "unknown": "Unknown",
        "unkown": "Unknown"
    }

    df["dog_gender"] = s.map(mapping).fillna("Unknown")

    return df


def fix_dog_age_consistency(df):
    df = df.copy()

    def extract_numbers(value):
        if pd.isna(value):
            return np.nan

        nums = re.findall(r"\d+", str(value))
        nums = [int(n) for n in nums]

        if not nums:
            return np.nan

        return float(np.median(nums))

    df["dog_age"] = df["dog_age"].apply(extract_numbers)

    df.loc[df["dog_age"] <= 0, "dog_age"] = np.nan

    # imputation belongs here (consistency decision)
    median_age = df["dog_age"].median()
    df["dog_age"] = df["dog_age"].fillna(median_age)

    df["dog_age"] = df["dog_age"].round().astype(int).astype(str)

    return df