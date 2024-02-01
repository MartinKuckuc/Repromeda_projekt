import pandas as pd
from scipy.stats import f_oneway

# Načtení Excel souboru
df = pd.read_excel(r'C:\Users\marti\OneDrive\Plocha\repromeda projekt\transfery_tabulka.xlsx')

# Převod sloupce 'vek_mother' na číselný formát
df['vek_mother'] = pd.to_numeric(df['vek_mother'], errors='coerce')

# Vytvoření věkových kategorií
bins = [0, 29, 34, 39, float('inf')]
labels = ['do 29', '30-34', '35-39', '40 a více']
df['vek_category'] = pd.cut(df['vek_mother'], bins=bins, labels=labels, right=False)

# Filtrace řádků bez hodnoty 'clinical_gravidity'
df_filtered = df.dropna(subset=['clinical_gravidity'])

# Provedení analýzy rozptylu (ANOVA) pro všechny kategorie
anova_result = f_oneway(
    df_filtered[df_filtered['vek_category'] == 'do 29']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category'] == '30-34']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category'] == '35-39']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category'] == '40 a více']['clinical_gravidity']
)

# Interpretace výsledků
alpha = 0.05
formatted_p_value = round(anova_result.pvalue, 4)
print(f"P-hodnota pro všechny kategorie: {formatted_p_value}")
if formatted_p_value < alpha:
    print("P-hodnota je menší než hladina významnosti 0.05, takže zamítáme nulovou hypotézu.")
    print("Existují statisticky významné rozdíly v úspěchu transferu mezi věkovými kategoriemi.")
else:
    print("P-hodnota je větší než hladina významnosti 0.05, takže nemáme dostatek důkazů k zamítnutí nulové hypotézy.")
    print("Neexistují statisticky významné rozdíly v úspěchu transferu mezi věkovými kategoriemi.")

# Provedení analýzy rozptylu (ANOVA) pro každou kategorii zvlášť
categories = ['do 29', '30-34', '35-39', '40 a více']
for category in categories:
    subset = df_filtered[df_filtered['vek_category'] == category]['clinical_gravidity']
    p_value = f_oneway(subset, df_filtered[df_filtered['vek_category'] != category]['clinical_gravidity']).pvalue
    formatted_p_value = round(p_value, 4)
    print(f"\nP-hodnota pro kategorii '{category}': {formatted_p_value}")
    if formatted_p_value < alpha:
        print("P-hodnota je menší než hladina významnosti 0.05, takže zamítáme nulovou hypotézu.")
        print("Existují statisticky významné rozdíly v úspěchu transferu mezi touto kategorií a ostatními.")
    else:
        print("P-hodnota je větší než hladina významnosti 0.05, takže nemáme dostatek důkazů k zamítnutí nulové hypotézy.")
        print("Neexistují statisticky významné rozdíly v úspěchu transferu mezi touto kategorií a ostatními.")
