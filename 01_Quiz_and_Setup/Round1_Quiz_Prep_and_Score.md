# Round 1: Quiz Preparation & Score Tracker

## Core Analytics Knowledge Reference

### Data Cleaning & Preprocessing Formulas (Pandas)
- **Check Nulls:** `df.isnull().sum()`
- **Fill Nulls:** `df['col'].fillna(df['col'].mode()[0], inplace=True)`
- **Drop Duplicates:** `df.drop_duplicates(inplace=True)`
- **String Normalization:** `df['col'] = df['col'].str.strip().str.title()`
- **IQR Outlier Bounds:** 
  - $Q_1 = \text{df}['col'].quantile(0.25)$
  - $Q_3 = \text{df}['col'].quantile(0.75)$
  - $IQR = Q_3 - Q_1$
  - $\text{Lower Bound} = Q_1 - 1.5 \times IQR$, $\text{Upper Bound} = Q_3 + 1.5 \times IQR$

### Core Excel Functions
- `XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])`
- `COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2])`
- `SUMIFS(sum_range, criteria_range1, criteria1)`
- `AVERAGEIFS(average_range, criteria_range1, criteria1)`

---

## Round 1 Score Log
- **Date Taken:** [YYYY-MM-DD]
- **Total Score:** ____ / 20 Marks
- **Status:** [Passed / Needs Review]