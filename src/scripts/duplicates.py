import pandas as pd


def duplicate_summary(df: pd.DataFrame):
    dup_mask = df.duplicated(keep=False)

    dup = df[dup_mask]

    if dup.empty:
        return pd.DataFrame({
            "duplicate_count": [0],
            "duplicate_percentage": [0.0]
        }), dup, pd.DataFrame()

    summary = pd.DataFrame({
        "duplicate_count": [len(dup)],
        "duplicate_percentage": [round(len(dup) / len(df) * 100, 2)]
    })

    grouped = (
        dup.groupby(list(df.columns), dropna=False)
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    return summary, dup, grouped


def duplicate_report(df: pd.DataFrame, name: str = "DATASET", show_samples=True):
    summary, dup, grouped = duplicate_summary(df)

    print(f"\n=== DUPLICATE REPORT: {name} ===")
    print(f"Rows: {len(df)}")

    print("\n--- SUMMARY ---")
    print(summary)

    if dup.empty:
        print("\nNo duplicates found.")
        return summary

    print("\n--- DUPLICATE SAMPLE ROWS ---")
    print(dup.head(5))

    print("\n--- GROUPED DUPLICATES (TOP 10) ---")
    print(grouped.head(10))

    return summary




def remove_duplicates(df):
    df = df.copy()

    before = df[df.duplicated(keep=False)]
    after = df.drop_duplicates()

    return after, before