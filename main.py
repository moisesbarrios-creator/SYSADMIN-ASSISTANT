
import os, shutil, platform, socket, getpass, datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
try:
    import psutil
except:
    psutil = None

class SysAdminAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("SYSADMIN ASSISTANT")

        ttk.Button(root, text="Información del Sistema", command=self.info).pack(fill="x")
        ttk.Button(root, text="Procesos", command=self.procesos).pack(fill="x")
        ttk.Button(root, text="Organizar Archivos", command=self.organizar).pack(fill="x")
        ttk.Button(root, text="Backup", command=self.backup).pack(fill="x")
        ttk.Button(root, text="Generar Reporte", command=self.reporte).pack(fill="x")

        self.txt = tk.Text(root, height=25)
        self.txt.pack(fill="both", expand=True)

    def info(self):
        self.txt.delete("1.0","end")
        self.txt.insert("end", f"Equipo: {platform.node()}\n")
        self.txt.insert("end", f"Usuario: {getpass.getuser()}\n")
        self.txt.insert("end", f"Sistema: {platform.system()} {platform.release()}\n")
        self.txt.insert("end", f"IP: {socket.gethostbyname(socket.gethostname())}\n")
        if psutil:
            ram = psutil.virtual_memory()
            self.txt.insert("end", f"RAM Total: {round(ram.total/1024**3,2)} GB\n")
            self.txt.insert("end", f"CPU: {psutil.cpu_percent()}%\n")

    def procesos(self):
        self.txt.delete("1.0","end")
        if not psutil:
            return
        for p in psutil.process_iter(['pid','name']):
            self.txt.insert("end", f"{p.info['pid']} - {p.info['name']}\n")

    def organizar(self):
        carpeta = filedialog.askdirectory()
        if not carpeta: return
        for archivo in os.listdir(carpeta):
            ruta = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta):
                ext = archivo.split(".")[-1].upper()
                destino = os.path.join(carpeta, ext)
                os.makedirs(destino, exist_ok=True)
                shutil.move(ruta, os.path.join(destino, archivo))
        messagebox.showinfo("OK","Archivos organizados")

    def backup(self):
        origen = filedialog.askdirectory(title="Origen")
        destino = filedialog.askdirectory(title="Destino")
        if origen and destino:
            carpeta = os.path.join(destino, "backup")
            shutil.copytree(origen, carpeta, dirs_exist_ok=True)
            messagebox.showinfo("OK","Respaldo realizado")

    def reporte(self):
        nombre = "reporte.txt"
        with open(nombre,"w",encoding="utf8") as f:
            f.write("Reporte generado: " + str(datetime.datetime.now()))
        messagebox.showinfo("OK", f"Reporte guardado en {nombre}")

root = tk.Tk()
app = SysAdminAssistant(root)
root.mainloop()
