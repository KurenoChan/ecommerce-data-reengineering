import pandas as pd
import numpy as np

def completeness_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Missing Count": df.isna().sum(),
        "Missing %": (df.isna().mean() * 100).round(2)
    }).sort_values("Missing Count", ascending=False)
    
    