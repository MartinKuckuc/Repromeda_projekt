import pandas as pd
from scipy.stats import f_oneway

# Načtení Excel souboru
df = pd.read_excel(r'C:\Users\marti\OneDrive\Plocha\repromeda projekt\transfery_tabulka.xlsx')

# Převod sloupce 'vek_mother' a 'vek_embryo' na číselný formát
df['vek_mother'] = pd.to_numeric(df['vek_mother'], errors='coerce')
df['vek_embryo'] = pd.to_numeric(df['vek_embryo'], errors='coerce')

# Vytvoření věkových kategorií pro matky
bins_mother = [0, 29, 34, 39, float('inf')]
labels_mother = ['do 29', '30-34', '35-39', '40 a více']
df['vek_category_mother'] = pd.cut(df['vek_mother'], bins=bins_mother, labels=labels_mother, right=False)

# Vytvoření věkových kategorií pro embrya
bins_embryo = [0, 29, 34, 39, float('inf')]
labels_embryo = ['do 29', '30-34', '35-39', '40 a více']
df['vek_category_embryo'] = pd.cut(df['vek_embryo'], bins=bins_embryo, labels=labels_embryo, right=False)

# Filtrace řádků bez hodnoty 'clinical_gravidity' a darovaných embryí
df_filtered = df[(df['clinical_gravidity'].notna()) & (df['f_donor'] != 1)]

# Provedení analýzy rozptylu (ANOVA) pro věk matky
anova_result_mother = f_oneway(
    df_filtered[df_filtered['vek_category_mother'] == 'do 29']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category_mother'] == '30-34']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category_mother'] == '35-39']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category_mother'] == '40 a více']['clinical_gravidity']
)

# Provedení analýzy rozptylu (ANOVA) pro věk embrya
anova_result_embryo = f_oneway(
    df_filtered[df_filtered['vek_category_embryo'] == 'do 29']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category_embryo'] == '30-34']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category_embryo'] == '35-39']['clinical_gravidity'],
    df_filtered[df_filtered['vek_category_embryo'] == '40 a více']['clinical_gravidity']
)

# Interpretace výsledků
alpha = 0.05
formatted_p_value_mother = round(anova_result_mother.pvalue, 4)
formatted_p_value_embryo = round(anova_result_embryo.pvalue, 4)

print(f"P-hodnota pro věk matky: {formatted_p_value_mother}")
if formatted_p_value_mother < alpha:
    print("P-hodnota je menší než hladina významnosti 0.05, takže zamítáme nulovou hypotézu pro věk matky.")
    print("Existují statisticky významné rozdíly v úspěchu transferu mezi věkovými kategoriemi matky.")
else:
    print("P-hodnota je větší než hladina významnosti 0.05, takže nemáme dostatek důkazů k zamítnutí nulové hypotézy pro věk matky.")
    print("Neexistují statisticky významné rozdíly v úspěchu transferu mezi věkovými kategoriemi matky.")

print("\nP-hodnota pro věk embrya:", formatted_p_value_embryo)
if formatted_p_value_embryo < alpha:
    print("P-hodnota je menší než hladina významnosti 0.05, takže zamítáme nulovou hypotézu pro věk embrya.")
    print("Existují statisticky významné rozdíly v úspěchu transferu mezi věkovými kategoriemi embrya.")
else:
    print("P-hodnota je větší než hladina významnosti 0.05, takže nemáme dostatek důkazů k zamítnutí nulové hypotézy pro věk embrya.")
    print("Neexistují statisticky významné rozdíly v úspěchu transferu mezi věkovými kategoriemi embrya.")
