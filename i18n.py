import os
import json
import sys

def ruta_recurso(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GestorIdiomas:
    def __init__(self, idioma_codigo="es"):
        self.carpeta_idiomas = ruta_recurso("idiomas")
        self.idiomas_disponibles = {}  # { "es": "Español", "en": "English" }
        self.traducciones = {}
        self.traducciones_base = {}  # Fallback (Español)
        self.idioma_actual = idioma_codigo

        self.escanear_idiomas()
        self.cargar_idioma_base()
        self.cargar_idioma(idioma_codigo)

    def escanear_idiomas(self):
        """Busca todos los archivos .json en la carpeta idiomas y extrae sus nombres"""
        self.idiomas_disponibles = {}
        if not os.path.exists(self.carpeta_idiomas):
            try:
                os.makedirs(self.carpeta_idiomas)
            except Exception:
                pass
            return

        for archivo in os.listdir(self.carpeta_idiomas):
            if archivo.endswith(".json"):
                path = os.path.join(self.carpeta_idiomas, archivo)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        meta = data.get("meta", {})
                        codigo = meta.get("codigo", os.path.splitext(archivo)[0])
                        nombre = meta.get("nombre_idioma", codigo.upper())
                        self.idiomas_disponibles[codigo] = nombre
                except Exception as e:
                    print(f"⚠️ Error al leer archivo de idioma {archivo}: {e}")

    def cargar_idioma_base(self):
        """Carga el idioma base (Español) para fallback"""
        path = os.path.join(self.carpeta_idiomas, "es.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.traducciones_base = json.load(f)
            except Exception:
                self.traducciones_base = {}

    def cargar_idioma(self, codigo):
        """Carga el diccionario del idioma solicitado"""
        self.idioma_actual = codigo
        path = os.path.join(self.carpeta_idiomas, f"{codigo}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.traducciones = json.load(f)
            except Exception as e:
                print(f"⚠️ Error al cargar idioma {codigo}: {e}")
                self.traducciones = self.traducciones_base
        else:
            self.traducciones = self.traducciones_base

    def t(self, clave, default=None):
        """Obtiene la traducción de una clave (ej: 'ajustes.titulo').
           Soporta claves compuestas divididas por puntos."""
        partes = clave.split(".")
        
        # 1. Buscar en idioma actual
        val = self._obtener_valor(self.traducciones, partes)
        if val is not None:
            return val

        # 2. Buscar en idioma base (Fallback)
        val = self._obtener_valor(self.traducciones_base, partes)
        if val is not None:
            return val

        # 3. Valor por defecto o clave
        return default if default is not None else clave

    def _obtener_valor(self, d, partes):
        sub = d
        for p in partes:
            if isinstance(sub, dict) and p in sub:
                sub = sub[p]
            else:
                return None
        return sub if isinstance(sub, str) else None
