from src.cleaning import basic_clean
import pandas as pd

print('Running test_import...')

df = pd.DataFrame({
    'id': [1,2,None],
    'date': ['2021-01-01', 'bad date', None],
    'value': [1.0, None, 3.5],
    'text': [' a ', None, 'c']
})

print('Original shape:', df.shape)
print(df)

cleaned = basic_clean(df, date_cols=['date'], id_cols=['id'])
print('Cleaned shape:', cleaned.shape)
print(cleaned)

