import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Dados experimentais
cu_adicionada = [0.0, 0.5, 0.75, 1.0, 1.2]
absorbancia = [0.098, 0.141, 0.162, 0.182, 0.203]

# Ajuste linear
slope, intercept, r_value, _, _ = stats.linregress(cu_adicionada, absorbancia)
x_intercept = -intercept / slope
r2 = r_value**2

# Equação da reta para legenda
equacao = f"y = {slope:.4f}x + {intercept:.4f} \n$R^2$ = {r2:.4f}"

# Gera pontos para reta do ajuste
x_vals = np.linspace(x_intercept, max(cu_adicionada)+0.3, 100)
y_vals = intercept + slope * x_vals

plt.figure(figsize=(10,6))

# Dados experimentais e coordenadas
plt.scatter(cu_adicionada, absorbancia, color="#000000", marker='x', s=70, zorder=3, label="Dados Experimentais")
for i, (xi, yi) in enumerate(zip(cu_adicionada, absorbancia)):
    plt.text(xi+0.06, yi-0.002, f"({xi:.2f}, {yi:.3f})", fontsize=11, color="#000000", va='center', ha='left')

# Reta de ajuste com equação + R na legenda
plt.plot(x_vals, y_vals, color="#ff1900", linewidth=2, zorder=2,
         label=f'Ajuste Linear:\n{equacao}')

# Evidenciar eixo y (vertical, na legenda também)
plt.axvline(x=0, color='grey', linewidth=1.5, zorder=1, label="Eixo y")

# Linha vertical verde na interseção (Cu da amostra)
plt.axvline(x=x_intercept, linestyle='--', color='#2f9032', linewidth=2, zorder=4, 
            label=f'[Cu] amostra')
plt.annotate(f'Cu amostra:\n{abs(x_intercept):.2f} mg/L',
             (x_intercept, 0.2), xytext=(x_intercept+0.1, 0.2),
             textcoords='data', color='#267b2c', fontsize=12,
             bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#267b2c'),
             arrowprops=dict(arrowstyle='->', color='#267b2c', lw=2)
)

plt.title('Determinação de $Cu^{2+}$ em aguardente', fontsize=15, family='sans-serif', pad=20)
plt.xlabel('[$Cu$] (mg/L)', fontsize=14)
plt.ylabel('Absorbância', fontsize=14)

plt.legend(fontsize=11, loc='lower right')
plt.grid(True, axis='y', linestyle=':', linewidth=1, alpha=0.7)
plt.xlim(x_intercept-0.2, max(cu_adicionada)+0.4)
plt.ylim(0, 0.22)
plt.tight_layout()
plt.show()
