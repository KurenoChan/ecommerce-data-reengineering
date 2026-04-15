import pandas as pd
import numpy as np

def completeness_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Missing Count": df.isna().sum(),
        "Missing %": (df.isna().mean() * 100).round(2)
    }).sort_values("Missing Count", ascending=False)
    
def completeness_report(df, name, show_samples=True):
    missing_mask = df.isna()

    report = pd.DataFrame(
        {
            "Missing Count": missing_mask.sum(),
            "Missing %": (missing_mask.mean() * 100).round(2),
        }
    ).sort_values("Missing Count", ascending=False)

    print(f"\n=== COMPLETENESS REPORT: {name} ===")
    print(f"Rows: {len(df)}")
    print(report)

    if show_samples:
        print("\n--- SAMPLE ROWS WITH MISSING VALUES ---")

        for col, count in report["Missing Count"].items():
            if count > 0:
                col_missing = df[df[col].isna()]
                print(f"\n[{col}] missing examples ({len(col_missing)} rows total)")
                print(col_missing.head(3))



def fix_title_completeness(df):
    df = df.copy()

    s = df["title"].astype("string")

    s = s.replace([
        "", " ", "-", "none", "null", "nan",
        "None", "NULL", "NaN"
    ], pd.NA)

    df["title"] = s

    return df


def fix_email_completeness(df):
    df = df.copy()

    s = df["email"].astype("string")

    s = s.replace(["", " ", "null", "nan"], pd.NA)

    df["email"] = s

    return df


def fix_amount_completeness(df):
    df = df.copy()

    s = df["amount_spent_on_dog_food"].astype(str)

    s = s.replace(["", " ", "nan", "None", "null", "NULL"], np.nan)

    df["amount_spent_on_dog_food"] = s

    return df


def fix_dog_size_completeness(df):
    df = df.copy()

    df["dog_size"] = (
        df["dog_size"]
        .astype(str)
        .replace(["", " ", "nan", "None", "NULL", "null"], np.nan)
    )

    return df


def fix_dog_gender_completeness(df):
    df = df.copy()

    s = df["dog_gender"].astype("string")

    s = s.replace(["", " ", "nan", "null"], pd.NA)

    df["dog_gender"] = s

    return df


def fix_dog_age_completeness(df):
    df = df.copy()

    df["dog_age"] = df["dog_age"].replace("", np.nan)

    return df