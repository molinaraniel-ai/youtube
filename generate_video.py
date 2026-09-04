#!/usr/bin/env python3
"""
Genera un vídeo MP4 de más de 5 minutos.
"""

from moviepy.editor import (
    TextClip, CompositeVideoClip, ColorClip, AudioFileClip, concatenate_videoclips
)
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
from pathlib import Path

OUTPUT = Path("output_video.mp4")
DURATION = 370          # segundos (> 5 min)
FPS = 24
SIZE = (1280, 720)

def make_tone(duration, freq=440, fps=44100):
    """Genera un tono simple como audio de fondo."""
    t = np.linspace(0, duration, int(fps * duration), endpoint=False)
    wave = 0.1 * np.sin(2 * np.pi * freq * t)
    # Estéreo
    stereo = np.column_stack([wave, wave])
    return AudioArrayClip(stereo, fps=fps)

def create_video():
    print("Generando vídeo...")

    # Fondo negro
    background = ColorClip(size=SIZE, color=(10, 10, 30), duration=DURATION)

    # Texto principal que cambia cada 30 segundos
    clips = []
    segment = 30
    for i in range(0, DURATION, segment):
        end = min(i + segment, DURATION)
        txt = (
            f"Vídeo generado automáticamente\n"
            f"Segmento {i//segment + 1}\n"
            f"Tiempo: {i//60:02d}:{i%60:02d}"
        )
        txt_clip = (
            TextClip(
                txt,
                fontsize=50,
                color="white",
                font="DejaVu-Sans",
                size=SIZE,
                method="caption",
                align="center",
            )
            .set_start(i)
            .set_duration(end - i)
            .set_position("center")
        )
        clips.append(txt_clip)

    # Contador de segundos en la esquina
    def make_timer(t):
        mins, secs = divmod(int(t), 60)
        return f"{mins:02d}:{secs:02d}"

    timer = (
        TextClip("00:00", fontsize=40, color="cyan", font="DejaVu-Sans")
        .set_duration(DURATION)
        .set_position(("right", "top"))
    )
    # Actualizamos el timer frame a frame (más eficiente con un clip dinámico)
    timer = timer.set_make_frame(
        lambda t: TextClip(
            make_timer(t),
            fontsize=40,
            color="cyan",
            font="DejaVu-Sans",
        ).get_frame(0)
    )

    final = CompositeVideoClip([background] + clips + [timer])
    final = final.set_audio(make_tone(DURATION, freq=220))

    print(f"Escribiendo {OUTPUT} ({DURATION}s)...")
    final.write_videofile(
        str(OUTPUT),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium",
        logger=None,          # menos ruido en Actions
    )
    print("Vídeo generado correctamente.")
    return OUTPUT

if __name__ == "__main__":
    create_video()