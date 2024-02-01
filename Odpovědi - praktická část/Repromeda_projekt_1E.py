import pandas as pd
from scipy.stats import ttest_ind

# Načtení Excel souboru
df = pd.read_excel(r'C:\Users\marti\OneDrive\Plocha\repromeda projekt\transfery_tabulka.xlsx')

# Filtrace řádků s prázdnými hodnotami v 'clinical_gravidity'
df_filtered = df.dropna(subset=['clinical_gravidity'])

# Provedení t-testu pro pohlaví XX a XY
xx_group = df_filtered[df_filtered['sex'] == 'XX']['clinical_gravidity']
xy_group = df_filtered[df_filtered['sex'] == 'XY']['clinical_gravidity']

t_statistic, p_value = ttest_ind(xx_group, xy_group, equal_var=False)

# Zaokrouhlení P-hodnoty na 4 desetinná místa
formatted_p_value = round(p_value, 4)

# Interpretace výsledků
alpha = 0.05
print(f"P-hodnota pro významnost pohlaví embrya: {formatted_p_value}")
if formatted_p_value < alpha:
    print("P-hodnota je menší než hladina významnosti 0.05, takže zamítáme nulovou hypotézu.")
    print("Existují statisticky významné rozdíly v úspěchu klinické gravidity mezi pohlavím XX a XY.")
else:
    print("P-hodnota je větší než hladina významnosti 0.05, takže nemáme dostatek důkazů k zamítnutí nulové hypotézy.")
    print("Neexistují statisticky významné rozdíly v úspěchu klinické gravidity mezi pohlavím XX a XY.")
