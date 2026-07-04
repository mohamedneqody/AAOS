import pandas as pd

df = pd.DataFrame({
    'CustomerID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Revenue': [100.5, 200.0, 150.25],
    'IsActive': [True, False, True]
})

df.to_excel('Book1.xlsx', index=False)
print("Book1.xlsx created")
