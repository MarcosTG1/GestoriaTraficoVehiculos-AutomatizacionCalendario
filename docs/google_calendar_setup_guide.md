# Guía de Configuración de Google Calendar API

Para poder modificar eventos en un Google Calendar específico mediante scripts, necesitas configurar un proyecto en Google Cloud y obtener las credenciales adecuadas.

## Paso 1: Crear un Proyecto en Google Cloud
1. Ve a la [Consola de Google Cloud](https://console.cloud.google.com/).
2. Haz clic en el selector de proyectos en la parte superior izquierda y selecciona **"Nuevo Proyecto"**.
3. Dale un nombre (ej. `GestoriaCalendario`) y haz clic en **"Crear"**.

## Paso 2: Habilitar la API de Google Calendar
1. En el menú lateral, ve a **"APIs y servicios"** > **"Biblioteca"**.
2. Busca **"Google Calendar API"**.
3. Haz clic en el resultado y luego en **"Habilitar"**.

## Paso 3: Configurar la Pantalla de Consentimiento OAuth
1. Ve a **"APIs y servicios"** > **"Pantalla de consentimiento de OAuth"**.
2. Selecciona **"Externo"** (o "Interno" si tienes una organización de Google Workspace) y haz clic en **"Crear"**.
3. Rellena los campos obligatorios:
   - **Nombre de la aplicación**: `GestoriaCalendario`
   - **Correo de asistencia del usuario**: Tu correo.
   - **Información de contacto del desarrollador**: Tu correo.
4. Haz clic en **"Guardar y continuar"**.
5. En **"Permisos"**, haz clic en **"Añadir o quitar permisos"**.
6. Busca y selecciona el permiso: `.../auth/calendar` (Ver, editar, compartir y eliminar permanentemente todos los calendarios que usen Google Calendar).
7. Haz clic en **"Actualizar"**, luego en **"Guardar y continuar"**.
8. En **"Usuarios de prueba"**, añade tu correo electrónico (el de la cuenta que quieres modificar). Esto es crucial mientras la app no esté verificada.
9. Guarda y vuelve al panel.

## Paso 4: Crear Credenciales (OAuth 2.0 Client ID)
Este método es ideal si el script actuará en nombre de un usuario específico (tú).

1. Ve a **"APIs y servicios"** > **"Credenciales"**.
2. Haz clic en **"Crear credenciales"** > **"ID de cliente de OAuth"**.
3. En **"Tipo de aplicación"**, selecciona **"Aplicación de escritorio"**.
4. Ponle un nombre (ej. `ScriptPython`) y haz clic en **"Crear"**.
5. Aparecerá una ventana con tu "ID de cliente" y "Secreto de cliente". Haz clic en **"Descargar JSON"**.
6. Guarda este archivo como `credentials.json` en la carpeta `secrets/` de tu proyecto.

## Paso 5: Autenticación en el Script
El script necesitará usar este `credentials.json` para solicitar un "token" la primera vez.
1. Al ejecutar el script por primera vez, se abrirá una ventana del navegador pidiéndote permiso.
2. Acepta los permisos.
3. Se generará un archivo `token.json` automáticamente, que permitirá al script ejecutarse en el futuro sin pedir permiso de nuevo (hasta que expire).

---

**Nota**: Si prefieres usar una "Cuenta de Servicio" (Service Account) para no depender de tu usuario personal, el proceso es diferente y requiere compartir tu calendario con el email de la cuenta de servicio. Para scripts personales, OAuth 2.0 (lo descrito arriba) es lo más sencillo y seguro.
