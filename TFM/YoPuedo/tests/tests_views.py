from django.test import TestCase
from TFM.settings import BASE_DIR
from http import HTTPStatus
from TFM.YoPuedo.models import Usuario


##########################################################################################

# Comprobamos el funcionamiento de la URL registrarse
class RegistroViewTest(TestCase):

    def test_url_accesible(self):
        resp = self.client.get('/registrarse/')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_post_registro(self):
        data = {
            'email': "mariajesus@gmail.com",
            'nombre': "María Jesús",
            'password': 'Password1.',
            'password_again': 'Password1.',
            'foto_de_perfil': f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg"
        }
        resp = self.client.post('/registrarse/', data)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertTrue(resp.context['user'].is_active)


##########################################################################################

# Comprobamos el funcionamiento de la URL validar clave
class ClaveViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create(email="mj@gmail.com", nombre="María Jesús",
                               password="Password1.", clave_aleatoria="clave_aleatoria",
                               clave_fija="clave_fija",
                               fotoPerfil=f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg")

    def test_url_registro_accesible(self):
        resp = self.client.get('/validar_clave/registro/mj@gmail.com')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_url_inicio_accesible(self):
        resp = self.client.get('/validar_clave/inicio_sesion/mj@gmail.com')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_post_registro_correcto(self):
        data = {
            'email': 'mj@gmail.com',
            'contador': '0',
            'clave': 'clave_aleatoria'
        }

        resp = self.client.post('/validar/registro/mj@gmail.com/', data)
        self.assertEqual(resp.status_code, HTTPStatus.ACCEPTED)

    def test_post_registro_incorrecto(self):
        Usuario.objects.create(email="mariajesus@gmail.com", nombre="María Jesús",
                               password="Password1.", clave_aleatoria="clave_aleatoria",
                               clave_fija="clave_fija",
                               fotoPerfil=f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg")

        data = {
            'email': 'mariajesus@gmail.com',
            'contador': '1',
            'clave': 'clave'
        }

        resp = self.client.post('/validar/registro/mariajesus@gmail.com/', data)
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(not resp.context['user'].is_active)
        self.assertTrue(not Usuario.objects.filter(email='mariajesus@gmail.com').exists())

    def test_post_inicio_correcto(self):
        data = {
            'email': 'mj@gmail.com',
            'contador': '0',
            'clave': 'clave_aleatoria'
        }

        resp = self.client.post('/validar/inicio_sesion/mj@gmail.com/', data)
        self.assertEqual(resp.status_code, HTTPStatus.ACCEPTED)

    def test_post_inicio_incorrecto(self):
        Usuario.objects.create(email="mariajesus@gmail.com", nombre="María Jesús",
                               password="Password1.", clave_aleatoria="clave_aleatoria",
                               clave_fija="clave_fija",
                               fotoPerfil=f"{BASE_DIR}/media/YoPuedo/foto_perfil/mariajesus@gmail.com.jpg")

        data = {
            'email': 'mariajesus@gmail.com',
            'contador': '1',
            'clave': 'clave'
        }

        resp = self.client.post('/validar/registro/mariajesus@gmail.com/', data)
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(not resp.context['user'].is_active)
        self.assertTrue(Usuario.objects.filter(email='mariajesus@gmail.com').exists())
