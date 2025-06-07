import numpy as np

# Dados
volumes = np.array([13.1, 13.4, 13.2])  # Em mL
conc_NaOH = 0.113  # mol/L
mm_CH3COOH = 60.052  # g/mol
volume_total = 27 #Em mL
volume_aliquota = 2 #Em mL
densidade_CH3COOH = 1.05 # Em g/cm^3

# Cálculos
media = np.mean(volumes)  # Média dos volumes
desvio_padrao = np.std(volumes, ddof=1)  # Desvio padrão
desvio_relativo = (desvio_padrao / media) * 100  # Desvio relativo

# Concentração de CH3COOH na solução diluída
conc_CH3COOH_diluido =  (media*conc_NaOH)/volume_total 

# Concentração de CH3COOH puro
conc_CH3COOH_puro = (conc_CH3COOH_diluido*volume_total)/volume_aliquota

# Concentração mássica em g/L
conc_mass = conc_CH3COOH_puro*mm_CH3COOH

#Título em massa (%)
titulo = (conc_mass/(densidade_CH3COOH*1000))*100


print(f"Média: {np.round(media, decimals = 1)} mL \n" 
      f"Desvio padrão dos volumes: {np.round(desvio_padrao, decimals = 2)} \n" 
      f"Desvio relativo dos volumes: {np.round(desvio_relativo, decimals = 2)}% \n" 
      f"Concentração de CH3COOH: {np.round(conc_CH3COOH_puro, decimals = 2)} mol/L \n" 
      f"Título: {np.round(titulo, decimals = 2)}%")