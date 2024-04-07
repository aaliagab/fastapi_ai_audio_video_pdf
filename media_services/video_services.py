from moviepy.editor import VideoFileClip

def get_audio_and_save(video_path, audio_output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = None  # Inicializar audio_clip a None

    try:
        # Extraer el audio
        audio_clip = video_clip.audio

        # Guardar el audio en formato WAV
        audio_clip.write_audiofile(audio_output_path, codec='pcm_s16le', fps=44100)

    finally:
        # Cerrar los clips para liberar recursos incluso si hay una excepción
        if audio_clip is not None:
            audio_clip.close()
        video_clip.close()