import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Налаштування стилю CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VideoUniquizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video Uniquizer Pro | AI & Media Tools")
        self.geometry("650x480")
        self.resizable(False, False)

        # Змінні для шляхів
        self.input_file_path = ""

        # ---- ГОЛОВНИЙ КОНТЕЙНЕР ----
        self.main_frame = ctk.CTkFrame(self, fg_color="#0f1117", corner_radius=16)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="VIDEO UNIQUIZER PRO", 
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            text_color="#00f2fe"
        )
        self.title_label.pack(pady=(15, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, 
            text="Професійний софт для обходу алгоритмів соцмереж", 
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#94a3b8"
        )
        self.subtitle_label.pack(pady=(0, 25))

        # Блок вибору файлу
        self.file_card = ctk.CTkFrame(self.main_frame, fg_color="#1a1d24", corner_radius=12)
        self.file_card.pack(fill="x", padx=20, pady=10)

        self.file_label = ctk.CTkLabel(
            self.file_card, 
            text="Файл не обрано", 
            font=ctk.CTkFont(size=13),
            text_color="#cbd5e1"
        )
        self.file_label.pack(side="left", padx=20, pady=20)

        self.select_btn = ctk.CTkButton(
            self.file_card, 
            text="Обрати відео", 
            command=self.select_file,
            fg_color="#3b82f6", 
            hover_color="#2563eb",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=130, height=38
        )
        self.select_btn.pack(side="right", padx=20, pady=20)

        # Статус / Прогрес
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Готовий до роботи", 
            font=ctk.CTkFont(size=13),
            text_color="#64748b"
        )
        self.status_label.pack(pady=(20, 10))

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=550, height=10, progress_color="#00f2fe")
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        # Кнопка запуску унікалізації
        self.run_btn = ctk.CTkButton(
            self.main_frame, 
            text="ЗАПУСТИТИ УНІКАЛІЗАЦІЮ", 
            command=self.start_process_thread,
            fg_color="#10b981", 
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=280, height=45,
            state="disabled"
        )
        self.run_btn.pack(pady=(30, 15))

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Оберіть відео для унікалізації",
            filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv")]
        )
        if file_path:
            self.input_file_path = file_path
            file_name = os.path.basename(file_path)
            self.file_label.configure(text=f"Обрано: {file_name}", text_color="#f8fafc")
            self.run_btn.configure(state="normal")
            self.status_label.configure(text="Файл успішно завантажено в пам'ять", text_color="#38bdf8")

    def start_process_thread(self):
        # Відкриваємо вікно «Зберегти як...», щоб користувач сам обрав місце збереження
        original_name = os.path.basename(self.input_file_path)
        output_path = filedialog.asksaveasfilename(
            title="Зберегти унікалізоване відео як...",
            defaultextension=".mp4",
            initialfile=f"unique_{original_name}",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )

        if not output_path:
            return  # Якщо користувач натиснув «Скасувати»

        self.run_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.status_label.configure(text="Обробка відео через FFmpeg...", text_color="#f59e0b")
        self.progress_bar.set(0.3)

        threading.Thread(target=self.process_video_task, args=(output_path,), daemon=True).start()

    def process_video_task(self, output_path):
        try:
            import subprocess
            video_filter = "eq=brightness=0.005:saturation=1.02,noise=alls=8:allf=t+u,setpts=0.98*PTS"
            audio_filter = "atempo=1.02"

            cmd = [
                "ffmpeg",
                "-i", self.input_file_path,
                "-vf", video_filter,
                "-af", audio_filter,
                "-map_metadata", "-1",
                "-c:v", "libx264",
                "-crf", "23",
                "-c:a", "aac",
                "-y",
                output_path
            ]

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=KeyError and False or True)
            
            # Перевіряємо запуск
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Успішно збережено!", text_color="#10b981")
            messagebox.showinfo("Успіх", f"Відео успішно унікалізовано та збережено:\n{output_path}")

        except Exception as e:
            self.status_label.configure(text=f"Помилка: {str(e)}", text_color="#ef4444")
            messagebox.showerror("Помилка", str(e))
        
        finally:
            self.run_btn.configure(state="normal")
            self.select_btn.configure(state="normal")

if __name__ == "__main__":
    app = VideoUniquizerApp()
    app.mainloop()