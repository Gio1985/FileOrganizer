""" Proyecto FileOrganizer"""
import sys
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from pathlib import Path
from .organizer import get_creation_date


def select_dir(entry):
    """ Función para seleccionar un directorio usando un diálogo de archivos. """
    dir_path = filedialog.askdirectory()
    if dir_path:
        entry.delete(0, tk.END)
        entry.insert(0, dir_path)


def run_organize(root_entry, dest_entry, progress, status, log_text, root):
    """ Función para ejecutar la organización de archivos. """
    source_dir = Path(root_entry.get()).resolve()
    dest_dir = Path(dest_entry.get()).resolve()
    if not source_dir.is_dir() or not dest_dir.exists():
        log_text.config(state='normal')
        log_text.insert(tk.END, "Directorios inválidos\n")
        log_text.config(state='disabled')
        log_text.see(tk.END)
        return

    files = list(source_dir.rglob('*'))
    total = sum(1 for f in files if f.is_file())
    progress['maximum'] = total
    count = 0
    skipped = 0

    meses = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }

    for item in files:
        if item.is_file():
            date = get_creation_date(item)
            year = date.strftime('%Y')
            month_num = date.strftime('%m')
            month_name = meses[month_num]
            target_path = dest_dir / year / f"{month_num}-{month_name}"
            target_path.mkdir(parents=True, exist_ok=True)
            dest_file = target_path / item.name
            if dest_file.exists():
                log_text.config(state='normal')
                log_text.insert(tk.END, f"Duplicado omitido: {item.name}\n")
                log_text.config(state='disabled')
                log_text.see(tk.END)
                skipped += 1
            else:
                item.rename(dest_file)
                count += 1
            progress['value'] = count + skipped
            status.config(text=f"Procesando: {count + skipped}/{total}")
            root.update_idletasks()

    log_text.config(state='normal')
    log_text.insert(
        tk.END, f"Proceso terminado exitosamente: {count} archivos organizados, {skipped} omitidos.\n")
    log_text.config(state='disabled')
    log_text.see(tk.END)


if __name__ == '__main__':
    if len(sys.argv) > 1:  # CLI
        from .organizer import organize_files
        source_dir = Path(sys.argv[1]).resolve()
        dest_dir = Path(sys.argv[2]).resolve()
        try:
            organize_files(source_dir, dest_dir)
            print("Completado")
        except FileExistsError as e:
            print(f"Duplicado omitido: {e.filename}")
    else:  # GUI
        root = tk.Tk()
        root.title("FileOrganizer")
        root.geometry("600x300")

        tk.Label(root, text="Origen:").grid(row=0, column=0, padx=10, pady=5)
        root_entry = tk.Entry(root, width=50)
        root_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Seleccionar", command=lambda: select_dir(
            root_entry)).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(root, text="Destino:").grid(row=1, column=0, padx=10, pady=5)
        dest_entry = tk.Entry(root, width=50)
        dest_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Seleccionar", command=lambda: select_dir(
            dest_entry)).grid(row=1, column=2, padx=10, pady=5)

        progress = ttk.Progressbar(root, length=500, mode='determinate')
        progress.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        status = tk.Label(root, text="")
        status.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        tk.Button(root, text="Ejecutar", command=lambda: run_organize(
            root_entry, dest_entry, progress, status, log_text, root)).grid(row=4, column=1, padx=10, pady=10)

        log_text = scrolledtext.ScrolledText(
            root, width=70, height=5, state='disabled')  # Inicial disabled
        log_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        root.mainloop()
