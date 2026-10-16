import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from moviepy import ColorClip, TextClip, CompositeVideoClip

def generar_video():
    print("Generando video de 40 segundos con animaciones...")
    
    # 1. Fondo de 40 segundos (Color azul oscuro/grisáceo moderno)
    fondo = ColorClip(size=(1280, 720), color=(15, 23, 42), duration=40)
    
    # 2. Título principal usando un método compatible con ImageMagick
    titulo = (
        TextClip(
            text="Automatizacion con Python\n& GitHub Actions",
            font_size=50,
            color="white",
            method="caption",
            size=(1100, 200)
        )
        .with_position(("center", 200))
        .with_duration(40)
        .crossfadein(2)
        .crossfadeout(2)
    )
    
    # 3. Textos dinámicos por intervalos
    texto_1 = (
        TextClip(text="Creando videos automaticamente", font_size=35, color="#38bdf8", method="caption", size=(1000, 100))
        .with_position(("center", 480))
        .with_start(0)
        .with_duration(13)
        .crossfadein(1)
        .crossfadeout(1)
    )
    
    texto_2 = (
        TextClip(text="Procesando con MoviePy y FFmpeg", font_size=35, color="#4ade80", method="caption", size=(1000, 100))
        .with_position(("center", 480))
        .with_start(13)
        .with_duration(13)
        .crossfadein(1)
        .crossfadeout(1)
    )
    
    texto_3 = (
        TextClip(text="Subida automatica a YouTube completada", font_size=35, color="#f472b6", method="caption", size=(1000, 100))
        .with_position(("center", 480))
        .with_start(26)
        .with_duration(14)
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
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public"
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
