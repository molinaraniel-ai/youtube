#!/usr/bin/env python3
"""
Sube un vídeo a YouTube (público o no listado).
Requiere las variables de entorno:
  YOUTUBE_CLIENT_ID
  YOUTUBE_CLIENT_SECRET
  YOUTUBE_REFRESH_TOKEN
"""

import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_FILE = Path("output_video.mp4")

def get_authenticated_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=creds)

def upload_video(
    file_path: Path,
    title: str,
    description: str,
    privacy: str = "unlisted",   # "public", "private" o "unlisted"
    category_id: str = "22",     # People & Blogs
):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["automatizado", "github-actions", "python"],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(file_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024 * 8,  # 8 MB
    )

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media,
    )

    print("Subiendo vídeo a YouTube...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Progreso: {int(status.progress() * 100)}%")

    print("¡Subida completada!")
    print(f"ID del vídeo: {response['id']}")
    print(f"URL: https://youtu.be/{response['id']}")
    return response

if __name__ == "__main__":
    if not VIDEO_FILE.exists():
        print(f"Error: no se encuentra {VIDEO_FILE}")
        sys.exit(1)

    privacy = os.environ.get("YOUTUBE_PRIVACY", "unlisted")  # o "public"

    try:
        upload_video(
            file_path=VIDEO_FILE,
            title="Vídeo generado automáticamente con Python + GitHub Actions",
            description=(
                "Este vídeo fue generado y subido de forma completamente automática "
                "usando Python y GitHub Actions.\n\n"
                "Código disponible en el repositorio."
            ),
            privacy=privacy,
        )
    except HttpError as e:
        print(f"Error de la API de YouTube: {e}")
        sys.exit(1)