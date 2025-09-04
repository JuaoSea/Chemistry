import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Comprimento da corda
L = 2.0
# Velocidade da onda (valor arbitrário para visualização)
v = 1.0
# Posição x
x = np.linspace(0, L, 500)

# Modo que vamos animar (1, 2 e 3)
modos = [1, 2, 3]

# Criação da figura
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

lines = []
for ax, n in zip(axes, modos):
    line, = ax.plot([], [], lw=2)
    lines.append(line)
    ax.set_xlim(0, L)
    ax.set_ylim(-1.2, 1.2)
    ax.set_title(f"Modo {n}")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (deslocamento)")
    ax.grid(True)

# Inicialização
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Função de atualização da animação
def animate(frame):
    t = frame / 50  # tempo
    for line, n in zip(lines, modos):
        omega_n = n * np.pi * v / L
        y = np.sin(n * np.pi * x / L) * np.cos(omega_n * t)
        line.set_data(x, y)
    return lines

ani = animation.FuncAnimation(fig, animate, frames=500, init_func=init, blit=False, interval=50)

plt.show()

# Para salvar a animação em .mp4, descomente a linha abaixo e tenha o ffmpeg instalado
#ani.save("modos_corda.mp4", writer="ffmpeg", fps=20, dpi=150)
