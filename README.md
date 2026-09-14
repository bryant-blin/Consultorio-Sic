 Documentación del Sistema de Gestión Clínica SIC

## Descripción general

El Sistema de Gestión Clínica SIC es una aplicación web diseñada para administrar las operaciones diarias de un consultorio médico. Permite gestionar pacientes, citas, historial clínico, facturación, catálogo de exámenes y usuarios del sistema. Adicionalmente, incorpora un bot de Telegram que permite a los pacientes agendar citas directamente desde su teléfono y recibir notificaciones sobre el estado de las mismas.

La aplicación puede ejecutarse de dos maneras: como una aplicación de escritorio en Windows mediante una ventana nativa integrada, o como un servicio web alojado en la nube a través de plataformas como Render.

## Arquitectura del proyecto

El proyecto sigue un patrón de arquitectura Modelo-Vista-Controlador adaptado al framework Flask de Python. Los archivos están organizados en carpetas según su responsabilidad dentro de la aplicación.

```
Proyecto/
    principal.py          Punto de entrada principal, define todas las rutas de la aplicación
    lanzador.py           Script que verifica actualizaciones y arranca el ejecutable compilado
    migrate_db.py         Script para migrar datos entre bases de datos
    subir_base_datos.py   Script auxiliar para subir la base de datos a producción
    requirements.txt      Lista de dependencias de Python necesarias
    version.json          Archivo que almacena la versión actual del sistema

    modelo/
        usuarios.py       Definición de todas las tablas de la base de datos (modelos ORM)

    controladores/
        autenticacion.py  Lógica de inicio de sesión, registro y recuperación de contraseña

    servicios/
        bot_telegram.py   Bot de Telegram para interacción con pacientes

    vista/
        *.html            Plantillas HTML para cada página de la interfaz web

    static/               Archivos estáticos como imágenes y hojas de estilo
```

---

## Tecnologías utilizadas

El sistema está construido con las siguientes tecnologías y bibliotecas:

- **Python** como lenguaje de programación principal.
- **Flask** como framework web para manejar las rutas y la lógica del servidor.
- **SQLAlchemy** a través de Flask-SQLAlchemy para la interacción con la base de datos mediante ORM.
- **Flask-Login** para gestionar la autenticación y sesiones de usuario.
- **PostgreSQL** como base de datos relacional, tanto en entorno local como en la nube (Neon).
- **pyTelegramBotAPI** para construir y operar el bot de Telegram.
- **OpenAI / Groq** como proveedor de inteligencia artificial para la funcionalidad de reportes en lenguaje natural.
- **openpyxl** para generar y exportar archivos Excel.
- **BeautifulSoup** para obtener la tasa oficial del dólar desde la página web del Banco Central de Venezuela.
- **pywebview** para mostrar la aplicación web dentro de una ventana de escritorio nativa en Windows.
- **Gunicorn** como servidor de producción para el despliegue en la nube.

---

## Modelo de datos

El archivo `modelo/usuarios.py` define todas las entidades de la base de datos a través de clases de Python que SQLAlchemy traduce a tablas relacionales.

### Usuario

Almacena el perfil personal de cada persona registrada en el sistema. Contiene su nombre, apellidos, correo electrónico y fecha de registro.

### Rol

Define los perfiles de acceso posibles dentro del sistema. Los tres roles que el sistema crea automáticamente al iniciarse son: Administrador, Secretaria y Doctor. El rol de un usuario determina a qué secciones puede acceder.

### Login

Contiene las credenciales de acceso de cada usuario: nombre de usuario, contraseña y estado de actividad. Cada registro de Login está vinculado a un Usuario y a un Rol.

### Historial Medico

Representa el expediente de un paciente. Almacena su cédula de identidad, nombre completo, edad, fecha de nacimiento, teléfono, dirección, sexo, y datos clínicos como altura, peso, tensión arterial, antecedentes médicos, enfermedad actual, indicaciones y observaciones del médico. También registra la fecha en que fue creado el expediente y si fue procesado en un cierre de día.

### Cita

Representa una cita médica agendada. Almacena el nombre y apellido del paciente, su cédula, la fecha y hora de la cita, el motivo de la consulta y el estado de la misma, que puede ser Pendiente, Confirmada o Cancelada. También guarda el identificador de chat de Telegram del paciente para poder notificarle directamente.

### Examen

Representa un servicio o examen que ofrece el consultorio. Tiene nombre, descripción, precio en dólares y pertenece a una categoría.

### Categoria

Agrupa los exámenes bajo una misma denominación para facilitar su organización y búsqueda.

### Factura

Registra cada ítem vendido en el punto de venta. Almacena el nombre del paciente, el examen asociado, el precio cobrado, la fecha de la transacción y un identificador de transacción que agrupa todos los ítems de una misma venta. También tiene un indicador que señala si la factura fue procesada en un cierre de día.

### Pago Detalle

Almacena los métodos de pago utilizados en una transacción. Dado que el punto de venta soporta pagos mixtos, una misma transacción puede tener múltiples registros en esta tabla, uno por cada método de pago utilizado, con su respectivo monto.

### Configuracion

Tabla de una sola fila que almacena la configuración global del sistema. Actualmente guarda la tasa de cambio del dólar obtenida del Banco Central de Venezuela y la fecha de su última actualización.

### Horario Disponible

Almacena los bloques de tiempo habilitados por el administrador para que los pacientes puedan agendar citas. Cada registro tiene una fecha, una hora y un indicador que señala si ese horario ya fue reservado por alguien.

---

## Sistema de autenticación

El archivo `controladores/autenticacion.py` maneja todo lo relacionado con el acceso al sistema.

### Inicio de sesión

El sistema recibe el nombre de usuario y la contraseña desde el formulario de login. Busca el registro en la base de datos y, si las credenciales coinciden, inicia la sesión del usuario utilizando Flask-Login. Si algo falla, muestra un mensaje de error sin especificar cuál campo es incorrecto.

### Registro de nuevos usuarios

El registro de cuentas está protegido por una clave maestra. Para crear una cuenta nueva, el solicitante debe conocer esta clave, lo que impide que cualquier persona pueda registrarse sin autorización previa. Al crearse una cuenta se generan simultáneamente dos registros: el perfil de Usuario con los datos personales y el registro de Login con las credenciales de acceso.

### Recuperación de contraseña

El usuario ingresa su correo electrónico y una nueva contraseña. El sistema busca el perfil asociado a ese correo y actualiza la contraseña directamente en el registro de Login vinculado.

### Control de acceso por rol

La aplicación utiliza un decorador personalizado llamado `roles_required` que protege cada ruta verificando si el usuario actualmente autenticado tiene uno de los roles permitidos. Si no tiene el rol adecuado, es redirigido al dashboard con un mensaje de error.

---

## Rutas y funcionalidades de la aplicación web

El archivo `principal.py` es el núcleo de la aplicación y contiene todas las rutas que la conforman.

### Tasa del Dólar BCV

Al arrancar y de manera periódica desde el frontend, el sistema consulta la página web oficial del Banco Central de Venezuela mediante scraping para obtener la tasa de cambio oficial del dólar. Esta tasa se guarda en la tabla de Configuracion y se inyecta automáticamente en todas las plantillas HTML para que pueda mostrarse en cualquier parte de la interfaz sin necesidad de solicitarla explícitamente en cada ruta.

### Dashboard

La página principal que ve el usuario al iniciar sesión. Muestra contadores generales del sistema: total de citas registradas, total de exámenes en el catálogo, facturas activas del cierre actual y total de pacientes en el sistema. Solo los usuarios autenticados pueden acceder a esta página.

### Analítica e indicadores

El sistema expone un endpoint de programación que la página de reportes consume para mostrar indicadores de negocio en tiempo real. Estos indicadores pueden filtrarse por tres periodos: el día actual, el mes en curso o el año en curso. Los datos que devuelve incluyen el total de ingresos en bolívares y su equivalente en dólares, el ticket promedio por transacción, el conteo de pacientes nuevos y recurrentes, métricas de citas y datos para construir gráficos de uso de exámenes y métodos de pago.

### Punto de Venta

Accesible únicamente para Administrador y Secretaria. Es la pantalla principal de facturación donde se seleccionan los exámenes que se le realizarán al paciente, se indica el nombre del paciente y se registran los métodos de pago. Al validar la venta, el sistema genera un identificador único de transacción y guarda cada ítem y cada método de pago en sus respectivas tablas. Si algún paso falla, revierte todos los cambios para evitar registros incompletos en la base de datos.

### Gestión de Pacientes

Permite listar, buscar, crear, editar y eliminar expedientes de pacientes. La búsqueda funciona por nombre o por número de cédula. El listado completo se ordena alfabéticamente. Tanto la creación como la eliminación de pacientes requieren ser Administrador o Secretaria.

### Catálogo de Exámenes

Accesible para Administrador y Secretaria. Permite administrar el catálogo de servicios que ofrece el consultorio. Cada examen tiene un nombre, una categoría, un precio en dólares y una descripción opcional. El formulario permite crear, editar y eliminar exámenes.

### Reportes y Facturación

Muestra el listado de todas las transacciones del cierre actual, es decir, las que aún no han sido procesadas en un cierre de día. Las ventas se agrupan por su identificador de transacción para mostrar un resumen legible con todos los exámenes realizados, el método de pago utilizado y el total cobrado. Desde esta pantalla se pueden anular transacciones completas y exportar el reporte actual a un archivo Excel con formato visual personalizado. También es posible ejecutar el cierre de día, que marca todas las transacciones y los nuevos pacientes como procesados, dejando la vista limpia para el día siguiente.

### Historial Clínico

Accesible para Administrador y Doctor. Permite buscar pacientes por nombre o cédula y acceder a su ficha clínica completa. Desde la ficha se puede editar toda la información del paciente, incluyendo datos personales y clínicos como antecedentes, enfermedad actual, indicaciones del médico y observaciones. También hay una pantalla de visor 3D asociada a la ficha de cada paciente.

### Gestión de Citas

Muestra el listado de todas las citas ordenadas cronológicamente. Permite crear nuevas citas ingresando los datos del paciente, la fecha, la hora y el motivo. Al crear una cita, el sistema verifica que no exista otra cita para exactamente el mismo horario y envía una notificación automática al canal de administración del bot de Telegram. Las citas pueden editarse, confirmarse o cancelarse. Cuando el estado de una cita cambia, si el paciente agendó a través del bot de Telegram, recibe automáticamente un mensaje informándole sobre el cambio.

### Gestión de Horarios

Accesible únicamente para el Administrador. Presenta un calendario interactivo donde el administrador puede generar bloques de tiempo disponibles para que los pacientes elijan al agendar una cita por el bot de Telegram. El sistema sabe qué zonas horarias son válidas, evita generar horarios en el pasado y no permite eliminar horarios que ya están reservados.

### Gestión de Usuarios

Exclusivo para el Administrador. Muestra el listado de todos los usuarios del sistema con su nombre, nombre de usuario, rol y estado. Desde esta pantalla el administrador puede editar los datos de cualquier usuario, cambiar su rol, bloquear o desbloquear su acceso y eliminar su cuenta. El sistema impide que un administrador se bloquee o elimine a sí mismo.

---

## Bot de Telegram

El archivo `servicios/bot_telegram.py` implementa un bot de Telegram que corre en un hilo de ejecución paralelo al servidor web, de modo que ambos funcionan simultáneamente sin interferirse.

### Flujo de registro de pacientes

Cuando un paciente escribe al bot por primera vez, se le solicita su número de cédula. Si la cédula existe en la base de datos, el sistema lo reconoce y le muestra el menú principal. Si no existe, inicia un proceso de registro en el que se le solicita su nombre completo, edad y número de teléfono. Antes de guardar los datos, el bot muestra un resumen y permite al paciente corregir cualquier campo si cometió un error. Una vez confirmados, el registro queda guardado en la base de datos.

### Flujo de agendamiento de citas

Desde el menú principal del bot, el paciente puede seleccionar la opción de agendar una cita. El bot le presenta un calendario interactivo con el que puede elegir el mes y el día que desea. Luego se le muestran únicamente los horarios que el administrador ha habilitado previamente para ese día. El paciente selecciona uno, escribe el motivo de su consulta y el bot registra la cita automáticamente en la base de datos. Al mismo tiempo, marca ese horario como ocupado para que no pueda ser elegido por otro paciente y envía una notificación al canal de administración informando sobre la nueva cita.

### Consulta y cancelación de citas

El paciente puede escribir el comando de su cita para ver los detalles de su próxima cita activa. Desde esa misma pantalla puede solicitar su cancelación pulsando un botón. Si cancela, el sistema actualiza el estado de la cita y notifica al canal de administración.

### Reportes inteligentes mediante inteligencia artificial

El bot ofrece una función de reportes donde el paciente o el personal puede escribir una consulta en lenguaje natural. El sistema consulta el esquema de la base de datos, se lo envía a un modelo de inteligencia artificial que genera automáticamente la consulta SQL equivalente, ejecuta esa consulta en la base de datos y devuelve los resultados en un archivo Excel directamente en el chat de Telegram.

### Comandos disponibles para el personal

El bot incluye comandos especiales para el personal del consultorio. El comando de citas para hoy muestra un listado ordenado por hora de todas las citas agendadas para el día actual. El comando de reporte activa el flujo de consultas en lenguaje natural. El comando de identificacion permite conocer el identificador de chat de Telegram de cualquier cuenta, lo cual es útil para configurar el sistema.

### Notificaciones bidireccionales

El bot puede notificar al canal de administración de la clínica sobre eventos importantes como nuevas citas o cancelaciones. También puede notificar directamente a los pacientes cuando el personal confirma o cancela una cita desde la interfaz web.

---

## Inicialización del sistema

El sistema usa una estrategia de inicialización diferida. En lugar de ejecutar tareas al arrancar el servidor, espera a que llegue la primera solicitud real antes de crear las tablas de la base de datos, verificar que los roles existan y arrancar el hilo del bot de Telegram. Esto evita problemas de tiempo de espera en entornos en la nube donde el servidor puede tardar en estar listo.

---

## Modos de ejecución

### Modo escritorio

Cuando se ejecuta localmente en Windows sin ninguna variable de entorno especial, la aplicación arranca Flask en el puerto 5000 en un hilo secundario y abre una ventana de escritorio nativa a través de pywebview que apunta a esa dirección local. Esto hace que la aplicación se comporte como un programa de escritorio convencional, con su propio ícono y ventana, aunque internamente funcione como una aplicación web.

### Modo nube

Cuando se detecta la variable de entorno que indica que el sistema está corriendo en un servidor como Render, la aplicación arranca directamente como servidor web sin abrir ventana gráfica. La base de datos se conecta a través de una URL de entorno en lugar de las credenciales locales.

---

Script de actualización automatica

El archivo `lanzador.py` es un script independiente pensado para distribuirse junto al ejecutable compilado. Al ejecutarse, consulta un servidor remoto para comparar la versión instalada con la versión más reciente disponible. Si detecta una versión más nueva, la descarga automáticamente y reemplaza el ejecutable actual. Una vez completada la verificación, sea o no necesaria una actualización, arranca el ejecutable principal del sistema.

Configuracion de la base de datos

El sistema detecta automáticamente si debe usar la base de datos local o la de la nube. Si existe la variable de entorno `DATABASE_URL`, la usa directamente y se asegura de que tenga el formato correcto que PostgreSQL requiere y que la conexión sea segura mediante SSL. Si esa variable no existe, conecta a una base de datos PostgreSQL local con las credenciales configuradas directamente en el código.

Dependencias

| Biblioteca | Uso |
|---|---|
| flask | Framework web principal |
| flask-sqlalchemy | Integración de SQLAlchemy con Flask |
| flask-login | Manejo de sesiones y autenticación |
| psycopg2-binary | Conector de PostgreSQL para Python |
| requests | Peticiones HTTP para scraping del BCV |
| beautifulsoup4 | Análisis del HTML del BCV |
| openpyxl | Generación de archivos Excel |
| pyTelegramBotAPI | Cliente para la API de Telegram |
| python-telegram-bot-calendar | Componente de calendario para el bot |
| gunicorn | Servidor WSGI para producción en la nube |
| python-dotenv | Carga de variables de entorno desde archivos .env |
| openai | Cliente compatible con la API de Groq para IA |
