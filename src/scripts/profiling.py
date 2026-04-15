import pandas as pd

# -------------------------
# DATASET SUMMARY
# -------------------------


def dataset_summary(df, name):
    return pd.DataFrame([{
        "Dataset": name,
        "Rows": len(df),
        "Columns": df.shape[1],
        "Missing Values": df.isna().sum().sum(),
        "Duplicates": df.duplicated().sum()
    }])


# -------------------------
# INCONSISTENCY DETECTION
# -------------------------


def dog_size_issues(df):
    valid = {"Small", "Medium", "Large", "Extra Large", "Extra Small", "Unknown"}
    return df[~df["dog_size"].isin(valid)]


def dog_gender_issues(df):
    valid = {"Male", "Female", "Unknown"}
    return df[~df["dog_gender"].isin(valid)]


def dog_age_issues(df):
    return df[df["dog_age"].isna()]


def amount_issues(df):
    return df[df["amount_spent_on_dog_food"].isna()]


def email_issues(df):
    return df[~df["email"].str.contains(r"^[^@]+@[^@]+\.[^@]+$", na=False)]


# -------------------------
# SUMMARY REPORT
# -------------------------


def inconsistency_summary(before, after):

    results = []

    checks = {
        "dog_size": dog_size_issues,
        "dog_gender": dog_gender_issues,
        "dog_age": dog_age_issues,
        "amount": amount_issues,
        "email": email_issues
    }

    for name, func in checks.items():
        b = func(before)
        a = func(after)

        results.append({
            "Issue": name,
            "Before": len(b),
            "After": len(a),
            "Fixed": len(b) - len(a)
        })

    return pd.DataFrame(results)
