import numpy as np


def normalize_missing(df):
    df = df.copy()

    df = df.replace("", np.nan)

    return df


def drop_noise_columns(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.loc[:, ~df.columns.str.match(r"^unnamed")]
    return df


def show_step_changes(name, before_df, after_df, focus_cols=None):
    print("\n" + "=" * 90)
    print(f"[STEP REPORT] {name}")
    print("=" * 90)

    before_df = before_df.copy()
    after_df = after_df.copy()

    # -------------------------
    # 1. HANDLE ROW COUNT CHANGE
    # -------------------------
    before_ids = set(before_df["id"])
    after_ids = set(after_df["id"])

    removed_ids = before_ids - after_ids
    added_ids = after_ids - before_ids

    if removed_ids or added_ids:
        if removed_ids:
            removed = before_df[before_df["id"].isin(removed_ids)]
            print(f"Rows removed: {len(removed)}")
            print(removed.head(10))

        if added_ids:
            added = after_df[after_df["id"].isin(added_ids)]
            print(f"Rows added: {len(added)}")
            print(added.head(10))

        print("=" * 90)

        # 🚨 STOP HERE — do NOT run compare()
        return len(removed_ids)

    # -------------------------
    # 2. ALIGN DATA
    # -------------------------
    before_idx = before_df.set_index("id")
    after_idx = after_df.set_index("id")

    common_ids = before_idx.index.intersection(after_idx.index)

    before_idx = before_idx.loc[common_ids]
    after_idx = after_idx.loc[common_ids]

    # align columns strictly
    before_idx = before_idx[after_idx.columns]

    # -------------------------
    # 3. COLUMN-LEVEL DIFF
    # -------------------------
    diff = before_idx.compare(after_idx)
    diff = diff.rename(columns={"self": "before", "other": "after"}, level=1)
    
    if diff.empty:
        print("No changes detected")
        print("=" * 90)
        return 0

    # -------------------------
    # 4. OPTIONAL COLUMN FILTER
    # -------------------------
    if focus_cols:
        diff = diff.loc[:, diff.columns.get_level_values(0).isin(focus_cols)]

        if diff.empty:
            print(f"No changes detected in columns: {focus_cols}")
            print("=" * 90)
            return 0

    # -------------------------
    # 5. REPORT
    # -------------------------
    changed_rows = diff.index.nunique()

    print(f"Modified rows: {changed_rows}")

    print("\n--- SAMPLE CHANGES ---")
    print(diff.head(5))

    # -------------------------
    # 6. SUMMARY PER COLUMN
    # -------------------------
    col_counts = diff.columns.get_level_values(0).value_counts()

    print("\n--- CHANGE COUNT BY COLUMN ---")
    print(col_counts)

    print("=" * 90)

    return changed_rows


def show_duplicate_removal(before_df, after_df):
    print("\n" + "=" * 90)
    print("[STEP REPORT] Duplicate Removal")
    print("=" * 90)

    before_df = before_df.copy()

    # -------------------------
    # 1. DUPLICATES (BEFORE)
    # -------------------------
    dup = before_df[before_df.duplicated(keep=False)]

    if dup.empty:
        print("No duplicates found.")
        print("=" * 90)
        return 0

    print(f"Total duplicate rows (before): {len(dup)}")

    print("\n--- FULL DUPLICATE ROWS (BEFORE REMOVAL) ---")
    print(dup.sort_values(list(before_df.columns)).reset_index(drop=True))

    # -------------------------
    # 2. GROUPED VIEW (SUMMARY)
    # -------------------------
    grouped = (
        dup.groupby(list(before_df.columns), dropna=False)
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    print("\n--- DUPLICATE GROUP SUMMARY (FREQUENCY VIEW) ---")
    print(grouped.head(10))

    # -------------------------
    # 3. AFTER STATE INFO
    # -------------------------
    removed = len(before_df) - len(after_df)

    print(f"\nRows removed: {removed}")

    print("=" * 90)

    return removed