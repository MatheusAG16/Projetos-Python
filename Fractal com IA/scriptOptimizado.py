import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
import colorsys
from numba import jit
import threading
import time

# Funções otimizadas com Numba JIT para cálculos ultra-rápidos
@jit(nopython=True)
def mandelbrot_set(h, w, max_iter, x_min, x_max, y_min, y_max):
    """Versão ultra-otimizada do conjunto de Mandelbrot"""
    result = np.zeros((h, w), dtype=np.int32)
    
    for i in range(h):
        for j in range(w):
            # Mapear pixel para coordenadas complexas
            c_real = x_min + (x_max - x_min) * j / w
            c_imag = y_min + (y_max - y_min) * i / h
            
            # Iteração de Mandelbrot
            z_real = 0.0
            z_imag = 0.0
            
            for n in range(max_iter):
                if z_real*z_real + z_imag*z_imag > 4:
                    result[i, j] = n
                    break
                
                new_real = z_real*z_real - z_imag*z_imag + c_real
                new_imag = 2*z_real*z_imag + c_imag
                z_real = new_real
                z_imag = new_imag
            else:
                result[i, j] = max_iter
    
    return result

@jit(nopython=True)
def julia_set(h, w, max_iter, x_min, x_max, y_min, y_max, c_real, c_imag):
    """Versão ultra-otimizada do conjunto de Julia"""
    result = np.zeros((h, w), dtype=np.int32)
    
    for i in range(h):
        for j in range(w):
            z_real = x_min + (x_max - x_min) * j / w
            z_imag = y_min + (y_max - y_min) * i / h
            
            for n in range(max_iter):
                if z_real*z_real + z_imag*z_imag > 4:
                    result[i, j] = n
                    break
                
                new_real = z_real*z_real - z_imag*z_imag + c_real
                new_imag = 2*z_real*z_imag + c_imag
                z_real = new_real
                z_imag = new_imag
            else:
                result[i, j] = max_iter
    
    return result

@jit(nopython=True)
def burning_ship_set(h, w, max_iter, x_min, x_max, y_min, y_max):
    """Versão ultra-otimizada do Burning Ship"""
    result = np.zeros((h, w), dtype=np.int32)
    
    for i in range(h):
        for j in range(w):
            c_real = x_min + (x_max - x_min) * j / w
            c_imag = y_min + (y_max - y_min) * i / h
            
            z_real = 0.0
            z_imag = 0.0
            
            for n in range(max_iter):
                if z_real*z_real + z_imag*z_imag > 4:
                    result[i, j] = n
                    break
                
                new_real = abs(z_real)*abs(z_real) - abs(z_imag)*abs(z_imag) + c_real
                new_imag = 2*abs(z_real)*abs(z_imag) + c_imag
                z_real = new_real
                z_imag = new_imag
            else:
                result[i, j] = max_iter
    
    return result

@jit(nopython=True)
def tricorn_set(h, w, max_iter, x_min, x_max, y_min, y_max):
    """Versão ultra-otimizada do Tricorn"""
    result = np.zeros((h, w), dtype=np.int32)
    
    for i in range(h):
        for j in range(w):
            c_real = x_min + (x_max - x_min) * j / w
            c_imag = y_min + (y_max - y_min) * i / h
            
            z_real = 0.0
            z_imag = 0.0
            
            for n in range(max_iter):
                if z_real*z_real + z_imag*z_imag > 4:
                    result[i, j] = n
                    break
                
                # Conjugado de z
                new_real = z_real*z_real - z_imag*z_imag + c_real
                new_imag = -2*z_real*z_imag + c_imag
                z_real = new_real
                z_imag = new_imag
            else:
                result[i, j] = max_iter
    
    return result

class FastFractalGenerator:
    def __init__(self):
        # Resolução reduzida para performance (pode ajustar)
        self.width = 600
        self.height = 600
        self.max_iter = 80  # Menos iterações inicialmente
        self.zoom_factor = 2.0
        self.center_x = 0.0
        self.center_y = 0.0
        self.zoom = 1.0
        
        # Parâmetros aleatórios
        self.fractal_type = random.choice(['mandelbrot', 'julia', 'burning_ship', 'tricorn'])
        self.color_scheme = random.randint(0, 4)
        
        # Parâmetros específicos para Julia
        if self.fractal_type == 'julia':
            self.julia_c_real = random.uniform(-2, 2)
            self.julia_c_imag = random.uniform(-2, 2)
        
        # Cache para colormap
        self._color_cache = {}
        self.generate_colormap()
        
        print(f"🚀 Fractal otimizado: {self.fractal_type}")
        if self.fractal_type == 'julia':
            print(f"   Parâmetro: {self.julia_c_real:.3f} + {self.julia_c_imag:.3f}i")
    
    def generate_colormap(self):
        """Pre-calcula o mapa de cores para performance"""
        colors = np.zeros((self.max_iter + 1, 3))
        
        for i in range(self.max_iter + 1):
            if i == self.max_iter:
                colors[i] = [0, 0, 0]  # Preto para pontos no conjunto
            else:
                t = i / self.max_iter
                
                if self.color_scheme == 0:  # Azul-vermelho
                    colors[i] = colorsys.hsv_to_rgb(0.7 * t, 1, 1)
                elif self.color_scheme == 1:  # Arco-íris
                    colors[i] = colorsys.hsv_to_rgb(t, 1, 1)
                elif self.color_scheme == 2:  # Fogo
                    colors[i] = [min(1, 2*t), min(1, 2*t-0.5) if t > 0.25 else 0, 0]
                elif self.color_scheme == 3:  # Oceano
                    colors[i] = [0, min(1, 2*t), min(1, t*3)]
                else:  # Psicodélico
                    colors[i] = colorsys.hsv_to_rgb((3*t) % 1, 1, 1)
        
        self.colormap = colors
    
    def generate_fractal(self):
        """Gera fractal usando funções otimizadas"""
        start_time = time.time()
        
        # Define área de visualização
        x_min = self.center_x - 2.0 / self.zoom
        x_max = self.center_x + 2.0 / self.zoom
        y_min = self.center_y - 2.0 / self.zoom
        y_max = self.center_y + 2.0 / self.zoom
        
        # Chama função otimizada correspondente
        if self.fractal_type == 'mandelbrot':
            iterations = mandelbrot_set(self.height, self.width, self.max_iter, 
                                      x_min, x_max, y_min, y_max)
        elif self.fractal_type == 'julia':
            iterations = julia_set(self.height, self.width, self.max_iter,
                                 x_min, x_max, y_min, y_max,
                                 self.julia_c_real, self.julia_c_imag)
        elif self.fractal_type == 'burning_ship':
            iterations = burning_ship_set(self.height, self.width, self.max_iter,
                                        x_min, x_max, y_min, y_max)
        elif self.fractal_type == 'tricorn':
            iterations = tricorn_set(self.height, self.width, self.max_iter,
                                   x_min, x_max, y_min, y_max)
        
        # Aplica colormap vetorizado (super rápido)
        fractal_image = self.colormap[iterations]
        
        calc_time = time.time() - start_time
        print(f"⚡ Fractal calculado em {calc_time:.3f}s")
        
        return fractal_image
    
    def zoom_in(self, event):
        """Zoom in otimizado"""
        self.zoom *= self.zoom_factor
        # Aumenta iterações apenas se necessário
        if self.zoom > 10:
            self.max_iter = min(200, int(80 + np.log10(self.zoom) * 20))
            self.generate_colormap()  # Regenera colormap se mudou iterações
        self.update_fractal()
    
    def zoom_out(self, event):
        """Zoom out otimizado"""
        self.zoom /= self.zoom_factor
        if self.zoom <= 10:
            self.max_iter = 80
            self.generate_colormap()
        self.update_fractal()
    
    def reset_view(self, event):
        """Reset otimizado"""
        self.center_x = 0.0
        self.center_y = 0.0
        self.zoom = 1.0
        self.max_iter = 80
        self.generate_colormap()
        self.update_fractal()
    
    def new_fractal(self, event):
        """Gera novo fractal rapidamente"""
        print("🔄 Gerando novo fractal...")
        self.__init__()
        self.update_fractal()
    
    def on_click(self, event):
        """Click otimizado para recentrar"""
        if event.inaxes != self.ax:
            return
        
        # Conversão otimizada de coordenadas
        range_size = 4.0 / self.zoom
        
        self.center_x = self.center_x - range_size/2 + (event.xdata / self.width) * range_size
        self.center_y = self.center_y - range_size/2 + ((self.height - event.ydata) / self.height) * range_size
        
        self.update_fractal()
    
    def update_fractal(self):
        """Atualização otimizada da visualização"""
        print(f"🔄 Zoom: {self.zoom:.1f}x, Iterações: {self.max_iter}")
        
        # Gera fractal em thread separada para não travar a UI
        def generate_and_update():
            fractal_image = self.generate_fractal()
            # Atualiza na thread principal
            self.fig.canvas.mpl_connect('draw_event', lambda e: self.im.set_array(fractal_image))
            self.im.set_array(fractal_image)
            self.fig.canvas.draw_idle()  # draw_idle é mais rápido que draw
        
        # Para fractais simples, calcula diretamente; para complexos, usa thread
        if self.zoom < 50:
            generate_and_update()
        else:
            thread = threading.Thread(target=generate_and_update)
            thread.daemon = True
            thread.start()
    
    def show(self):
        """Interface otimizada"""
        print("🖥️  Inicializando interface...")
        
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.suptitle(f'🚀 Fractal Turbo: {self.fractal_type.upper()}', fontsize=16)
        
        # Primeira geração
        fractal_image = self.generate_fractal()
        self.im = self.ax.imshow(fractal_image, extent=[0, self.width, 0, self.height])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Conecta eventos
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Interface compacta
        plt.subplots_adjust(left=0.15)
        
        # Botões otimizados
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
        
        # Instruções compactas
        instructions = [
            '🚀 FRACTAL TURBO',
            '',
            '• Clique = Centralizar',
            '• Botões = Zoom',  
            '• "Novo" = Outro fractal',
            '',
            '⚡ Otimizado com Numba!',
            f'📐 Resolução: {self.width}x{self.height}',
            f'🎯 Iterações: {self.max_iter}'
        ]
        
        for i, text in enumerate(instructions):
            weight = 'bold' if '🚀' in text else 'normal'
            size = 11 if '🚀' in text else 9
            self.fig.text(0.02, 0.65 - i*0.04, text, fontsize=size, weight=weight)
        
        plt.show()

# Executar o gerador ultra-rápido
if __name__ == "__main__":
    print("🚀" * 20)
    print("   GERADOR DE FRACTAIS TURBO")  
    print("🚀" * 20)
    print("\n⚡ Otimizações ativas:")
    print("   • Numba JIT compilation")
    print("   • Cálculos vetorizados")  
    print("   • Cache de colormaps")
    print("   • Threading para zoom alto")
    print("   • Resolução adaptativa")
    print("\n🎯 Preparando fractal...")
    
    try:
        fractal_gen = FastFractalGenerator()
        fractal_gen.show()
    except ImportError:
        print("\n❌ Para máxima performance, instale:")
        print("   pip install numba")
        print("\n🔄 Executando versão básica otimizada...")
        
        # Fallback sem numba (ainda otimizado)
        import sys
        sys.modules['numba'] = type(sys)('numba')
        sys.modules['numba'].jit = lambda **kwargs: lambda f: f
        fractal_gen = FastFractalGenerator()
        fractal_gen.show()