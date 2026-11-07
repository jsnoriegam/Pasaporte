# AppImage Hub

[appimage.github.io](https://appimage.github.io/) es un catálogo comunitario de
AppImages. No aloja binarios: enlaza al release del proyecto y lo prueba en la
LTS más antigua de Ubuntu.

## Enviar Pasaporte

1. Crea el archivo `data/Pasaporte` en un fork de
   [AppImage/appimage.github.io](https://github.com/AppImage/appimage.github.io)
   con una sola línea:

   ```
   https://github.com/jsnoriegam/Pasaporte
   ```

   El archivo `Pasaporte` de esta carpeta ya tiene ese contenido.

2. Abre un PR que añada **solo** ese archivo. Su CI descarga el AppImage del
   release más reciente (o del pre-release más nuevo), lo ejecuta y comenta una
   captura o el error.

3. Si el test falla por la versión de Ubuntu, revisa los requisitos del host en
   el README. Si falla por el nombre del AppImage, añade un sufijo `#` al enlace
   para elegir el archivo concreto.

El archivo de esta carpeta no se envía: es una copia de referencia para no
tener que recordar el formato.
