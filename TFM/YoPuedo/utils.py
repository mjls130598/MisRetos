import logging
import os.path
import random
import string
from shutil import rmtree

from TFM.settings import BASE_DIR, EMAIL_HOST_USER
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMultiAlternatives

from .models import Usuario, Reto, Etapa, Animo, Prueba, Notificacion

logger = logging.getLogger(__name__)


class Utils:
    # Método de subida de ficheros
    @staticmethod
    def handle_uploaded_file(image, localizacion, directorio):
        logger.info("Comprobamos que el directorio donde se va a guardar está creado "
                    "previamente")
        if not os.path.exists(directorio):
            try:
                logger.info(f"Creamos el directorio {directorio}")
                os.makedirs(directorio)
            except OSError:
                logger.error(
                    f"Se ha producido un error al crear el directorio {directorio}")
                raise

        logger.info("Guardamos archivos en local")
        with open(localizacion, "wb+") as destination:
            for chunk in image.chunks():
                destination.write(chunk)

    # Método para guardar al nuevo usuario en la BBDD
    @staticmethod
    def guardar_usuario(self, email, nombre, password, foto):
        fichero, extension = os.path.splitext(foto.name)
        directorio = os.path.join(BASE_DIR, "media", "YoPuedo", "foto_perfil")
        localizacion = os.path.join(directorio, email + extension)
        clave_fija = self.claves_aleatorias(16)
        clave_aleatoria = self.claves_aleatorias(10)

        try:
            self.handle_uploaded_file(foto, localizacion, directorio)
        except:
            logger.error("Error al subir la foto de perfil")

        fichero = os.path.join("/media", "YoPuedo", "foto_perfil", email + extension)
        Usuario.objects.create_user(email=email, nombre=nombre, password=password,
                                    foto_perfil=fichero, clave_fija=clave_fija,
                                    clave_aleatoria=clave_aleatoria)
        return clave_aleatoria, clave_fija

    # Método que genera claves aleatorias
    @staticmethod
    def claves_aleatorias(longitud):
        logger.info("Generamos clave aleatoria")
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(longitud))
        return result_str

    # Método para enviar correos
    @staticmethod
    def enviar_correo(content, email, contexto):
        logger.info(f"Enviamos correo a {email}")
        mail = EmailMultiAlternatives(
            contexto,
            'Yo Puedo',
            EMAIL_HOST_USER,
            [email]
        )

        mail.attach_alternative(content, 'text/html')
        mail.send()

    CATEGORIAS_CHOOSE = (
        ("", ""),
        ("economia", "Ahorro"),
        ("inteligencia", "Conocimientos"),
        ("salud", "Deporte"),
        ("mente", "Miedos")
    )

    categorias = ["economia", "inteligencia", "salud", "mente"]

    @staticmethod
    def numero_elementos_importados(importados):

        num_elementos = 0

        for elemento in importados:
            if elemento:
                num_elementos += 1

        return num_elementos

    @staticmethod
    def crear_id_reto():
        caracteres = string.ascii_lowercase + string.digits
        id_reto = "RET"
        while True:
            id_reto += ''.join(random.choice(caracteres) for _ in range(47))
            reto = Reto.objects.filter(id_reto=id_reto)

            if len(reto) == 0:
                break
            else:
                id_reto = "RET"

        return id_reto

    @staticmethod
    def crear_id_etapa(num_etapa):
        caracteres = string.ascii_lowercase + string.digits
        id_etapa = f"ETP{num_etapa}"
        while True:
            id_etapa += ''.join(random.choice(caracteres) for _ in range(47))
            etapa = Etapa.objects.filter(id_etapa=id_etapa)

            if len(etapa) == 0:
                break
            else:
                id_etapa = "ETP"

        return id_etapa

    @staticmethod
    def eliminar_archivo(archivo):
        logger.info(f"Eliminamos el archivo {archivo}")
        os.remove(archivo)

    @staticmethod
    def valido_general(reto, general_form):
        logger.info("Miramos si el formulario GENERAL es válido")
        if not general_form.is_valid():
            logger.info("Comprobamos los errores encontrados en el formulario")
            if not ('titulo' in general_form.errors or 'categoria' in
                    general_form.errors):
                logger.info("Verificamos que los errores encontrados son los buscados")

                valido_objetivo = 'Debes indicar el objetivo del reto' in \
                                  general_form.errors['objetivo_texto'] and \
                                  '/media/' in reto.objetivo \
                    if 'objetivo_texto' in general_form.errors else True

                valida_recompensa = 'Debes indicar la recompensa del reto' in \
                                    general_form.errors['recompensa_texto'] and \
                                    '/media/' in reto.recompensa \
                    if 'recompensa_texto' in general_form.errors else True

                if 'objetivo_texto' in general_form.errors and \
                        'Debes indicar el objetivo del reto' in \
                        general_form.errors['objetivo_texto'] and \
                        '/media/' in reto.objetivo:
                    general_form.errors.pop('objetivo_texto', None)

                if 'recompensa_texto' in general_form.errors and \
                        'Debes indicar la recompensa del reto' in \
                        general_form.errors['recompensa_texto'] and \
                        '/media/' in reto.recompensa:
                    general_form.errors.pop('recompensa_texto', None)

                return general_form, valido_objetivo and valida_recompensa
            else:
                logger.error("Tiene errores en título y/o categoría")
                return general_form, False

        else:
            logger.info("El formulario es correcto")
            return general_form, True

    @staticmethod
    def validas_etapas(reto, etapas_form):

        etapas_validas = etapas_form.is_valid()

        logger.info("Miramos si el formulario ETAPAS es válido")
        if not etapas_validas:
            logger.info("Comprobamos los errores encontrados en el formulario")
            etapas_validas = True
            etapas = reto.etapa_set.all()

            for index, etapa_form in enumerate(etapas_form):
                if not etapa_form.is_valid():
                    logger.info("No es válida la etapa por ...")
                    if not etapa_form.cleaned_data or \
                            etapa_form.cleaned_data['id_etapa'].value() == '':
                        logger.info("Es nueva y no tiene los datos necesarios")
                        etapas_validas = False
                    else:
                        id_etapa = etapa_form.cleaned_data['id_etapa'].value()
                        if 'Debes indicar el objetivo de la etapa' in \
                                etapa_form.errors['objetivo_texto'] and \
                                '/media/' in etapas.get(id_etapa=id_etapa).objetivo:
                            etapas_form[index].errors.pop('objetivo_texto', None)
                        else:
                            etapas_validas = False
                else:
                    logger.info(f"Etapa {index + 1} correcta")
        else:
            logger.info("El formulario es correcto")

        return etapas_form, etapas_validas

    # Método para borrar los archivos multimedia del reto
    def borrar_reto(reto):
        logger.info(f"Borramos archivos del reto {reto.id_reto}")
        rmtree(os.path.join(BASE_DIR, "media", "YoPuedo", reto.id_reto))

    # Método para borrar los archivos de ánimos de una persona
    def borrar_animo(usuario):
        logger.info(f"Borramos los archivos de ánimo de {usuario.email}")
        animos = Animo.objects.filter(animador__usuario=usuario,
                                      mensaje__contains='/media/')

        for animo in animos:
            Utils.eliminar_archivo(os.path.join(BASE_DIR, animo.mensaje[1:]))

    # Método para borrar los archivos de ánimos de una persona
    def borrar_animo_reto(usuario, reto):
        logger.info(f"Borramos los archivos de ánimo de {usuario.email} del reto {reto.id_reto}")
        animos = Animo.objects.filter(animador__usuario=usuario,
                                      etapa__reto=reto,
                                      mensaje__contains='/media/')

        for animo in animos:
            Utils.eliminar_archivo(os.path.join(BASE_DIR, animo.mensaje[1:]))

    # Método para borrar los archivos de pruebs de una persona
    def borrar_prueba(usuario):
        logger.info(f"Borramos los archivos de prueba de {usuario.email}")
        pruebas = Prueba.objects.filter(participante__usuario=usuario,
                                        prueba__contains='/media/')

        for prueba in pruebas:
            Utils.eliminar_archivo(os.path.join(BASE_DIR, prueba.prueba[1:]))

    # Método para borrar los archivos de pruebs de una persona
    def borrar_prueba_reto(usuario, reto):
        logger.info(f"Borramos los archivos de prueba de {usuario.email} del reto "
                    f"{reto.id_reto}")
        pruebas = Prueba.objects.filter(participante__usuario=usuario,
                                        prueba__contains='/media/')

        for prueba in pruebas:
            Utils.eliminar_archivo(os.path.join(BASE_DIR, prueba.prueba[1:]))

    # Método para borrar los retos de una persona
    def borrar_retos(usuario):
        logger.info(f"Borramos los archivos de los retos como coordinador de {usuario.email}")
        retos = Reto.objects.filter(coordinador=usuario)

        for reto in retos:
            Utils.borrar_reto(reto)

    # Método para eliminar los archivos insertados por una persona
    def borrar_persona(usuario):
        logger.info(f"Borramos todos los documentos del usuario {usuario.email}")
        Utils.borrar_prueba(usuario)
        Utils.borrar_animo(usuario)
        Utils.borrar_retos(usuario)

    # Método para crear Notificación de Animador
    @staticmethod
    def notificacion_animador(coordinador, animador, reto):
        notificacion = Notificacion()
        notificacion.categoria = "Reto"
        notificacion.mensaje = f"{coordinador.nombre} te ha invitado a participar como " \
                               f"animador del reto {reto.titulo}. ¿Quieres que " \
                               f"comencemos a apoyar?"
        notificacion.enlace = f'/reto/{reto.id_reto}'
        notificacion.usuario = animador
        notificacion.save()

    @staticmethod
    def notificacion_participante(coordinador, participante, reto):
        notificacion = Notificacion()
        notificacion.categoria = "Reto"
        notificacion.mensaje = f"{coordinador.nombre} te ha invitado a participar " \
                               f"en el reto {reto.titulo}. ¿Comenzamos?"
        notificacion.enlace = f'/reto/{reto.id_reto}'
        notificacion.usuario = participante
        notificacion.save()
