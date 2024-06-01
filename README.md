# AdbHammer

ADB Commander es una herramienta GUI para la gestión de dispositivos Android mediante ADB (Android Debug Bridge). Esta aplicación permite realizar diversas operaciones en dispositivos Android de manera sencilla y eficiente.

## Características

- **Conectar Dispositivo**: Conecta tu dispositivo Android al ordenador.
- **Listar Archivos**: Lista los archivos en el almacenamiento del dispositivo.
- **Instalar APK**: Instala archivos APK en el dispositivo.
- **Capturar Pantalla**: Captura una captura de pantalla del dispositivo.
- **Reiniciar Dispositivo**: Reinicia el dispositivo Android.
- **Enviar Archivos**: Envía archivos desde el ordenador al dispositivo.
- **Recuperar Archivos**: Recupera archivos desde el dispositivo al ordenador.
- **Información del Dispositivo**: Muestra información detallada del dispositivo.
- **Desinstalar Aplicación**: Desinstala una aplicación del dispositivo.
- **Finalizar Aplicación**: Finaliza una aplicación en ejecución.
- **Iniciar Aplicación**: Inicia una aplicación especificada.
- **Reiniciar Aplicación**: Reinicia una aplicación.
- **Borrar Datos de Aplicación**: Borra los datos de una aplicación.
- **Borrar Datos y Reiniciar Aplicación**: Borra los datos de una aplicación y la reinicia.
- **Iniciar Aplicación con Depurador**: Inicia una aplicación con el depurador adjunto.
- **Reiniciar Aplicación con Depurador**: Reinicia una aplicación con el depurador adjunto.
- **Otorgar Permisos**: Otorga permisos específicos a una aplicación.
- **Revocar Permisos**: Revoca permisos específicos de una aplicación.
- **Habilitar/Deshabilitar Wi-Fi**: Habilita o deshabilita la conectividad Wi-Fi.
- **Habilitar/Deshabilitar Datos Móviles**: Habilita o deshabilita la conectividad de datos móviles.

## Requisitos

- Python 3.x
- PyQt5
- ADB (Android Debug Bridge)

## Instalación

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tu_usuario/adb-commander.git
    cd adb-commander
    ```

2. **Instalar dependencias**:
    ```bash
    pip install pyqt5
    ```

3. **Configurar ADB**:
    - Descarga las herramientas de plataforma de Android SDK desde [aquí](https://developer.android.com/studio/releases/platform-tools) y asegúrate de que `adb` esté en tu PATH.

4. **Ejecutar la aplicación**:
    ```bash
    python adb_gui.py
    ```

## Uso

1. **Conectar el dispositivo**: Conecta tu dispositivo Android al ordenador mediante un cable USB y habilita la depuración USB.
2. **Ejecutar ADB Commander**: Sigue los pasos de instalación y ejecución mencionados anteriormente.
3. **Usar la GUI**: Utiliza la interfaz gráfica para realizar las operaciones deseadas en tu dispositivo Android.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio importante.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

¡Gracias por usar ADB Commander!
