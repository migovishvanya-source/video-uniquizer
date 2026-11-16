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

        self.title("Video Uniquizer Pro | Batch Mode")
        self.geometry("650x520")
        self.resizable(False, False)

        # Змінні для шляхів
        self.input_file_paths = []

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
            text="Пакетна унікалізація відео для соцмереж", 
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#94a3b8"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Блок вибору файлів
        self.file_card = ctk.CTkFrame(self.main_frame, fg_color="#1a1d24", corner_radius=12)
        self.file_card.pack(fill="x", padx=20, pady=10)

        self.file_label = ctk.CTkLabel(
            self.file_card, 
            text="Файли не обрано", 
            font=ctk.CTkFont(size=13),
            text_color="#cbd5e1"
        )
        self.file_label.pack(side="left", padx=20, pady=20)

        self.select_btn = ctk.CTkButton(
            self.file_card, 
            text="Обрати відео", 
            command=self.select_files,
            fg_color="#3b82f6", 
            hover_color="#2563eb",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=130, height=38
        )
        self.select_btn.pack(side="right", padx=20, pady=20)

        # Статус / Прогрес (зробили світлішим, щоб ідеально читався на чорному)
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Готовий до роботи", 
            font=ctk.CTkFont(size=13),
            text_color="#38bdf8"
        )
        self.status_label.pack(pady=(15, 5))

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=550, height=10, progress_color="#00f2fe")
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        # Кнопка запуску (тепер у стильному синьому кольорі із залізобетонно білим текстом)
        self.run_btn = ctk.CTkButton(
            self.main_frame, 
            text="ЗАПУСТИТИ ПАКЕТНУ ОБРОБКУ", 
            command=self.start_process_thread,
            fg_color="#3b82f6", 
            hover_color="#2563eb",
            text_color="#ffffff",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=320, height=45,
            state="disabled"
        )
        self.run_btn.pack(pady=(25, 15))

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Оберіть відео для унікалізації",
            filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv")]
        )
        if files:
            self.input_file_paths = files
            count = len(files)
            self.file_label.configure(text=f"Обрано файлів: {count}", text_color="#f8fafc")
            self.run_btn.configure(state="normal")
            self.status_label.configure(text=f"Готово до обробки ({count} шт.)", text_color="#38bdf8")

    def start_process_thread(self):
        output_dir = filedialog.askdirectory(title="Оберіть папку для збереження унікалізованих відео")
        if not output_dir:
            return

        self.run_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.status_label.configure(text="Запуск пакетної обробки...", text_color="#f59e0b")

        threading.Thread(target=self.process_batch_task, args=(output_dir,), daemon=True).start()

    def process_batch_task(self, output_dir):
        try:
            import subprocess
            total_files = len(self.input_file_paths)
            
            for index, file_path in enumerate(self.input_file_paths):
                filename = os.path.basename(file_path)
                output_path = os.path.join(output_dir, f"unique_{filename}")
                
                progress_val = (index) / total_files
                self.progress_bar.set(progress_val)
                self.status_label.configure(
                    text=f"Обробка [{index+1}/{total_files}]: {filename}", 
                    text_color="#f59e0b"
                )

                video_filter = "eq=brightness=0.005:saturation=1.02,noise=alls=8:allf=t+u,setpts=0.98*PTS"
                audio_filter = "atempo=1.02"

                cmd = [
                    "ffmpeg",
                    "-i", file_path,
                    "-vf", video_filter,
                    "-af", audio_filter,
                    "-map_metadata", "-1",
                    "-c:v", "libx264",
                    "-crf", "23",
                    "-c:a", "aac",
                    "-y",
                    output_path
                ]

                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            self.progress_bar.set(1.0)
            self.status_label.configure(text="Пакетну обробку завершено успішно!", text_color="#10b981")
            messagebox.showinfo("Успіх", f"Успішно унікалізовано файлів: {total_files}\nЗбережено у папку: {output_dir}")

        except Exception as e:
            self.status_label.configure(text=f"Помилка: {str(e)}", text_color="#ef4444")
            messagebox.showerror("Помилка", str(e))
        
        finally:
            self.run_btn.configure(state="normal")
            self.select_btn.configure(state="normal")

if __name__ == "__main__":
    app = VideoUniquizerApp()
    app.mainloop()