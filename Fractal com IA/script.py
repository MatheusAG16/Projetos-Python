import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
import colorsys

class FractalGenerator:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.max_iter = 100
        self.zoom_factor = 2.0
        self.center_x = 0.0
        self.center_y = 0.0
        self.zoom = 1.0
        
        # Parâmetros aleatórios para diferentes tipos de fractais
        self.fractal_type = random.choice(['mandelbrot', 'julia', 'burning_ship', 'tricorn'])
        self.color_scheme = random.randint(0, 4)
        
        # Parâmetros específicos para Julia Set
        if self.fractal_type == 'julia':
            self.julia_c = complex(random.uniform(-2, 2), random.uniform(-2, 2))
        
        print(f"Fractal gerado: {self.fractal_type}")
        if self.fractal_type == 'julia':
            print(f"Parâmetro Julia: {self.julia_c}")
    
    def mandelbrot(self, c):
        """Calcula o conjunto de Mandelbrot"""
        z = 0
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return self.max_iter
    
    def julia(self, z):
        """Calcula o conjunto de Julia"""
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = z*z + self.julia_c
        return self.max_iter
    
    def burning_ship(self, c):
        """Calcula o fractal Burning Ship"""
        z = 0
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = complex(abs(z.real), abs(z.imag))**2 + c
        return self.max_iter
    
    def tricorn(self, c):
        """Calcula o fractal Tricorn"""
        z = 0
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = z.conjugate()**2 + c
        return self.max_iter
    
    def get_color(self, iterations):
        """Gera cores baseadas no esquema escolhido"""
        if iterations == self.max_iter:
            return (0, 0, 0)  # Preto para pontos no conjunto
        
        t = iterations / self.max_iter
        
        if self.color_scheme == 0:  # Esquema azul-vermelho
            return colorsys.hsv_to_rgb(0.7 * t, 1, 1)
        elif self.color_scheme == 1:  # Esquema arco-íris
            return colorsys.hsv_to_rgb(t, 1, 1)
        elif self.color_scheme == 2:  # Esquema fogo
            return (min(1, 2*t), min(1, 2*t-0.5) if t > 0.25 else 0, 0)
        elif self.color_scheme == 3:  # Esquema oceano
            return (0, min(1, 2*t), min(1, t*3))
        else:  # Esquema psicodélico
            return colorsys.hsv_to_rgb((3*t) % 1, 1, 1)
    
    def generate_fractal(self):
        """Gera o fractal atual com os parâmetros de zoom"""
        # Define a área de visualização baseada no zoom e centro
        x_min = self.center_x - 2.0 / self.zoom
        x_max = self.center_x + 2.0 / self.zoom
        y_min = self.center_y - 2.0 / self.zoom
        y_max = self.center_y + 2.0 / self.zoom
        
        # Cria arrays de coordenadas
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j*Y
        
        # Calcula o fractal
        fractal_array = np.zeros((self.height, self.width, 3))
        
        for i in range(self.height):
            for j in range(self.width):
                if self.fractal_type == 'mandelbrot':
                    iterations = self.mandelbrot(C[i, j])
                elif self.fractal_type == 'julia':
                    iterations = self.julia(C[i, j])
                elif self.fractal_type == 'burning_ship':
                    iterations = self.burning_ship(C[i, j])
                elif self.fractal_type == 'tricorn':
                    iterations = self.tricorn(C[i, j])
                
                fractal_array[i, j] = self.get_color(iterations)
        
        return fractal_array
    
    def zoom_in(self, event):
        """Aumenta o zoom"""
        self.zoom *= self.zoom_factor
        self.max_iter = min(500, int(self.max_iter * 1.1))  # Aumenta iterações com zoom
        self.update_fractal()
    
    def zoom_out(self, event):
        """Diminui o zoom"""
        self.zoom /= self.zoom_factor
        self.max_iter = max(50, int(self.max_iter * 0.9))  # Diminui iterações
        self.update_fractal()
    
    def reset_view(self, event):
        """Reseta para a visualização inicial"""
        self.center_x = 0.0
        self.center_y = 0.0
        self.zoom = 1.0
        self.max_iter = 100
        self.update_fractal()
    
    def new_fractal(self, event):
        """Gera um novo fractal aleatório"""
        self.__init__()  # Reinicializa com novos parâmetros aleatórios
        self.update_fractal()
    
    def on_click(self, event):
        """Centraliza o zoom no ponto clicado"""
        if event.inaxes != self.ax:
            return
        
        # Converte coordenadas da tela para coordenadas complexas
        x_range = 4.0 / self.zoom
        y_range = 4.0 / self.zoom
        
        self.center_x = self.center_x - x_range/2 + (event.xdata / self.width) * x_range
        self.center_y = self.center_y - y_range/2 + ((self.height - event.ydata) / self.height) * y_range
        
        self.update_fractal()
    
    def update_fractal(self):
        """Atualiza a visualização do fractal"""
        print(f"Gerando fractal... Zoom: {self.zoom:.2f}, Centro: ({self.center_x:.4f}, {self.center_y:.4f})")
        fractal_image = self.generate_fractal()
        self.im.set_array(fractal_image)
        self.fig.canvas.draw()
    
    def show(self):
        """Exibe o fractal com interface interativa"""
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.suptitle(f'Fractal Aleatório: {self.fractal_type.capitalize()}', fontsize=16)
        
        # Gera e exibe o fractal inicial
        fractal_image = self.generate_fractal()
        self.im = self.ax.imshow(fractal_image, extent=[0, self.width, 0, self.height])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Conecta evento de clique
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Cria botões
        ax_zoom_in = plt.axes([0.02, 0.85, 0.1, 0.04])
        ax_zoom_out = plt.axes([0.02, 0.80, 0.1, 0.04])
        ax_reset = plt.axes([0.02, 0.75, 0.1, 0.04])
        ax_new = plt.axes([0.02, 0.70, 0.1, 0.04])
        
        btn_zoom_in = Button(ax_zoom_in, 'Zoom +')
        btn_zoom_out = Button(ax_zoom_out, 'Zoom -')
        btn_reset = Button(ax_reset, 'Reset')
        btn_new = Button(ax_new, 'Novo')
        
        btn_zoom_in.on_clicked(self.zoom_in)
        btn_zoom_out.on_clicked(self.zoom_out)
        btn_reset.on_clicked(self.reset_view)
        btn_new.on_clicked(self.new_fractal)
        
        # Adiciona instruções
        self.fig.text(0.02, 0.65, 'Instruções:', fontsize=12, weight='bold')
        self.fig.text(0.02, 0.60, '• Clique para centralizar', fontsize=10)
        self.fig.text(0.02, 0.56, '• Use os botões para zoom', fontsize=10)
        self.fig.text(0.02, 0.52, '• "Novo" gera outro fractal', fontsize=10)
        self.fig.text(0.02, 0.48, '• Zoom infinito disponível!', fontsize=10)
        
        plt.tight_layout()
        plt.show()

# Executar o gerador de fractais
if __name__ == "__main__":
    print("🌀 Gerador de Fractais Aleatórios com Zoom Infinito 🌀")
    print("=" * 50)
    
    fractal_gen = FractalGenerator()
    fractal_gen.show()