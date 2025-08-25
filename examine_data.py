import pandas as pd

# Read the Excel file
df = pd.read_excel('korea_week_split(1).xlsx')

print("Columns:", df.columns.tolist())
print("\nShape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nSample data from each column:")
for col in df.columns:
    print(f"\n{col}:")
    print(df[col].head(3).tolist())
