# FileOrganizer

## Descripción

Aplicación CLI en Python para organizar archivos recursivamente por fecha de creación, estructurando en carpetas `/AÑO/MES/`. Soporta metadatos EXIF para imágenes y videos, con fallback a fecha de modificación.

## Requisitos

- Python 3.11+
- Dependencias: Pillow, Hachoir (instalar via `requirements.txt`)

## Instalación

1. Clona el repositorio.
2. Crea entorno virtual: `python -m venv venv`.
3. Activa: `source venv/bin/activate` (Linux/macOS) o `venv\Scripts\activate` (Windows).
4. Instala: `pip install -r requirements.txt`.

## Uso

Ejecuta desde la raíz del proyecto:

```bash
python -m src.main /ruta/directorio_raiz /ruta/directorio_destino
```
