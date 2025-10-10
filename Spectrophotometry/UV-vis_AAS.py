import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  #
from sklearn.metrics import r2_score  

# Dados experimentais de absorbância e concentração
absorbance = [0.071, 0.173, 0.275, 0.329, 0.422, 0.540, 0.567, 0.739, 0.910]  
concentration = [0.5153, 1.0306, 1.5459, 2.0612, 2.5765, 3.0918, 3.6071, 4.1224, 4.6377]  

# Ajuste de uma regressão linear aos dados experimentais (modelo y = mx + b)
coefficients = np.polyfit(concentration, absorbance, 1)  # Calcula os coeficientes da regressão
slope_new, intercept_new = coefficients  # Armazena a inclinação (m) e o intercepto (b)

# Geração de valores ajustados de absorbância para o modelo
y_fit = slope_new * np.array(concentration) + intercept_new  # Valores previstos de absorbância com base no modelo

# Cálculo das concentrações a partir das absorbâncias usando a equação da linha ajustada
calculated_concentration = [(a - intercept_new) / slope_new for a in absorbance]

# Organização dos dados em um DataFrame para facilitar a visualização
data = pd.DataFrame({
    "Absorbance": absorbance,  # Valores de absorbância
    "Measured Concentration (mg/L)": concentration,  # Concentrações medidas
    "Calculated Concentration (mg/L)": calculated_concentration  # Concentrações calculadas pelo modelo
})

# Configuração da figura para os gráficos
plt.figure(figsize=(12, 6))

# Gráfico 1: Curva de calibração
plt.subplot(1, 2, 1)  
x = np.linspace(min(concentration), max(concentration), 100)  # Valores para desenhar a linha da regressão
plt.plot(x, slope_new * x + intercept_new, color="red", 
         label=f"Curva de calibração: y = {slope_new:.4f}x + {intercept_new:.4f}")  
plt.scatter(concentration, absorbance, color="black", 
            label="Dados Experimentais", marker="x", zorder=5)  

# Anotações dos pontos experimentais no gráfico
for conc, abs_val in zip(concentration, absorbance):
    plt.text(conc, abs_val, f"({conc:.4f}, {abs_val:.3f})", fontsize=8, ha='right')

# Cálculo e exibição do coeficiente de determinação (R²) no gráfico
r2 = r2_score(absorbance, y_fit)  #
plt.text(4.02, 0.03, f"$R^2 = {r2:.4f}$", fontsize=10, color='blue', ha='left', va='bottom')

# Configuração do título e rótulos do gráfico de calibração
plt.title("Curva de Calibração")
plt.xlabel("Concentração (mg/L)")
plt.ylabel("Absorbância")
plt.legend()  
plt.grid(True)  

# Gráfico 2: Comparação entre concentrações medidas e calculadas
plt.subplot(1, 2, 2)  
plt.scatter(concentration, concentration, color="green", 
            label="Concentração medida", marker="x", zorder=6)  # Linha referência y=x
plt.scatter(concentration, calculated_concentration, color="orange", 
            label="Concentração calculada", marker="x", zorder=6)  # Pontos calculados
plt.plot([0, max(concentration)], [0, max(concentration)], color="red", linestyle="--", 
         label="y=x", zorder=5)  # Linha diagonal de referência

# Adiciona anotações para cada ponto no gráfico de comparação
for measured, calculated in zip(concentration, calculated_concentration):
    plt.text(measured, calculated, f"({measured:.4f}, {calculated:.4f})", fontsize=8, ha='left')

# Configuração do título e rótulos do gráfico de comparação
plt.title("Comparação entre Concentração Medida e Calculada")
plt.xlabel("Concentração medida (mg/L)")
plt.ylabel("Concentração calculada (mg/L)")
plt.legend()  
plt.grid(True) 

# Ajusta os layouts para evitar sobreposição
plt.tight_layout()
plt.savefig('calibration_curve.png')  # Salva a figura
plt.show()  # Exibe os gráficos
