import feedparser
import requests
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import google.generativeai as genai
import base64
import random

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de WordPress
wordpress_url = os.getenv('WORDPRESS_URL')
token = os.getenv('WORDPRESS_TOKEN')
username = os.getenv('WORDPRESS_USERNAME')

# Configuración de Google Gemini

gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)

# URL del feed RSS
rss_url = os.getenv('RSS_URL')

# Archivo para guardar los elementos del feed
feed_file = 'feed_data.json'

def load_saved_entries(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_entries(file_path, entries):
    with open(file_path, 'w') as f:
        json.dump(entries, f)

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    contents = soup.select('div.group')
    return "\n".join([content.get_text() for content in contents])

def find_unsplash_image(keywords):
    keywords = keywords.split(', ')

    # Buscar una imagen en Unsplash hasta encontrar una que coincida con las palabras clave
    image_url = None
    i = 0
    while not image_url and i < len(keywords):
        image_url = search_unsplash_image(keywords[i])
        i += 1
    return image_url

def search_unsplash_image(keywords):
    query = keywords.replace(' ', '+')
    url = f"https://api.unsplash.com/search/photos?query={query}&orientation=landscape&client_id=apQpOGqco6XHKd01ojCMu5H-qqGCErP1UHL5iivhxGA"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            # Numero random entre 0 y 9
            random_number = random.randint(0, 9)
            return data['results'][random_number]['urls']['full']
    return None


def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        ## Save the content into a jpg file into images folder
        image_folder = 'images'
        image_filename = 'image.jpg'

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        image_path = os.path.join(image_folder, image_filename)

        with open(image_path, 'wb') as f:
            f.write(response.content)
        return response.content
    return None

def header(user, password):
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    header_json = {'Authorization': 'Basic ' + token.decode('utf-8')}
    return header_json

def upload_image_to_wordpress(image_path, site_url, headers, alt_text, title):
    media_endpoint = site_url + 'wp-json/wp/v2/media'
    with open(image_path, 'rb') as img:
        file_name = os.path.basename(image_path)
        files = {'file': (file_name, img, 'image/jpeg')}
        data = {
            'alt_text': alt_text,
            'title': title
        }
        response = requests.post(media_endpoint, headers=headers, files=files, data=data)
        if response.status_code == 201:
            response_json = response.json()
            return response_json.get('id')
        else:
            print(f"Error uploading image: {response.status_code} - {response.text}")
            return None

def create_wordpress_post(title, content, slug, keywords, id):
    post_data = {
        'title': title,
        'content': content,
        'status': 'publish', # Cambiar a 'publish' para publicar el post y 'draft' para guardarlo como borrador
        'slug': slug,
        'featured_media': id,
    }
    response = requests.post(wordpress_url, json=post_data, auth=(username, token))
    if response.status_code == 201:
        print('Post creado exitosamente.')
        print(response.json())
        return True
    else:
        print(f'Error al crear el post: {response.status_code}')
        print(response.json())
        return False

def process_feed_entry(entry, saved_entries):
    print(f"Nuevo elemento encontrado: {entry.title}")
    # Obtener el contenido del artículo
    article_text = fetch_article_content(entry.link)
    if article_text:

        # Traducir el contenido del artículo
        model = genai.GenerativeModel('gemini-1.5-flash')
        translated_text = model.generate_content("Imagínate que eres un traductor experto nativo en ingles y español. Te encargan la tarea de traducir un articulo, pero te exigen que solo devuelvas el cuerpo, es decir no debes incluir título. Además, debes usar formato markdown para hacer más intuitivo el formato del texto. Ahora una ves has entendido este contexto, traduce TODO el texto siguiendo las ordenes que te dicho, no puedes dejar nada sin traducir: " + entry.title + article_text)
        print("Texto traducido: ", translated_text.candidates[0].content.parts[0].text)

        # Optimizar el contenido para SEO
        seo_optimized_text = model.generate_content("Imagina que eres un experto en posicionamiento SEO y tu compañero de traducción te ha pasado un artículo. Compruebas que el artículo parece estar bien pero que no esta optimizado para posicionarse de manera correcta. Entonces te pones manos a la obra y decides optimizar el artículo. Para ello haces uso de las reglas básicas de SEO y legibilidad. Primero seleccionas unas palabras clave, y te aseguras de que aparezcan el título, al menos 4 veces a lo largo del artículo y más de uno de los subtítulos. No incluyas enlaces, nunca. Más tarde diseñas el título, el slug y la meta descripción, todos deben contener la o las palabras clave y no ser demasiado largos, ya que es perjudicial. Por último te aseguras de que la legibilidad sea correcta y entre otra medidas sigues la regla del 25, que consiste en que no más del 25% de las frases, pueden contener más de 25 palabras, es decir acorta las frases si es necesario. Además, no puede haber más de 300 palabras entre subtítulo y subtítulo. Una vez finalizado, respetarás el formato markdown de tu compañero de traducción e incluirás una pequeñas lista al final del artículo con la o las palabras clave, el título, el slug y la meta descripción. No uses dos puntos al final de los subtítulos. Aquí tienes el artículo, que no se te olvide ningún paso ni dejes el texto por la mitad: " + translated_text.candidates[0].content.parts[0].text)

        # Elimina los hastags y asteriscos del texto
        seo_optimized_text = seo_optimized_text.candidates[0].content.parts[0].text
        print("Texto SEO optimizado: ", seo_optimized_text)

        # Obtener los elementos SEO
        if 'clave:' in seo_optimized_text:
            keywords = seo_optimized_text.split('clave:**')[1]
            keywords = keywords.split('**')[0]
            keywords = keywords.replace('.', '')
        if 'tulo:' in seo_optimized_text:
            title = seo_optimized_text.replace('#', '').replace('*', '').split('tulo:')[1]
            if 'slug' in title:
                title = title.split('slug')[0]
            if 'Slug' in title:
                title = title.split('Slug')[0]
        if 'lug:' in seo_optimized_text:
            slug = seo_optimized_text.replace('#', '').replace('*', '').split('lug:')[1]
            slug = slug.split(' ')[0]
        print("SEO items: ", keywords, title, slug)

        # Descargar imagen de Unsplash
        image_url = find_unsplash_image(keywords)
        download_image(image_url)
        print("Imagen descargada.")

        # Subir la imagen a WordPress
        hed = header(username,token) #username, application password                       
        id = upload_image_to_wordpress('images/image.jpg', 'https://alexcerezo.es/',hed, title, keywords)
        print("Imagen subida a WordPress")

        # Generar contenido HTML
        model = genai.GenerativeModel('gemini-1.5-pro')
        html_text = model.generate_content("Imagina que eres el encargado de subir a wordpress los artículos de tu periódico, pero tu eres más listo. Has decidido tomar los artículos que te comparte tu compañero de seo en formato markdown, y automatizar su subida a wordpress. Para ello necesitas transformar este texto en formato markdown en html y necesitas diferenciar entre el título, párrafos y subtítulos. Por lo tanto transforma este artículo en html, no hace falta que generes ningún texto adicional únicamente lo que te envía tu compañero de SEO. Tu código NO DEBE contener el título, ya que lo añadirá tu compañero a wordpress más tarde, en otras palabras elimínalo. Nunca pongas un subtitulo al principio, empieza SIEMPRE con un párrafo. No incluyas enlaces, tu compañero lo hará más tarde. Aquí tienes el texto que te han compartido, no dejes el texto a medias: " + seo_optimized_text)
        print("Contenido HTML generado: ", html_text.candidates[0].content.parts[0].text)

        # Generar contenido HTML con formato
        formatted_html_text = model.generate_content('Estás a punto de subir el código de tu artículo a wordpress pero ups, te das cuenta de que el texto tiene poca gracia. Así que decides modificar el código para añadir texto en cursiva y/o negrita en las partes más importantes de cada párrafo. No tengas miedo a añadir formato, si no el texto se verá muy plano, añade al menos 3 modificaciones de formato por párrafo pero a veces negrita, a veces cursiva y otras veces ambas, no tienes porque usarlas todas a la vez. No puedes modificar nada más a parte del formato, ya que desestructuraras el código y/o el contenido, por lo tanto no añadas etiquetas que no estén relacionadas con el formato. No añadas "```html" al principio ni nada parecido porque corrompe el texto. Pon los enlaces SIEMPRE subrayados, en negrita, y sin el texto en azul que tan desagradable. Aquí tienes el código y por favor, no dejes el texto a medias: ' + html_text.candidates[0].content.parts[0].text)
        print("Contenido HTML con formato: ", formatted_html_text.candidates[0].content.parts[0].text)

        # Generar todo el articulo
        article = '<div><img src="' + image_url + '" alt="' + title + '" style="width: 100%;">' + formatted_html_text.candidates[0].content.parts[0].text.replace('#', '').replace('*', '') + '<p><strong><a href="' + entry.link + '">Fuente</a></strong></p></div>'
        
        # Crear el post en WordPress
        if create_wordpress_post(title, article, slug, keywords, id):
            saved_entries.append(entry.id)
            save_entries(feed_file, saved_entries)
    else:
        print("No se pudo encontrar el contenido del artículo.")


def main():
    feed = feedparser.parse(rss_url)
    saved_entries = load_saved_entries(feed_file)
    if feed.entries:
        last_entry = feed.entries[0]
        if last_entry.id not in saved_entries:
            process_feed_entry(last_entry, saved_entries)
        else:
            print("El último elemento ya está guardado.")
    else:
        print("No se encontraron elementos en el feed.")

if __name__ == "__main__":
    main()
