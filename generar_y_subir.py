import os
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from moviepy.editor import ColorClip, CompositeVideoClip

def crear_video():
    print("Generando el video automáticamente...")
    # Crear un fondo verde de 5 segundos de duración (resolución 1280x720)
    video = ColorClip(size=(1280, 720), color=(0, 128, 0), duration=5)
    
    nombre_archivo = "resultado_messi.mp4"
    video.write_videofile(nombre_archivo, fps=24, codec='libx264', audio=False)
    print(f"¡Video generado con éxito: {nombre_archivo}!")
    return nombre_archivo

def subir_video(video_file):
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Faltan credenciales en las variables de entorno.")

    credentials = google.oauth2.credentials.Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    if not os.path.exists(video_file):
        raise FileNotFoundError(f"No se encontró el archivo {video_file}")

    body = {
        "snippet": {
            "title": "Resultado Messi ⚽ (Generado Automáticamente)",
            "description": "Video generado por código Python y subido mediante GitHub Actions.",
            "tags": ["Messi", "Python", "AutoUpload"],
            "categoryId": "17"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"Iniciando subida de {video_file} a YouTube...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Progreso de subida: {int(status.progress() * 100)}%")

    print(f"\n¡Video subido exitosamente!")
    print(f"Enlace al video: https://youtu.be/{response.get('id')}")

if __name__ == "__main__":
    video_generado = crear_video()
    subir_video(video_generado)
