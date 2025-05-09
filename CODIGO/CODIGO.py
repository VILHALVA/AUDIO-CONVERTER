import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
from threading import Thread
import glob

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CONVERSOR DE ÁUDIO")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.selected_directory = ""
        self.output_format = ctk.StringVar(value="mp3")

        self.scrollable_frame = ctk.CTkScrollableFrame(root, width=580, height=580)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.scrollable_frame, text="CONVERSOR DE ÁUDIO", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.select_dir_button = ctk.CTkButton(self.scrollable_frame, text="DIRETÓRIO", command=self.select_directory)
        self.select_dir_button.pack(pady=5)

        self.convert_button = ctk.CTkButton(self.scrollable_frame, text="CONVERTER", command=self.start_conversion)
        self.convert_button.pack(pady=5)

        self.format_frame = ctk.CTkFrame(self.scrollable_frame)
        self.format_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(self.format_frame, text="CONVERTER PARA:").pack(anchor='center')

        formats = ["mp3", "wav", "ogg", "flac", "aac", "m4a", "wma", "opus", "alac"]
        for fmt in formats:
            ctk.CTkRadioButton(self.format_frame, text=fmt.upper(), variable=self.output_format, value=fmt).pack(anchor='center')

        self.status_textbox = ctk.CTkTextbox(self.scrollable_frame, width=500, height=200)
        self.status_textbox.pack(pady=10)
        self.status_textbox.configure(state='disabled')

        self.progress_frame = ctk.CTkFrame(self.scrollable_frame)
        self.progress_frame.pack(pady=5, fill='x', padx=20)

        self.percent_label = ctk.CTkLabel(self.progress_frame, text="0%")
        self.percent_label.pack(side='left')

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(side='left', expand=True, fill='x', padx=10)

        self.count_label = ctk.CTkLabel(self.progress_frame, text="0/0")
        self.count_label.pack(side='right')

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory = directory
            self.append_status(f"Diretório selecionado: {directory}\n")

    def start_conversion(self):
        if not self.selected_directory:
            messagebox.showerror("Erro", "Por favor, selecione um diretório primeiro.")
            return
        Thread(target=self.convert_audios).start()

    def convert_audios(self):
        input_dir = self.selected_directory
        selected_format = self.output_format.get()
        output_dir = os.path.join(input_dir, f"CONVERTIDOS_{selected_format.upper()}")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        audio_extensions = ['*.wav', '*.ogg', '*.flac', '*.aac', '*.m4a', '*.wma', '*.alac', '*.opus', '*.mp4', '*.mov', '*.mp3']
        
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(glob.glob(os.path.join(input_dir, ext)))

        total_files = len(audio_files)
        if total_files == 0:
            self.append_status("Nenhum arquivo de áudio encontrado no diretório!\n")
            return

        converted = 0

        for idx, file_path in enumerate(audio_files, 1):
            filename = os.path.basename(file_path)
            name_without_ext = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, f"{name_without_ext}.{selected_format}")

            cmd = [
                "ffmpeg",
                "-y",
                "-i", file_path,
                "-vn",
                "-ar", "44100",
                "-ac", "2",
                "-b:a", "128k",
                output_file
            ]

            self.append_status(f"Convertendo: {filename} para {selected_format.upper()}...\n")

            try:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self.append_status(result.stderr)
            except Exception as e:
                self.append_status(f"Erro ao converter {filename}: {e}\n")
                continue

            converted += 1
            percent = (converted / total_files)
            self.progress_bar.set(percent)
            self.percent_label.configure(text=f"{int(percent * 100)}%")
            self.count_label.configure(text=f"{converted}/{total_files}")

        self.append_status("\nConversão concluída!\n")
        messagebox.showinfo("Finalizado", f"Todos os áudios foram convertidos para {selected_format.upper()} com sucesso!")

    def append_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert('end', message)
        self.status_textbox.see('end')
        self.status_textbox.configure(state='disabled')

if __name__ == "__main__":
    root = ctk.CTk()
    app = AudioConverterApp(root)
    root.state("zoomed")
    root.resizable(False, False)
    root.mainloop()
