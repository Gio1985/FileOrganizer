# FileOrganizer

## Descripción

Aplicación CLI en Python para organizar archivos recursivamente por fecha de creación, estructurando en carpetas `/AÑO/MES-NOMBRE/`. Soporta metadatos EXIF para imágenes y videos, con fallback a fecha de modificación.

- CLI para operaciones rápidas.
- GUI con progreso, logs de errores/omitidos y mensaje de éxito.

## Requisitos

- Python 3.11+
- Dependencias: Pillow, Hachoir (instalar vía `requirements.txt`)

## Instalación

1. Clona el repositorio.
2. Crea entorno virtual: `python -m venv venv`.
3. Activa: `source venv/bin/activate` (Linux/macOS) o `venv\Scripts\activate` (Windows).
4. Instala: `pip install -r requirements.txt`.

## Uso

Ejecuta de dos medios:

- Con GUI: simplemente ejecuta `python -m src.main` en la raíz del proyecto por defecto. Configura Origen o Destino vía UI.
- CLI: `python -m src.main /ruta/directorio_raiz /ruta/directorio_destino`.

## Notas

- Mueve archivos sin alterarlos.
- Compatible con Windows, Linux, macOS.
- Subcarpetas creadas con formato `MM-NOMBRE/` (e.g. `01-Enero`).
- Licencia: MIT (o especifica según corresponda).
