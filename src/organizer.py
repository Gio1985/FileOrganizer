import os
import shutil
from datetime import datetime
from pathlib import Path
from contextlib import closing

from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


def get_creation_date(file_path: Path) -> datetime:
    """Obtiene fecha de creación real del archivo."""
    try:
        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff']:
            with Image.open(file_path) as img:
                exif_data = img.getexif()
                if exif_data and 36867 in exif_data:  # DateTimeOriginal
                    date_str = exif_data[36867]
                    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        elif file_path.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv']:
            parser = createParser(str(file_path))
            if parser is not None:  # Verificar explícitamente
                with closing(parser) as p:
                    metadata = extractMetadata(p)
                    if metadata:
                        date = metadata.get('creation_date')
                        if date:
                            return date
    except Exception:
        pass  # Fallback si error
    # Fallback: fecha de modificación del archivo
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def organize_files(root_dir: Path, dest_dir: Path):
    """Organiza archivos recursivamente."""
    for item in root_dir.rglob('*'):
        if item.is_file():
            date = get_creation_date(item)
            year = date.strftime('%Y')
            month = date.strftime('%m')
            target_path = dest_dir / year / month
            target_path.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(target_path / item.name))
