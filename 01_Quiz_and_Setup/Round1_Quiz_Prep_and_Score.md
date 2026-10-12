# Round 1: Quiz Preparation Cheat Sheet & Score Tracker

## 1. Data Cleaning & Preprocessing (Pandas & NumPy)

### Core Inspection Functions
- **Check Dataset Overview:** `df.info()`
- **Summary Statistics:** `df.describe()`
- **Missing Value Count:** `df.isnull().sum()`
- **Check Duplicates:** `df.duplicated().sum()`

### Preprocessing Operations
- **Fill Nulls (Categorical Mode):** `df['col'] = df['col'].fillna(df['col'].mode()[0])`
- **Fill Nulls (Numerical Median):** `df['col'] = df['col'].fillna(df['col'].median())`
- **Drop Duplicates:** `df.drop_duplicates(inplace=True)`
- **String Standardizing:** `df['col'] = df['col'].str.strip().str.title()`

### Outlier Detection (IQR Method)
- **First Quartile ($Q_1$):** $Q_1 = \text{df}[\text{'col'}].\text{quantile}(0.25)$
- **Third Quartile ($Q_3$):** $Q_3 = \text{df}[\text{'col'}].\text{quantile}(0.75)$
- **Interquartile Range ($IQR$):** $IQR = Q_3 - Q_1$
- **Lower Outlier Bound:** $\text{Lower Bound} = Q_1 - 1.5 \times IQR$
- **Upper Outlier Bound:** $\text{Upper Bound} = Q_3 + 1.5 \times IQR$
- **Outlier Capping:** `df['col'] = np.where(df['col'] > upper, upper, np.where(df['col'] < lower, lower, df['col']))`

---

## 2. Feature Engineering & Categorical Encoding

- **One-Hot Encoding (Nominal):** `pd.get_dummies(df, columns=['category_col'], drop_first=True)`
- **Ordinal Encoding:** `df['col_encoded'] = df['col'].map({'Low': 1, 'Medium': 2, 'High': 3})`
- **Date Feature Extraction:** `df['year'] = pd.to_datetime(df['date']).dt.year`

---

## 3. Data Visualization (Matplotlib & Seaborn)

- **Distribution / Histogram:** `sns.histplot(df['col'], kde=True)`
- **Category Comparison:** `sns.barplot(x='category', y='value', data=df)`
- **Grouped Category Plot:** `sns.countplot(x='age_band', hue='channel', data=df)`
- **Outlier Box Plot:** `sns.boxplot(x='account_type', y='amount', data=df)`
- **Correlation Heatmap:** `sns.heatmap(df.corr(), annot=True, cmap='coolwarm')`

---

## 4. Core Microsoft Excel Functions

- **Modern Lookup:** `=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])`
- **Conditional Count:** `=COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2])`
- **Conditional Sum:** `=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2])`
- **Conditional Average:** `=AVERAGEIFS(average_range, criteria_range1, criteria1)`

---

## 5. Round 1 Quiz Assessment Log

- **Student ID / Name:** [U23AD491 / Your Name]
- **Date Taken:** [YYYY-MM-DD]
- **Quiz Score:** ____ / 20 Marks
- **Percentage:** ____ %
- **Status:** [Passed (>=14/20) / Needs Review (<14/20)]
- **Review Checklist:**
  - [ ] Pandas Data Cleaning & Handling Missing Data
  - [ ] Outlier Calculation & Capping Techniques
  - [ ] Excel Pivot Tables & Conditional Formulas
  - [ ] Matplotlib & Seaborn Visualization Types