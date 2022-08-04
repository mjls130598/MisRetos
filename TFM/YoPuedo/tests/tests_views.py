from django.test import TestCase
from TFM.settings import BASE_DIR
from http import HTTPStatus
from ..models import Usuario


##########################################################################################

# Comprobamos el funcionamiento de la URL registrarse
class RegistroViewTest(TestCase):

    def test_url_accesible(self):
        resp = self.client.get('/registrarse/')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_post_registro(self):
        data = {
            'email': "registro@view.com",
            'nombre': "María Jesús",
            'password': 'Password1.',
            'password_again': 'Password1.',
            'foto_de_perfil': f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        }
        resp = self.client.post('/registrarse/', data)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertTrue(Usuario.objects.filter(email='registro@view.com').exists())


##########################################################################################

# Comprobamos el funcionamiento de la URL validar_clave clave
class ClaveViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create_user(email="clave_view@gmail.com", nombre="María Jesús",
                               password="Password1.", clave_aleatoria="clavealeat",
                               clave_fija="clavefijausuario",
                               foto_perfil=f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg")

    def test_url_registro_accesible(self):
        resp = self.client.get('/validar_clave/registro/clave_view@gmail.com')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_url_inicio_accesible(self):
        resp = self.client.get('/validar_clave/inicio_sesion/clave_view@gmail.com')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_post_registro_correcto(self):
        data = {
            'email': 'clave_view@gmail.com',
            'contador': 0,
            'clave': 'clavealeat'
        }

        resp = self.client.post('/validar_clave/registro/clave_view@gmail.com', data)
        self.assertEqual(resp.status_code, HTTPStatus.ACCEPTED)

    def test_post_inicio_correcto(self):
        data = {
            'email': 'clave_view@gmail.com',
            'contador': 0,
            'clave': 'clavealeat'
        }

        resp = self.client.post('/validar_clave/inicio_sesion/clave_view@gmail.com', data)
        self.assertEqual(resp.status_code, HTTPStatus.ACCEPTED)

    def test_post_inicio_incorrecto(self):
        data = {
            'email': 'clave_view@gmail.com',
            'contador': 2,
            'clave': 'clavealeatoria'
        }

        resp = self.client.post('/validar_clave/inicio_sesion/clave_view@gmail.com', data)
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(not resp.context['user'].is_authenticated)
        self.assertTrue(Usuario.objects.filter(email='clave_view@gmail.com').exists())

    def test_post_registro_incorrecto(self):

        data = {
            'email': 'clave_view@gmail.com',
            'contador': 2,
            'clave': 'clavealeatoria'
        }

        resp = self.client.post('/validar_clave/registro/clave_view@gmail.com', data)
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(not resp.context['user'].is_authenticated)
        self.assertTrue(not Usuario.objects.filter(email='clave_view@gmail.com').exists())


##########################################################################################

# Comprobamos el funcionamiento de la URL registrarse
class InicioViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create_user(email="inicio_view@gmail.com", nombre="María Jesús",
                               password="Password1.", clave_aleatoria="clavealeat",
                               clave_fija="clavefijausuario",
                               foto_perfil=f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg")

    def test_url_accesible(self):
        resp = self.client.get('/iniciar_sesion/')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_post_inicio(self):
        data = {
            'email_sesion': "inicio_view@gmail.com",
            'password_sesion': 'Password1.',
        }
        resp = self.client.post('/iniciar_sesion/', data)
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        user = Usuario.objects.get(email='inicio_view@gmail.com')
        self.assertTrue(user.is_authenticated)
