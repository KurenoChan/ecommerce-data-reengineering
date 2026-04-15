import pandas as pd
import numpy as np
import re

from src.scripts.profiling import dataset_summary, inconsistency_summary
from src.scripts.completeness import (
    completeness_summary, completeness_report,
    fix_title_completeness, 
    fix_email_completeness, 
    fix_amount_completeness, 
    fix_dog_size_completeness,
    fix_dog_gender_completeness, 
    fix_dog_age_completeness
)
from src.scripts.consistency import (
    inconsistency_summary, inconsistency_report,
    fix_title_consistency, 
    fix_email_consistency, 
    fix_amount_consistency, 
    fix_dog_size_consistency,
    fix_dog_gender_consistency, 
    fix_dog_age_consistency 
)
from src.scripts.duplicates import (
    duplicate_summary, duplicate_report,
    remove_duplicates
)
from src.utils.helpers import (
    normalize_missing,
    drop_noise_columns,
    show_step_changes,
    show_duplicate_removal,
)

# =========================================================
# 7. LOAD DATA
# =========================================================
print("\n************************************")
print("*** START DATA CLEANING PIPELINE ***")
print("************************************")

df = pd.read_csv("data/raw/dog_survey.csv", dtype=str, keep_default_na=False)

df.columns = df.columns.str.strip().str.lower()

df = drop_noise_columns(df)
df = normalize_missing(df)

df_before = df.copy()


# =========================================================
# 8. BEFORE CLEANING REPORTS
# =========================================================
print("\n==============================")
print("PHASE 1: DATA QUALITY CHECK")
print("==============================")

print("\n--- INCOMPLETENESS ---")
completeness_report(df_before, "RAW DATA")

print("\n--- INCONSISTENCIES ---")
summary_before, mask_before = inconsistency_summary(df_before)
inconsistency_report(df_before, "RAW DATA")

print("\n--- DUPLICATES ---")
dup_summary_before, dup_rows_before, dup_groups_before = duplicate_summary(df_before)
duplicate_report(df_before, "RAW DATA")

# issue_samples = {k: v.head(5) for k, v in issues_before.items()}


# =========================================================
# 9. CLEANING PIPELINE
# =========================================================
print("\n\n==============================")
print("PHASE 2: DATA CLEANING")
print("==============================")

df_before_step = df.copy()
total_changes = {}

# DUPLICATES
print("\n[STEP] duplicate removal")
before = df.copy()
df, removed = remove_duplicates(df)
total_changes["duplicates_removed"] = show_duplicate_removal(before, df)


# TITLE
print("\n[STEP] title cleaning")
before = df.copy()
df = fix_title_completeness(df)
df = fix_title_consistency(df)
total_changes["title"] = show_step_changes(
    "Title Cleaning", before, df, focus_cols=["title"]
)

# EMAIL
print("\n[STEP] email cleaning")
before = df.copy()
df = fix_email_completeness(df)
df = fix_email_consistency(df)
total_changes["email"] = show_step_changes(
    "Email Cleaning", before, df, focus_cols=["email"]
)

# AMOUNT
print("\n[STEP] amount cleaning")
before = df.copy()
df = fix_amount_completeness(df)
df = fix_amount_consistency(df)
total_changes["amount"] = show_step_changes(
    "Amount Fix", before, df, focus_cols=["amount_spent_on_dog_food"]
)

print("\n[STEP] dog_size cleaning")
before = df.copy()
df = fix_dog_size_completeness(df)
df = fix_dog_size_consistency(df)
total_changes["dog_size"] = show_step_changes(
    "Dog Size Fix", before, df, focus_cols=["dog_size"]
)


# DOG GENDER
print("\n[STEP] dog_gender cleaning")
before = df.copy()
df = fix_dog_gender_completeness(df)
df = fix_dog_gender_consistency(df)
total_changes["dog_gender"] = show_step_changes(
    "Dog Gender Cleaning", before, df, focus_cols=["dog_gender"]
)


# DOG AGE
print("\n[STEP] dog_age cleaning")
before = df.copy()
df = fix_dog_age_completeness(df)
df = fix_dog_age_consistency(df)
total_changes["dog_age"] = show_step_changes(
    "Dog Age Cleaning", before, df, focus_cols=["dog_age"]
)


print("\n\n=== STEP IMPACT SUMMARY ===")
summary_df = pd.DataFrame(
    list(total_changes.items()), columns=["Step", "Modified Rows"]
).sort_values("Modified Rows", ascending=False)
print(summary_df)
print(f"\nTotal modifications across pipeline: {summary_df['Modified Rows'].sum()}")


# =========================================================
# 10. AFTER CLEANING REPORTS
# =========================================================
print("\n\n==============================")
print("PHASE 3: POST-CLEANING REPORT")
print("==============================")

print("\n--- DATASET SUMMARY ---")
print(dataset_summary(df_before, "Before Cleaning"))
print()
print(dataset_summary(df, "After Cleaning"))

# 1. Completeness
print("\n--- COMPLETENESS (POST-CLEANING) ---")
completeness_report(df, "CLEANED DATA")
print("\n--- COMPLETENESS SUMMARY (FINAL) ---")
print(completeness_summary(df))

# 2. Inconsistencies (IMPORTANT FIX)
print("\n--- INCONSISTENCIES (POST-CLEANING) ---")
summary_after, mask_after = inconsistency_summary(df)
inconsistency_report(df, "CLEANED DATA")
summary_before, _ = inconsistency_summary(df_before)
summary_after, _ = inconsistency_summary(df)

print("\n--- INCONSISTENCY REDUCTION SUMMARY ---")
print((summary_before - summary_after).fillna(0))

# 3. Duplicates (recompute properly)
print("\n--- DUPLICATES (POST-CLEANING) ---")
dup_summary_after, dup_rows_after, dup_groups_after = duplicate_summary(df)
duplicate_report(df, "CLEANED DATA")

print("\n--- DUPLICATE REDUCTION SUMMARY ---")
print(pd.DataFrame({
    "Before": dup_summary_before["duplicate_count"],
    "After": dup_summary_after["duplicate_count"],
    "Reduced": dup_summary_before["duplicate_count"] - dup_summary_after["duplicate_count"]
}))

# 4. Summary comparison
print("\n--- FINAL SUMMARY ---")
print(f"Original rows: {len(df_before)}")
print(f"Final rows: {len(df)}")
print(f"Rows removed (net): {len(df_before) - len(df)}")

print(f"\nDuplicates before: {dup_summary_before['duplicate_count'].iloc[0]}")
print(f"Duplicates after: {dup_summary_after['duplicate_count'].iloc[0]}")

print(f"\nTotal missing (before): {df_before.isna().sum().sum()}")
print(f"Total missing (after): {df.isna().sum().sum()}")

if "title" in df.columns:
    print(f"\nTitle distribution:")
    print(df["title"].value_counts().head(10))

# =========================================================
# 11. EXPORT
# =========================================================
df.to_csv("data/processed/dog_survey_cleaned.csv", index=False)

print("\nCleaned dataset saved as: [dog_survey_cleaned.csv]\n")
print("================================")
print("DATA CLEANING PIPELINE COMPLETED")
print("================================\n")