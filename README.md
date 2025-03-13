# Proyecto de Automatización de Pruebas Móviles

## Estructura del Proyecto

```
📂 Proyecto
│-- 📂 APK                 # Contiene el archivo APK de la aplicación
│-- 📂 config              # Contiene el archivo capabilities.json con la configuración de Appium
│-- 📂 features            # Contiene los archivos .feature de Cucumber
│-- 📂 steps               # Contiene los steps definidos en Python para ejecutar las pruebas
│-- 📂 utils               # Contiene screenshot_helper.py y reporte
│   │-- screenshot_helper.py  # Función para capturas de pantalla
│   │-- reporte             # Carpeta donde se almacenan los reportes de ejecución
│-- 📄 README.md           # Documentación del proyecto
│-- 📄 requirements.txt    # Lista de dependencias necesarias
```

## Instalación y Configuración

### Requisitos Previos

Asegúrate de tener instalados los siguientes programas en tu sistema:

- [Python 3.12](https://www.python.org/downloads/)
- [Appium Server](https://appium.io/)
- [Node.js y npm](https://nodejs.org/)
- [Java JDK 17+](https://www.oracle.com/java/technologies/javase-jdk17-downloads.html)
- [Android SDK y ADB](https://developer.android.com/studio)

### Instalación de Dependencias

1. Clona el repositorio del proyecto:
   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_PROYECTO>
   ```

2. Crea un entorno virtual y actívalo:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias del proyecto:
   ```sh
   pip install -r requirements.txt
   ```

4. Instala Appium y sus drivers:
   ```sh
   npm install -g appium
   appium driver install uiautomator2
   ```

### Configuración de Appium

1. Asegúrate de que Appium esté ejecutándose:
   ```sh
   appium
   ```
2. Configura el archivo `config/capabilities.json` con los detalles del dispositivo y la aplicación.

### Ejecución de Pruebas

Para ejecutar las pruebas con Behave (Cucumber en Python), usa el siguiente comando:
```sh
behave features/
```

Si deseas generar un reporte en formato JSON:
```sh
behave -f json -o utils/reporte/report.json
```

### Capturas de Pantalla
Las capturas de pantalla se generan en los respectivos steps y se almacenan en `screenshots/`.

---
¡Listo! Ahora puedes ejecutar las pruebas automatizadas en tu dispositivo o emulador Android. 🚀

