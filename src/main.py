import sys
from pathlib import Path
from .organizer import organize_files  # Agrega el punto para relativo

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python main.py <directorio_raiz> <directorio_destino>")
        sys.exit(1)
    root_dir = Path(sys.argv[1]).resolve()
    dest_dir = Path(sys.argv[2]).resolve()
    organize_files(root_dir, dest_dir)
    print("Organización completada.")
