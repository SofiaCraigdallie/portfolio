import os
import shutil

# Carpetas base
base_dir = "docs/portfolio"
ut1_dir = os.path.join(base_dir, "ingenieria_datos/UT1")
ut2_dir = os.path.join(base_dir, "ingenieria_datos/UT2")

# Crear directorios si no existen
os.makedirs(ut1_dir, exist_ok=True)
os.makedirs(ut2_dir, exist_ok=True)

# Archivos a mover (según tus nombres reales)
proyectos = {
    "01-exploracion-iris.md": ut1_dir,
    "03-eda-netflix.md": ut1_dir,
    "04-eda-multifuentesyjoins.md": ut1_dir,
    "05-missing-data-detective.md": ut2_dir,
}

# Mover archivos
for archivo, destino in proyectos.items():
    origen = os.path.join(base_dir, archivo)
    destino_final = os.path.join(destino, archivo)

    if os.path.exists(origen):
        print(f"📂 Moviendo {archivo} → {destino}")
        shutil.move(origen, destino_final)
    else:
        print(f"⚠️ No se encontró {archivo}, salteando...")

print("✅ Organización completada. ¡Ya podés actualizar mkdocs.yml!")