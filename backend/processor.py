import os
import subprocess

def process_video(input_path: str, output_path: str):
    """
    Повна унікалізація відео через FFmpeg:
    - Зміна таймінгу та швидкості (setpts + atempo)
    - Додавання легкого цифрового шуму (зміна хешу файлу)
    - Мікрокорекція яскравості/насиченості
    - Повне видалення оригінальних метаданих
    """
    if not os.path.exists(input_path):
        print(f"[-] Помилка: файл не знайдено -> {input_path}")
        return False

    print(f"[+] Починаємо унікалізацію: {os.path.basename(input_path)}...")

    # Параметри унікалізації для FFmpeg
    video_filter = "eq=brightness=0.005:saturation=1.02,noise=alls=8:allf=t+u,setpts=0.98*PTS"
    audio_filter = "atempo=1.02"

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", video_filter,
        "-af", audio_filter,
        "-map_metadata", "-1",  # Затирання старих метаданих
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-y",
        output_path
    ]

    try:
        # Запускаємо процес обробки
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"[+] Успішно! Готове відео збережено у: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Помилка FFmpeg:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print("[-] Помилка: FFmpeg не встановлений або не доданий до системних змінних PATH!")
        return False

if __name__ == "__main__":
    # Тестовий запуск
    input_folder = "input"
    output_folder = "output"
    
    # Шукаємо перше ліпше відео в папці input
    files = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    
    if not files:
        print(f"[!] Покладіть будь-який відеофайл у папку '{input_folder}/' для тестування!")
    else:
        src = os.path.join(input_folder, files[0])
        dst = os.path.join(output_folder, f"unique_{files[0]}")
        process_video(src, dst)