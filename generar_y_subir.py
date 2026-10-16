import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

def generar_video():
    print("Generando video de 40 segundos con animaciones...")
    
    # 1. Fondo de 40 segundos (Color azul oscuro/grisáceo moderno)
    fondo = ColorClip(size=(1280, 720), color=(15, 23, 42), duration=40)
    
    # 2. Título principal que dura todo el video con efecto de aparición y desvanecimiento
    titulo = (
        TextClip(
            "Automatización con Python\n& GitHub Actions",
            fontsize=50,
            color="white",
            font="Arial",
            align="center"
        )
        .set_position(("center", 200))
        .set_duration(40)
        .crossfadein(2)
        .crossfadeout(2)
    )
    
    # 3. Textos dinámicos que van cambiando según el segundo (animación por intervalos)
    # Primer texto (del segundo 0 al 13)
    texto_1 = (
        TextClip("🚀 Creando videos automáticamente", fontsize=35, color="#38bdf8", font="Arial")
        .set_position(("center", 480))
        .set_start(0)
        .set_duration(13)
        .crossfadein(1)
        .crossfadeout(1)
    )
    
    # Segundo texto (del segundo 13 al 26)
    texto_2 = (
        TextClip("⚙️ Procesando con MoviePy y FFmpeg", fontsize=35, color="#4ade80", font="Arial")
        .set_position(("center", 480))
        .set_start(13)
        .set_duration(13)
        .crossfadein(1)
        .crossfadeout(1)
    )
    
    # Tercer texto (del segundo 26 al 40)
    texto_3 = (
        TextClip("📺 Subida automática a YouTube completada", fontsize=35, color="#f472b6", font="Arial")
        .set_position(("center", 480))
        .set_start(26)
        .set_duration(14)
        .crossfadein(1)
        .crossfadeout(1)
    )
    
    # 4. Unir todos los elementos en un solo video compuesto
    video_final = CompositeVideoClip([fondo, titulo, texto_1, texto_2, texto_3])
    
    # 5. Exportar el video en archivo MP4
    output_filename = "video_generado.mp4"
    video_final.write_videofile(
        output_filename, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac"
    )
    print("¡Video generado con éxito!")
    return output_filename

def subir_a_youtube(video_path):
    print("Iniciando subida a YouTube...")
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    
    # Credenciales obtenidas mediante variables de entorno (GitHub Secrets)
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")
    
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )
    
    youtube = build("youtube", "v3", credentials=creds)
    
    body = {
        "snippet": {
            "title": "Video Automático de 40 Segundos - Proyecto EEST N°1",
            "description": "Video generado y subido automáticamente usando Python, MoviePy y GitHub Actions.",
            "tags": ["python", "automation", "githubactions", "moviepy"],
            "categoryId": "28" # Ciencia y tecnología
        },
        "status": {
            "privacyStatus": "public" # Puede ser 'public', 'unlisted' o 'private'
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = request.execute()
    print(f"¡Video subido con éxito! ID del video: {response.get('id')}")

if __name__ == "__main__":
    archivo_video = generar_video()
    subir_a_youtube(archivo_video)
