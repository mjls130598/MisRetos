from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..forms import RegistroForm
from TFM.settings import BASE_DIR
from ..models import Usuario


# Comprobamos la validación del formulario de registro
class RegistroFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create(email="mj@gmail.com", nombre="María Jesús",
                               password="Password1.",
                               fotoPerfil=f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg")

    def test_correcto(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password1*',
            'password_again': 'Password1*',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertTrue(len(form.errors) == 0)

    def test_campo_vacio(self):
        form_data = {
            'email': '',
            'nombre': '',
            'password': '',
            'password_again': '',
        }

        form = RegistroForm(data=form_data)

        self.assertEqual(form.errors['email'], ['Este campo es obligatorio.'])
        self.assertEqual(form.errors['nombre'], ['Este campo es obligatorio.'])
        self.assertEqual(form.errors['password'], ['Este campo es obligatorio.'])
        self.assertEqual(form.errors['password_again'], ['Este campo es obligatorio.'])
        self.assertEqual(form.errors['foto_de_perfil'], ['Este campo es obligatorio.'])

    def test_email_incorrecto(self):
        form_data = {
            'email': 'mariajesus@gmail',
            'nombre': 'María Jesús',
            'password': 'Password1*',
            'password_again': 'Password1*',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['email'], ['Introduzca una dirección de correo '
                                                'electrónico válida.'])

    def test_email_existente(self):
        form_data = {
            'email': 'mj@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password1*',
            'password_again': 'Password1*',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['email'], ['Ya existe una cuenta con ese email. '
                                                'Pruebe con otro.'])

    def test_nombre_largo(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús López Salmerón María Jesús López Salmerón María '
                      'Jesús López Salmerón María Jesús López Salmerón',
            'password': 'Password1*',
            'password_again': 'Password1*',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['nombre'], ["Asegúrese de que este valor tenga "
                                                 "menos de 100 caracteres (tiene 107)."])

    def test_no_coinciden_password(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password1*',
            'password_again': 'Password1',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['password_again'], ['Las contraseñas deben ser '
                                                         'iguales'])

    def test_password_no_numerico(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password*',
            'password_again': 'Password*',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['password'], ['La contraseña debe contener al menos '
                                                   'un número'])

    def test_password_no_mayuscula(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'password1*',
            'password_again': 'password1*',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['password'], ['La contraseña debe tener al menos '
                                                   'una mayúscula'])

    def test_password_no_simbolos(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password1',
            'password_again': 'Password1',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['password'], ["La contraseña debe tener al menos "
                                                   "uno de estos símbolos: "
                                                   "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"])

    def test_password_no_minuscula(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'PASSWORD1*',
            'password_again': 'PASSWORD1*',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['password'],
                         ["La contraseña debe contener al menos una letra "
                          "en minúscula"])

    def test_foto_de_perfil_vacio(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password1*',
            'password_again': 'Password1*',
        }

        form = RegistroForm(data=form_data)

        self.assertEqual(form.errors['foto_de_perfil'], ['Este campo es obligatorio.'])

    def test_imagen_vacia(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password1*',
            'password_again': 'Password1',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/prueba.txt"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['foto_de_perfil'],
                         ['El fichero enviado está vacío.'])

    def test_no_imagen(self):
        form_data = {
            'email': 'mariajesus@gmail.com',
            'nombre': 'María Jesús',
            'password': 'Password1*',
            'password_again': 'Password1',
        }

        foto_perfil = f"{BASE_DIR}/media/YoPuedo/foto_perfil/prueba2.txt"
        foto_perfil = open(foto_perfil, 'rb')

        form = RegistroForm(data=form_data, files={'foto_de_perfil': SimpleUploadedFile(
            foto_perfil.name, foto_perfil.read())})

        self.assertEqual(form.errors['foto_de_perfil'], ['Envíe una imagen válida. El '
                                                         'fichero que ha enviado no era '
                                                         'una imagen o se trataba de una '
                                                         'imagen corrupta.'])
