import numpy as np

# Dados
volumes = np.array([10.5, 10.4, 10.3])  # Em mL
conc_AgNO3 = 0.0451  # mol/L
mm_NaCl = 58.5  # g/mol

# Cálculos
media = np.mean(volumes)  # Média dos volumes
desvio_padrao = np.std(volumes, ddof=1)  # Desvio padrão
desvio_relativo = (desvio_padrao / media) * 100  # Desvio relativo

# Mol de AgNO3 (igual a mol de NaCl, pela estequiometria)
mol_NaCl = (media / 1000) * conc_AgNO3  # Convertendo média de mL para L

# Massa de NaCl em g
massa_NaCl = mol_NaCl * mm_NaCl

# % m/v de NaCl (massa em g por 100 mL)
conc_NaCl_mv = (massa_NaCl / (media / 1000)) * 100  # Considerando volume titulado médio

print(media, desvio_padrao, desvio_relativo, conc_NaCl_mv)