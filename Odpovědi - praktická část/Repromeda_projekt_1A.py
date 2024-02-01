import pandas as pd

# Načtení Excel souboru
df = pd.read_excel(r'C:\Users\marti\OneDrive\Plocha\repromeda projekt\transfery_tabulka.xlsx')

# Převod sloupce 'vek_mother' na číselný formát
df['vek_mother'] = pd.to_numeric(df['vek_mother'], errors='coerce')

# Vytvoření věkových kategorií
bins = [0, 25, 30, 35, 40, float('inf')]
labels = ['<25', '25-30', '30-35', '35-40', '40+']
df['vek_category'] = pd.cut(df['vek_mother'], bins=bins, labels=labels, right=False)

# Filtrace řádků bez hodnoty 'clinical_gravidity'
df_filtered = df.dropna(subset=['clinical_gravidity'])

# Vytvoření tabulky úspěšnosti embryotransferu
success_table = pd.pivot_table(df_filtered, values='clinical_gravidity', index='vek_category', aggfunc='mean') * 100

# Přidání řádku pro všechny kategorie
success_table.loc['všechny kategorie'] = success_table.mean()

# Zaokrouhlení na 2 desetinná místa
success_table = success_table.round(2)

# Přejmenování sloupce pro lepší čitelnost
success_table.rename(columns={'clinical_gravidity': 'success_rate'}, inplace=True)

# Výpis výsledné tabulky úspěšnosti
print(success_table)
