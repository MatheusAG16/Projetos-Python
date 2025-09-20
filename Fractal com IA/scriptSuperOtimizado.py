import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
import colorsys
from numba import jit, prange
import threading
import time
from collections import deque
import queue

# Funções ultra-otimizadas com paralelização
@jit(nopython=True, parallel=True, fastmath=True)
def mandelbrot_turbo(h, w, max_iter, x_min, x_max, y_min, y_max):
    """Mandelbrot com paralelização e matemática rápida"""
    result = np.zeros((h, w), dtype=np.int32)
    dx = (x_max - x_min) / w
    dy = (y_max - y_min) / h
    
    for i in prange(h):
        y = y_min + i * dy
        for j in range(w):
            x = x_min + j * dx
            
            # Otimização: usar variáveis locais
            zr, zi = 0.0, 0.0
            zr2, zi2 = 0.0, 0.0
            
            for n in range(max_iter):
                if zr2 + zi2 > 4.0:
                    result[i, j] = n
                    break
                zi = 2.0 * zr * zi + y
                zr = zr2 - zi2 + x
                zr2 = zr * zr
                zi2 = zi * zi
            else:
                result[i, j] = max_iter
    return result

@jit(nopython=True, parallel=True, fastmath=True)
def julia_turbo(h, w, max_iter, x_min, x_max, y_min, y_max, cr, ci):
    """Julia Set ultra-otimizado"""
    result = np.zeros((h, w), dtype=np.int32)
    dx = (x_max - x_min) / w
    dy = (y_max - y_min) / h
    
    for i in prange(h):
        y = y_min + i * dy
        for j in range(w):
            x = x_min + j * dx
            
            zr, zi = x, y
            zr2, zi2 = zr * zr, zi * zi
            
            for n in range(max_iter):
                if zr2 + zi2 > 4.0:
                    result[i, j] = n
                    break
                zi = 2.0 * zr * zi + ci
                zr = zr2 - zi2 + cr
                zr2 = zr * zr
                zi2 = zi * zi
            else:
                result[i, j] = max_iter
    return result

@jit(nopython=True, parallel=True, fastmath=True)
def burning_ship_turbo(h, w, max_iter, x_min, x_max, y_min, y_max):
    """Burning Ship ultra-otimizado"""
    result = np.zeros((h, w), dtype=np.int32)
    dx = (x_max - x_min) / w
    dy = (y_max - y_min) / h
    
    for i in prange(h):
        y = y_min + i * dy
        for j in range(w):
            x = x_min + j * dx
            
            zr, zi = 0.0, 0.0
            
            for n in range(max_iter):
                if zr*zr + zi*zi > 4.0:
                    result[i, j] = n
                    break
                new_zr = zr*zr - zi*zi + x
                new_zi = 2.0 * abs(zr * zi) + y
                zr, zi = new_zr, new_zi
            else:
                result[i, j] = max_iter
    return result

@jit(nopython=True, parallel=True, fastmath=True)
def tricorn_turbo(h, w, max_iter, x_min, x_max, y_min, y_max):
    """Tricorn ultra-otimizado"""
    result = np.zeros((h, w), dtype=np.int32)
    dx = (x_max - x_min) / w
    dy = (y_max - y_min) / h
    
    for i in prange(h):
        y = y_min + i * dy
        for j in range(w):
            x = x_min + j * dx
            
            zr, zi = 0.0, 0.0
            
            for n in range(max_iter):
                if zr*zr + zi*zi > 4.0:
                    result[i, j] = n
                    break
                new_zr = zr*zr - zi*zi + x
                new_zi = -2.0 * zr * zi + y  # Conjugado
                zr, zi = new_zr, new_zi
            else:
                result[i, j] = max_iter
    return result

class VideoSmoothFractalGenerator:
    def __init__(self):
        # Resolução otimizada para fluidez
        self.width = 400
        self.height = 400
        self.max_iter = 50  # Menos iterações = mais velocidade
        self.zoom_factor = 1.2  # Zoom mais suave
        self.center_x = 0.0
        self.center_y = 0.0
        self.zoom = 1.0
        
        # Parâmetros aleatórios
        self.fractal_type = random.choice(['mandelbrot', 'julia', 'burning_ship', 'tricorn'])
        self.color_scheme = random.randint(0, 4)
        
        if self.fractal_type == 'julia':
            self.julia_c_real = random.uniform(-2, 2)
            self.julia_c_imag = random.uniform(-2, 2)
        
        # Sistema de cache multi-thread
        self.frame_cache = {}
        self.cache_size = 20
        self.render_queue = queue.Queue(maxsize=5)
        self.cache_thread_running = True
        
        # Pool de threads para pré-rendering
        self.render_threads = []
        for i in range(2):  # 2 threads de render
            t = threading.Thread(target=self._cache_worker, daemon=True)
            t.start()
            self.render_threads.append(t)
        
        # Animação automática
        self.auto_zoom = False
        self.animation_timer = None
        self.zoom_direction = 1
        self.target_x = random.uniform(-1, 1)
        self.target_y = random.uniform(-1, 1)
        
        # Sistema de transição suave
        self.transition_steps = 8
        self.transition_cache = deque(maxlen=self.transition_steps)
        
        self.generate_colormap()
        self.precompute_interesting_points()
        
        print(f"🎬 Fractal Vídeo: {self.fractal_type.upper()}")
        print(f"⚡ Resolução: {self.width}x{self.height} | FPS target: 30+")
    
    def precompute_interesting_points(self):
        """Pre-computa pontos interessantes para navegação automática"""
        self.interesting_points = []
        if self.fractal_type == 'mandelbrot':
            self.interesting_points = [
                (-0.7269, 0.1889), (-0.8, 0.156), (-0.74529, 0.11307),
                (-1.25066, 0.02012), (0.285, 0.01), (-0.762, 0.0847)
            ]
        elif self.fractal_type == 'julia':
            # Pontos interessantes para Julia sets
            self.interesting_points = [
                (0.0, 0.0), (0.3, 0.5), (-0.5, 0.6), 
                (0.285, 0.01), (-0.7269, 0.1889)
            ]
        else:
            # Pontos genéricos para outros fractais
            self.interesting_points = [
                (0.0, 0.0), (0.5, 0.5), (-0.5, 0.5),
                (0.3, -0.3), (-0.3, 0.3)
            ]
    
    def generate_colormap(self):
        """Colormap otimizado com gradientes suaves"""
        colors = np.zeros((256, 3), dtype=np.float32)  # Mais cores para suavidade
        
        for i in range(256):
            if i == 255:
                colors[i] = [0, 0, 0]
            else:
                t = i / 255.0
                
                if self.color_scheme == 0:  # Azul-vermelho suave
                    colors[i] = [
                        0.5 + 0.5 * np.cos(3.0 + t * 6.28318),
                        0.5 + 0.5 * np.cos(2.0 + t * 6.28318), 
                        0.5 + 0.5 * np.cos(1.0 + t * 6.28318)
                    ]
                elif self.color_scheme == 1:  # Arco-íris fluído
                    colors[i] = colorsys.hsv_to_rgb((t * 3) % 1.0, 0.8, 1.0)
                elif self.color_scheme == 2:  # Fogo intenso
                    colors[i] = [
                        min(1.0, t * 2),
                        min(1.0, max(0, (t - 0.3) * 2)),
                        max(0, t - 0.7) * 3
                    ]
                elif self.color_scheme == 3:  # Oceano profundo
                    colors[i] = [
                        t * 0.3,
                        0.5 + 0.5 * np.sin(t * 3.14159),
                        0.8 + 0.2 * np.cos(t * 6.28318)
                    ]
                else:  # Neon psicodélico
                    colors[i] = [
                        0.5 + 0.5 * np.sin(t * 12.56637),
                        0.5 + 0.5 * np.sin(t * 18.84955),
                        0.5 + 0.5 * np.sin(t * 25.13274)
                    ]
        
        self.colormap = colors
    
    def _cache_worker(self):
        """Worker thread para pré-renderização"""
        while self.cache_thread_running:
            try:
                params = self.render_queue.get(timeout=0.1)
                if params is None:
                    continue
                    
                zoom, cx, cy = params
                cache_key = (zoom, round(cx, 4), round(cy, 4))
                
                if cache_key not in self.frame_cache:
                    frame = self._generate_fractal_raw(zoom, cx, cy)
                    
                    # Gerencia tamanho do cache
                    if len(self.frame_cache) >= self.cache_size:
                        # Remove item mais antigo
                        oldest_key = next(iter(self.frame_cache))
                        del self.frame_cache[oldest_key]
                    
                    self.frame_cache[cache_key] = frame
                    
            except queue.Empty:
                continue
            except Exception:
                continue
    
    def _generate_fractal_raw(self, zoom, center_x, center_y):
        """Geração raw ultra-rápida"""
        x_min = center_x - 2.0 / zoom
        x_max = center_x + 2.0 / zoom
        y_min = center_y - 2.0 / zoom
        y_max = center_y + 2.0 / zoom
        
        if self.fractal_type == 'mandelbrot':
            iterations = mandelbrot_turbo(self.height, self.width, self.max_iter, 
                                        x_min, x_max, y_min, y_max)
        elif self.fractal_type == 'julia':
            iterations = julia_turbo(self.height, self.width, self.max_iter,
                                   x_min, x_max, y_min, y_max,
                                   self.julia_c_real, self.julia_c_imag)
        elif self.fractal_type == 'burning_ship':
            iterations = burning_ship_turbo(self.height, self.width, self.max_iter,
                                          x_min, x_max, y_min, y_max)
        else:  # tricorn
            iterations = tricorn_turbo(self.height, self.width, self.max_iter,
                                     x_min, x_max, y_min, y_max)
        
        # Mapeia para colormap expandido
        normalized = (iterations * 255 / self.max_iter).astype(np.int32)
        normalized = np.clip(normalized, 0, 255)
        
        return self.colormap[normalized]
    
    def generate_fractal_smooth(self):
        """Geração com transições suaves"""
        cache_key = (self.zoom, round(self.center_x, 4), round(self.center_y, 4))
        
        # Tenta pegar do cache primeiro
        if cache_key in self.frame_cache:
            return self.frame_cache[cache_key]
        
        # Se não estiver no cache, gera rapidamente
        start_time = time.time()
        frame = self._generate_fractal_raw(self.zoom, self.center_x, self.center_y)
        calc_time = time.time() - start_time
        
        # Adiciona ao cache
        if len(self.frame_cache) >= self.cache_size:
            oldest_key = next(iter(self.frame_cache))
            del self.frame_cache[oldest_key]
        self.frame_cache[cache_key] = frame
        
        # Pré-carrega próximos frames
        self._preload_next_frames()
        
        print(f"⚡ Frame: {calc_time*1000:.1f}ms | Cache: {len(self.frame_cache)}")
        return frame
    
    def _preload_next_frames(self):
        """Pré-carrega próximos frames prováveis"""
        if self.render_queue.qsize() < 3:  # Não sobrecarrega a queue
            # Pré-carrega zooms próximos
            for zoom_mult in [self.zoom_factor, 1/self.zoom_factor]:
                next_zoom = self.zoom * zoom_mult
                try:
                    self.render_queue.put_nowait((next_zoom, self.center_x, self.center_y))
                except queue.Full:
                    break
    
    def smooth_zoom_in(self, event):
        """Zoom suave com interpolação"""
        for step in range(self.transition_steps):
            zoom_step = self.zoom * (self.zoom_factor ** (step / self.transition_steps))
            self._smooth_update(zoom_step, self.center_x, self.center_y)
        
        self.zoom *= self.zoom_factor
        if self.zoom > 5:
            self.max_iter = min(100, int(50 + np.log10(self.zoom) * 10))
            self.generate_colormap()
    
    def smooth_zoom_out(self, event):
        """Zoom out suave"""
        for step in range(self.transition_steps):
            zoom_step = self.zoom * (1/self.zoom_factor) ** (step / self.transition_steps)
            self._smooth_update(zoom_step, self.center_x, self.center_y)
        
        self.zoom /= self.zoom_factor
        if self.zoom <= 5:
            self.max_iter = 50
            self.generate_colormap()
    
    def _smooth_update(self, zoom, cx, cy):
        """Atualização ultra-suave"""
        self.zoom = zoom
        self.center_x = cx
        self.center_y = cy
        
        fractal_image = self.generate_fractal_smooth()
        self.im.set_array(fractal_image)
        self.fig.canvas.draw_idle()
        plt.pause(0.01)  # Pequena pausa para fluidez
    
    def toggle_auto_zoom(self, event):
        """Toggle animação automática"""
        self.auto_zoom = not self.auto_zoom
        if self.auto_zoom:
            self.start_animation()
        else:
            if self.animation_timer:
                self.animation_timer.cancel()
    
    def start_animation(self):
        """Inicia animação suave automática"""
        if not self.auto_zoom:
            return
        
        # Zoom automático suave
        if self.zoom > 100:
            self.zoom_direction = -1
        elif self.zoom < 2:
            self.zoom_direction = 1
            # Muda para um ponto interessante aleatório
            self.target_x, self.target_y = random.choice(self.interesting_points)
        
        # Movimento suave em direção ao target
        dx = (self.target_x - self.center_x) * 0.05
        dy = (self.target_y - self.center_y) * 0.05
        
        self.center_x += dx
        self.center_y += dy
        
        # Zoom suave
        if self.zoom_direction > 0:
            self.zoom *= 1.05
        else:
            self.zoom *= 0.95
        
        # Atualiza frame
        fractal_image = self.generate_fractal_smooth()
        self.im.set_array(fractal_image)
        self.fig.canvas.draw_idle()
        
        # Próximo frame
        self.animation_timer = threading.Timer(0.033, self.start_animation)  # ~30 FPS
        self.animation_timer.start()
    
    def on_click(self, event):
        """Click suave com transição"""
        if event.inaxes != self.ax:
            return
        
        range_size = 4.0 / self.zoom
        new_x = self.center_x - range_size/2 + (event.xdata / self.width) * range_size
        new_y = self.center_y - range_size/2 + ((self.height - event.ydata) / self.height) * range_size
        
        # Transição suave para novo centro
        steps = 6
        for i in range(steps):
            t = (i + 1) / steps
            interp_x = self.center_x + (new_x - self.center_x) * t
            interp_y = self.center_y + (new_y - self.center_y) * t
            self._smooth_update(self.zoom, interp_x, interp_y)
    
    def new_fractal(self, event):
        """Novo fractal com transição"""
        print("🎬 Novo fractal suave...")
        
        # Para animação
        if self.auto_zoom:
            self.auto_zoom = False
            if self.animation_timer:
                self.animation_timer.cancel()
        
        # Limpa cache
        self.frame_cache.clear()
        
        # Novo fractal
        self.__init__()
        fractal_image = self.generate_fractal_smooth()
        self.im.set_array(fractal_image)
        self.fig.canvas.draw_idle()
    
    def show(self):
        """Interface de vídeo suave"""
        print("🎬 Iniciando modo vídeo suave...")
        
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(14, 10), facecolor='black')
        self.fig.suptitle(f'🎬 FRACTAL VIDEO: {self.fractal_type.upper()}', 
                         fontsize=18, color='white')
        
        # Primeira renderização
        fractal_image = self.generate_fractal_smooth()
        self.im = self.ax.imshow(fractal_image, extent=[0, self.width, 0, self.height], 
                                interpolation='bilinear')  # Interpolação para suavidade
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Interface compacta
        plt.subplots_adjust(left=0.12)
        
        # Botões otimizados
        btn_y = 0.88
        btn_spacing = 0.06
        btn_width, btn_height = 0.08, 0.04
        
        buttons = [
            ('Zoom +', self.smooth_zoom_in),
            ('Zoom -', self.smooth_zoom_out), 
            ('Auto', self.toggle_auto_zoom),
            ('Novo', self.new_fractal)
        ]
        
        for i, (label, callback) in enumerate(buttons):
            ax_btn = plt.axes([0.02, btn_y - i*btn_spacing, btn_width, btn_height])
            btn = Button(ax_btn, label, color='darkblue', hovercolor='blue')
            btn.label.set_color('white')
            btn.on_clicked(callback)
        
        # Info em tempo real
        info_text = [
            '🎬 FRACTAL VIDEO MODE',
            '',
            '⚡ TURBO RENDERING',
            f'📐 {self.width}x{self.height}',
            f'🎯 {self.max_iter} iter',
            '🧵 Multi-thread cache',
            '💾 Smart pre-loading',
            '',
            '🎮 CONTROLES:',
            '• Click = Navegar suave',
            '• Auto = Zoom automático',  
            '• Zoom = Transições fluídas',
            '',
            '🚀 TARGET: 30+ FPS',
        ]
        
        for i, text in enumerate(info_text):
            weight = 'bold' if any(x in text for x in ['🎬', '⚡', '🎮', '🚀']) else 'normal'
            size = 11 if weight == 'bold' else 9
            color = 'cyan' if weight == 'bold' else 'white'
            self.fig.text(0.02, 0.65 - i*0.032, text, fontsize=size, 
                         weight=weight, color=color)
        
        plt.tight_layout()
        plt.show()
    
    def __del__(self):
        """Cleanup ao destruir"""
        self.cache_thread_running = False
        if hasattr(self, 'animation_timer') and self.animation_timer:
            self.animation_timer.cancel()

if __name__ == "__main__":
    print("🎬" * 25)
    print("     FRACTAL VIDEO ENGINE")
    print("🎬" * 25)
    print("\n🚀 OTIMIZAÇÕES EXTREMAS:")
    print("   ⚡ Numba parallel + fastmath")
    print("   🧵 Multi-thread pre-rendering") 
    print("   💾 Intelligent frame caching")
    print("   🎨 Smooth color transitions")
    print("   📐 Optimized resolution (400x400)")
    print("   🎯 Target: 30+ FPS real-time")
    print("\n🎮 RECURSOS ESPECIAIS:")
    print("   🌊 Transições ultra-suaves")
    print("   🤖 Auto-zoom com IA navigation")
    print("   🎨 Interpolação bilinear")
    print("   ⚡ Cache preditivo inteligente")
    
    try:
        fractal_gen = VideoSmoothFractalGenerator()
        fractal_gen.show()
    except ImportError as e:
        print(f"\n❌ Para performance máxima instale:")
        print("   pip install numba")
        print(f"\nErro: {e}")
    except KeyboardInterrupt:
        print("\n👋 Finalizando Fractal Video Engine...")