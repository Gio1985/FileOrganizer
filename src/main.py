import sys
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
from .organizer import get_creation_date  # Solo importar get_creation_date


def select_dir(entry):
    """Selecciona un directorio y lo coloca en el campo de entrada."""
    dir_path = filedialog.askdirectory()
    if dir_path:
        entry.delete(0, tk.END)
        entry.insert(0, dir_path)


def run_organize(root_entry, dest_entry, progress, status, root):
    """Organiza archivos y actualiza barra de progreso."""
    root_dir = Path(root_entry.get()).resolve()
    dest_dir = Path(dest_entry.get()).resolve()
    if not root_dir.is_dir() or not dest_dir.exists():
        status.config(text="Directorios inválidos")
        return

    files = list(root_dir.rglob('*'))
    total = sum(1 for f in files if f.is_file())
    progress['maximum'] = total
    count = 0

    for item in files:
        if item.is_file():
            date = get_creation_date(item)
            year = date.strftime('%Y')
            month = date.strftime('%m')
            target_path = dest_dir / year / month
            target_path.mkdir(parents=True, exist_ok=True)
            item.rename(target_path / item.name)
            count += 1
            progress['value'] = count
            status.config(text=f"Procesando: {count}/{total}")
            root.update_idletasks()

    status.config(text="Completado")


if __name__ == '__main__':
    if len(sys.argv) > 1:  # CLI
        from .organizer import organize_files
        root_dir = Path(sys.argv[1]).resolve()
        dest_dir = Path(sys.argv[2]).resolve()
        organize_files(root_dir, dest_dir)
        print("Completado")
    else:  # GUI
        root = tk.Tk()
        root.title("FileOrganizer")

        tk.Label(root, text="Origen:").grid(row=0, column=0, padx=5, pady=5)
        root_entry = tk.Entry(root, width=50)
        root_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Seleccionar", command=lambda: select_dir(
            root_entry)).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Destino:").grid(row=1, column=0, padx=5, pady=5)
        dest_entry = tk.Entry(root, width=50)
        dest_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Seleccionar", command=lambda: select_dir(
            dest_entry)).grid(row=1, column=2, padx=5, pady=5)

        progress = ttk.Progressbar(root, length=400, mode='determinate')
        progress.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        status = tk.Label(root, text="")
        status.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        tk.Button(root, text="Ejecutar", command=lambda: run_organize(
            root_entry, dest_entry, progress, status, root)).grid(row=4, column=1, padx=5, pady=5)

        root.mainloop()
