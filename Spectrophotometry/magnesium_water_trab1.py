import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Dados experimentais
mg_adicionada = [0.0, 5, 10, 15, 20]
absorbancia = [14.09, 36.22, 48.52, 63.56, 73.25]

# Ajuste linear
slope, intercept, r_value, _, _ = stats.linregress(mg_adicionada, absorbancia)
x_intercept = -intercept / slope
r2 = r_value**2

# Equação
equacao = f"y = {slope:.4f}x + {intercept:.4f}\n$R^2$ = {r2:.4f}"

# Reta
x_vals = np.linspace(x_intercept, max(mg_adicionada)+2, 100)
y_vals = intercept + slope * x_vals

plt.figure(figsize=(10,6))

# Pontos
plt.scatter(mg_adicionada, absorbancia, color="black", marker='x', s=70, zorder=3, label="Dados experimentais")

# Coordenadas
for xi, yi in zip(mg_adicionada, absorbancia):
    plt.text(xi+0.2, yi, f"({xi:.1f}, {yi:.2f})", fontsize=10)

# Reta
plt.plot(x_vals, y_vals, color="red", linewidth=2, label=f'Ajuste linear\n{equacao}')

# Eixo y
plt.axvline(0, color='grey', linewidth=1.5, label="Eixo y")

# Linha da concentração
plt.axvline(x=x_intercept, linestyle='--', color='green', linewidth=2,
            label=f'[Mg²⁺] = {abs(x_intercept):.2f} mg/L')

# Posição dinâmica da anotação
y_pos = min(absorbancia) + 0.3*(max(absorbancia)-min(absorbancia))

plt.annotate(f'[Mg²⁺]: {abs(x_intercept):.2f} mg/L',
             (x_intercept, y_pos),
             xytext=(x_intercept+2, y_pos+10),
             arrowprops=dict(arrowstyle='->'),
             fontsize=11)

# Labels
plt.title('Determinação de $Mg^{2+}$ por adição de padrão', fontsize=14)
plt.xlabel('Concentração adicionada de $Mg^{2+}$ (mg/L)', fontsize=12)
plt.ylabel('Absorbância', fontsize=12)

plt.ylim(0, 80)
plt.legend()
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()