import requests
import xml.etree.ElementTree as ET
import os

# --- CONFIGURACIÓN ---
# URL del feed RSS de Google Trends para Argentina
RSS_URL = "https://trends.google.com.ar/trending/rss?geo=AR"
# Lee la URL del Webhook desde el secreto de GitHub
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
# --- FIN DE CONFIGURACIÓN ---

def get_rss_titles():
    """Obtiene los titulares del feed RSS y devuelve una lista de títulos."""
    try:
        response = requests.get(RSS_URL)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = root.findall('./channel/item')

        titles = []
        for item in items:
            title_element = item.find('title')
            if title_element is not None:
                titles.append(title_element.text)

        return titles

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el feed RSS: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error al analizar el XML del feed: {e}")
        return []

def send_to_slack_via_webhook(message):
    """Envía un mensaje a Slack usando un Webhook."""
    try:
        payload = {
            "text": message
        }
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"Mensaje enviado a Slack: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar a Slack: {e}")

def main():
    """Función principal que ejecuta el proceso."""
    print("\nVerificando nuevos titulares...")

    new_titles = get_rss_titles()

    if new_titles:
        for title in new_titles:
            send_to_slack_via_webhook(f"Nuevo en Google Trends: *{title}*")
        print("\nVerificación de titulares completada.")
    else:
        print("No se encontraron titulares o hubo un error.")

if __name__ == "__main__":
    main()
