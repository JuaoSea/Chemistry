import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.special import hermite, factorial

# Parâmetros
alpha = 1.0
x = np.linspace(-10, 10, 400)
v_min, v_max = 0, 40
frames = v_max - v_min + 1

# Função que gera função de onda e densidade
def psi_v(v, x, alpha):
    H_v = hermite(v)
    norm = (alpha/np.pi)**0.25 / np.sqrt(2**v * factorial(v))
    psi = norm * H_v(np.sqrt(alpha)*x) * np.exp(-0.5 * alpha * x**2)
    return psi, np.abs(psi)**2

# Criação da figura
fig, ax = plt.subplots(figsize=(8, 5))
line_psi, = ax.plot([], [], lw=2, label=r'$\psi_v(x)$')
line_prob, = ax.plot([], [], 'r', lw=2, label=r'$|\psi_v(x)|^2$')

ax.set_xlim(x.min(), x.max())
ax.set_ylim(-0.8, 0.8)
ax.set_xlabel('x')
ax.set_ylabel('Amplitude')
ax.set_title("Oscilador Harmônico Quântico: Função de onda e densidade")
ax.grid(True)
ax.legend()
text_v = ax.text(0.05, 0.90, '', transform=ax.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.7))

def init():
    line_psi.set_data([], [])
    line_prob.set_data([], [])
    text_v.set_text('')
    return line_psi, line_prob, text_v

def animate(frame):
    v = v_min + frame
    psi, prob = psi_v(v, x, alpha)
    line_psi.set_data(x, psi)
    line_prob.set_data(x, prob)
    text_v.set_text(f"v = {v}")
    return line_psi, line_prob, text_v

ani = animation.FuncAnimation(fig, animate, frames=frames, init_func=init, blit=True, interval=600)

plt.tight_layout()
plt.show()

# Para salvar:
ani.save("oscilador_harmonico.mp4", writer="ffmpeg", fps=1, dpi=150)
