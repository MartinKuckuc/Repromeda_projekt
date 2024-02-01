import pandas as pd

# Načtení Excel souboru
df = pd.read_excel(r'C:\Users\marti\OneDrive\Plocha\repromeda projekt\transfery_tabulka.xlsx')

# Vytvoření tabulky s počty transferů dle použité genetické metody
genetic_method_counts = df['genetic_method'].value_counts().reset_index()
genetic_method_counts.columns = ['Genetické metody', 'Počet']

# Přidání řádku pro prázdnou hodnotu (bez genetické metody)
empty_count = len(df[df['genetic_method'].isna()])
genetic_method_counts = pd.concat([genetic_method_counts, pd.DataFrame({'Genetické metody': ['bez genetické metody'], 'Počet': [empty_count]})], ignore_index=True)

# Přidání řádku pro ostatní genetické metody
other_count = len(df) - genetic_method_counts['Počet'].sum()
genetic_method_counts = pd.concat([genetic_method_counts, pd.DataFrame({'Genetické metody': ['ostatní'], 'Počet': [other_count]})], ignore_index=True)

# Výpis výsledné tabulky
print(genetic_method_counts)
