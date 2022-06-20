import mimetypes
import os
from pathlib import Path


def guardar_fichero(file):
    base_dir = Path(__file__).resolve().parent.parent
    fn = os.path.basename(file.filename)
    open(os.path.join(base_dir, 'static/YoPuedo/files/', fn), 'wb').write(
        file.file.read())


def checkear_imagen(fichero):
    guess = mimetypes.guess_type(fichero)
    return guess == "image/jpeg"
