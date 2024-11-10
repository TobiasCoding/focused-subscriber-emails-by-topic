# Envío automático de correos electrónicos a suscriptores, focalizados por categoría

Este proyecto facilita la automatización del envío de correos electrónicos con noticias temáticas a una lista de suscriptores. El código permite procesar y clasificar las noticias obtenidas de las alertas de Google según categorías. En su versión actual, clasifica las noticias en dos grupos: "electoral" y "no electoral". Sin embargo, se planea hacer que el sistema sea más flexible, de manera que el usuario pueda añadir un número indefinido de categorías.

Para el envío y procesamiento de los correos, se utiliza una cuenta de Gmail que reenvía automáticamente las noticias a una cuenta de Yandex, desde la cual se accede al correo mediante IMAP para su análisis. Debido a limitaciones en el envío de correos desde Yandex a través de código, se recurre a Brevo como plataforma de distribución de los mails.

El proyecto está diseñado para ejecutarse en Google Colab, permitiendo su uso por usuarios en redes corporativas con restricciones administrativas y sin permisos de instalación adicionales.


## Uso

1.  Descargar el repositorio
```bash
git clone https://github.com/TobiasCoding/focused-subscriber-emails-by-topic.git
```
2. Ingresar al directorio
```bash
cd focused-subscriber-emails-by-topic
```
3. Crear cuenta en Yandex y obtener API KEY.
4. Crear cuenta en Brevo y obtener API KEY.
5. Modificar el código de `main.py` para definir tu correo y API KEYs obtenidas.
```bash
nano main.py
```
6. Configurar según tus preferencias el archivo `build_databases.py`
```
nano build_databases.py
```
7. Ejecuta el archivo principal (`main.py`).
```bash
python main.py
```
**Selección de Opciones**: Durante la ejecución, podrás elegir opciones como:
   - Enviar correos electorales o no electorales.
   - Enviar a destinatarios específicos o hacer pruebas.
**Envío de Correos**: Tras seleccionar las opciones, los correos se enviarán automáticamente según los destinatarios y categorías configuradas.
