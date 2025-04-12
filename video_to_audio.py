import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import os
import re
from yt_dlp import YoutubeDL

class YouTubeAudioDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Audio YouTube")
        self.root.geometry("550x350")
        self.root.resizable(False, False)
        
        # Variables
        self.carpeta_guardado = os.path.expanduser("~/Downloads")
        self.descarga_en_proceso = False
        self.usar_ffmpeg = True
        self.ruta_ffmpeg = ""
        
        # Crear interfaz
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="Descargador de Audio de YouTube", font=("Helvetica", 14, "bold"))
        titulo.pack(pady=5)
        
        # URL
        frame_url = tk.Frame(main_frame)
        frame_url.pack(fill=tk.X, pady=5)
        
        etiqueta = tk.Label(frame_url, text="URL del video:", font=("Helvetica", 10))
        etiqueta.pack(side=tk.LEFT, padx=5)
        
        self.entrada_url = tk.Entry(frame_url, width=50, font=("Helvetica", 10))
        self.entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Carpeta
        frame_carpeta = tk.Frame(main_frame)
        frame_carpeta.pack(fill=tk.X, pady=5)
        
        self.etiqueta_carpeta = tk.Label(frame_carpeta, text=f"📁 {self.carpeta_guardado}", 
                                         font=("Helvetica", 9), fg="gray")
        self.etiqueta_carpeta.pack(side=tk.LEFT, padx=5)
        
        btn_carpeta = tk.Button(frame_carpeta, text="Cambiar", command=self.seleccionar_carpeta)
        btn_carpeta.pack(side=tk.RIGHT, padx=5)
        
        # Opción FFmpeg
        frame_ffmpeg = tk.Frame(main_frame)
        frame_ffmpeg.pack(fill=tk.X, pady=5)
        
        self.btn_ffmpeg = tk.Button(frame_ffmpeg, text="Seleccionar FFmpeg", 
                                   command=self.seleccionar_ffmpeg)
        self.btn_ffmpeg.pack(side=tk.RIGHT, padx=5)
        
        self.etiqueta_ffmpeg = tk.Label(frame_ffmpeg, text="FFmpeg: No configurado", font=("Helvetica", 9), fg="orange")
        self.etiqueta_ffmpeg.pack(side=tk.LEFT, padx=5)
        
        # Formato
        frame_formato = tk.Frame(main_frame)
        frame_formato.pack(fill=tk.X, pady=5)
        
        etiqueta_formato = tk.Label(frame_formato, text="Formato:", font=("Helvetica", 10))
        etiqueta_formato.pack(side=tk.LEFT, padx=5)
        
        self.formato_var = tk.StringVar(value="mp3")
        opciones_formato = ["mp3", "m4a", "wav", "opus"]
        
        formato_dropdown = ttk.Combobox(frame_formato, textvariable=self.formato_var, 
                                        values=opciones_formato, state="readonly", width=10)
        formato_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Calidad
        etiqueta_calidad = tk.Label(frame_formato, text="Calidad:", font=("Helvetica", 10))
        etiqueta_calidad.pack(side=tk.LEFT, padx=(20, 5))
        
        self.calidad_var = tk.StringVar(value="192")
        opciones_calidad = ["64", "128", "192", "256", "320"]
        
        calidad_dropdown = ttk.Combobox(frame_formato, textvariable=self.calidad_var, 
                                        values=opciones_calidad, state="readonly", width=10)
        calidad_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Progreso
        frame_progreso = tk.Frame(main_frame)
        frame_progreso.pack(fill=tk.X, pady=10)
        
        self.barra_progreso = ttk.Progressbar(frame_progreso, orient="horizontal", 
                                              length=500, mode="determinate")
        self.barra_progreso.pack(fill=tk.X, padx=5)
        
        self.etiqueta_progreso = tk.Label(frame_progreso, text="", font=("Helvetica", 9))
        self.etiqueta_progreso.pack(pady=5)
        
        # Botones
        frame_botones = tk.Frame(main_frame)
        frame_botones.pack(fill=tk.X, pady=10)
        
        self.btn_descargar = tk.Button(frame_botones, text="Descargar Audio", 
                                        command=self.iniciar_descarga, bg="#4CAF50", fg="white", 
                                        font=("Helvetica", 10, "bold"), padx=20, pady=5)
        self.btn_descargar.pack(side=tk.RIGHT, padx=5)
        
        self.btn_cancelar = tk.Button(frame_botones, text="Cancelar", 
                                      command=self.cancelar_descarga, state=tk.DISABLED,
                                      font=("Helvetica", 10), padx=10, pady=5)
        self.btn_cancelar.pack(side=tk.RIGHT, padx=5)
        
        # Estado
        self.etiqueta_estado = tk.Label(main_frame, text="Configura FFmpeg antes de descargar", 
                                         font=("Helvetica", 9), fg="orange")
        self.etiqueta_estado.pack(pady=5)
            
    def seleccionar_ffmpeg(self):
        # Seleccionar la carpeta bin de FFmpeg
        ffmpeg_dir = filedialog.askdirectory(title="Seleccionar carpeta bin de FFmpeg")
        
        if ffmpeg_dir:
            # Verificar si contiene ffmpeg.exe (Windows) o ffmpeg (Mac/Linux)
            ffmpeg_exe = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
            ffmpeg_path = os.path.join(ffmpeg_dir, ffmpeg_exe)
            
            if os.path.exists(ffmpeg_path):
                self.ruta_ffmpeg = ffmpeg_dir
                self.etiqueta_ffmpeg.config(text=f"FFmpeg: Configurado", fg="green")
                self.etiqueta_estado.config(text="FFmpeg configurado correctamente. Listo para descargar.", fg="green")
            else:
                messagebox.showerror("Error", f"No se encontró {ffmpeg_exe} en la carpeta seleccionada")
                self.etiqueta_estado.config(text="FFmpeg no encontrado en la carpeta seleccionada", fg="red")
    
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.carpeta_guardado = carpeta
            self.etiqueta_carpeta.config(text=f"📁 {self.carpeta_guardado}")
    
    def progreso_hook(self, d):
        if d['status'] == 'downloading':
            # Extraer el porcentaje limpio
            porcentaje_bruto = d.get('_percent_str', '0.0%').strip()
            porcentaje_limpio = re.sub(r'\x1b\[[0-9;]*m', '', porcentaje_bruto)
            
            try:
                progreso = float(porcentaje_limpio.replace('%', ''))
                self.barra_progreso["value"] = progreso
                
                # Actualizar etiqueta con información de velocidad y tiempo restante
                velocidad = d.get('_speed_str', '? KiB/s')
                velocidad_limpia = re.sub(r'\x1b\[[0-9;]*m', '', velocidad).strip()
                
                tiempo_restante = d.get('_eta_str', '?')
                tiempo_limpio = re.sub(r'\x1b\[[0-9;]*m', '', tiempo_restante).strip()
                
                texto_progreso = f"Progreso: {porcentaje_limpio} - Velocidad: {velocidad_limpia} - Tiempo restante: {tiempo_limpio}"
                self.etiqueta_progreso.config(text=texto_progreso)
                
            except ValueError:
                self.etiqueta_progreso.config(text="Preparando descarga...")
            
            self.root.update_idletasks()
            
        elif d['status'] == 'finished':
            self.barra_progreso["value"] = 100
            self.etiqueta_progreso.config(text="Convirtiendo a formato de audio...")
            self.root.update_idletasks()
    
    def iniciar_descarga(self):
        url = self.entrada_url.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, introduce un enlace de YouTube válido")
            return
        
        # Validar URL
        if not (url.startswith('http://') or url.startswith('https://')) or 'youtube' not in url and 'youtu.be' not in url:
            messagebox.showwarning("URL no válida", "Por favor, introduce un enlace de YouTube válido")
            return
        
        # Verificar que FFmpeg esté configurado
        if not self.ruta_ffmpeg:
            messagebox.showwarning("FFmpeg no configurado", 
                               "Por favor, selecciona la carpeta bin de FFmpeg para continuar")
            return
            
        self.descarga_en_proceso = True
        self.btn_descargar.config(state=tk.DISABLED)
        self.btn_cancelar.config(state=tk.NORMAL)
        self.etiqueta_estado.config(text="Descargando...", fg="#1976D2")
        
        # Iniciar descarga en segundo plano
        threading.Thread(target=self.descargar_audio, args=(url,), daemon=True).start()
    
    def descargar_audio(self, url):
        try:
            formato = self.formato_var.get()
            calidad = self.calidad_var.get()
            
            opciones = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.carpeta_guardado, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': formato,
                    'preferredquality': calidad,
                }],
                'progress_hooks': [self.progreso_hook],
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'ffmpeg_location': self.ruta_ffmpeg,
            }
            
            with YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=False)
                titulo = info.get('title', 'Video sin título')
                
                # Actualizar estado
                self.mostrar_estado(f"Descargando: {titulo}", "blue")
                
                # Descargar
                ydl.download([url])
                
            # Descarga completada
            self.mostrar_estado("¡Descarga completada con éxito!", "green")
            messagebox.showinfo("Éxito", f"Audio descargado correctamente:\n{titulo}\n\nFormato: {formato}\nCalidad: {calidad} kbps\nUbicación: {self.carpeta_guardado}")
            
        except Exception as e:
            error_msg = str(e)
            self.mostrar_estado(f"Error: {error_msg[:50]}...", "red")
            messagebox.showerror("Error", f"Ocurrió un error durante la descarga:\n{error_msg}")
        
        finally:
            self.finalizar_descarga()
    
    def cancelar_descarga(self):
        if self.descarga_en_proceso:
            self.mostrar_estado("Descarga cancelada por el usuario", "orange")
            self.finalizar_descarga()
    
    def finalizar_descarga(self):
        self.descarga_en_proceso = False
        self.btn_descargar.config(state=tk.NORMAL)
        self.btn_cancelar.config(state=tk.DISABLED)
        self.barra_progreso["value"] = 0
        self.etiqueta_progreso.config(text="")
    
    def mostrar_estado(self, mensaje, color="black"):
        self.etiqueta_estado.config(text=mensaje, fg=color)
        self.root.update_idletasks()

# Iniciar aplicación
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = YouTubeAudioDownloader(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error crítico", f"Error al iniciar la aplicación:\n{str(e)}")