import pandas as pd

# Assuming df is your DataFrame
# Create a sample DataFrame for demonstration
data = {'A': [1, 2, 3], 'B': ['a', 'b', 'c'],'C':[4,5,6]}
df = pd.DataFrame(data)

# Convert rows to strings
df_as_strings = df[['A','B']].apply(lambda row: ': '.join(map(str, row)), axis=1)
print(df_as_strings)
# Output the resulting strings
for string_row in df_as_strings:
    print(string_row)
