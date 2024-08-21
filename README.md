# 🚀 Auto-WordPress Generator with Gemini 🤖

Este proyecto contiene un script en Python que se ejecuta automáticamente cada 3 horas para subir artículos a un sitio web de WordPress. El script utiliza **Gemini**, la potente IA de Google, para generar contenido de alta calidad.

## 📝 Descripción

Este script ha sido diseñado para automatizar la publicación de artículos en WordPress. Cada 3 horas, se ejecuta el script que:

1. 🧠 Genera artículos optimizados para SEO usando la IA Gemini de Google.
2. 📷 Genera imágenes de calidad y las incluye en el artículo.
3. 🌐 Sube automáticamente el contenido a un sitio web de WordPress.
4. ⏲️ Gestiona la programación de publicaciones de manera eficiente.

## 🚀 Características

- **Automatización completa**: Publicaciones automáticas cada 3 horas.
- **Contenido generado por IA**: Aprovecha la inteligencia artificial de Google Gemini para crear artículos de alta calidad.
- **Integración con WordPress**: Subida y publicación automática en WordPress.

## ⚙️ Instalación

Para ejecutar este proyecto en tu entorno local, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/alexcerezo/wordpress-article-generator.git
   cd wordpress-article-generator
   
2. **Configurar el repositorio**
   Configura las Workflow permissions para que puedan leer y escribir:
   Entra en Settings >> Actions -> Workflow permissions y selecciona Read and write permissions

3. **Configura los secretos**
   Configura los secretos de las Actions para que se puedan ejecutar de manera correcta. Entra en Settings >> Secrets and variables >> Actions y añade los siguientes secretos:
   WORDPRESS_URL=https://tudominio.com/wp-json/wp/v2/posts
   WORDPRESS_TOKEN=XXXX XXXX XXXX XXXX XXXX XXXX
   WORDPRESS_USERNAME=username
   GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   RSS_URL=https://undominio.com/feed

## 🧠 Recursos adicionales

  [¿Cómo crear una aplicación en WordPress?](https://wordpress.com/es/support/seguridad/autenticacion-en-dos-pasos/application-specific-passwords/)
  [¿Cómo conseguir la API key de Gemini?](https://docs.aicontentlabs.com/es/articulos/clave-api-google-gemini/)
  [¿Cómo conseguir el RSS feed de una página?](https://rss.com/blog/como-encontrar-un-feed-rss/#:~:text=En%20el%20c%C3%B3digo%20HTML%20se,entre%20comillas%20despu%C3%A9s%20de%20href%3D.)

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas o mejoras, siéntete libre de abrir un issue o enviar un pull request.

## 📝 Licencia

Este proyecto está licenciado bajo la **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**.

- **Uso personal**: Puedes utilizar el software para fines personales o educativos.
- **No comercial**: No se permite el uso comercial del software bajo ninguna circunstancia.
- **No modificaciones**: No se permite la redistribución ni la creación de obras derivadas basadas en este software salvo autorazación previa.


