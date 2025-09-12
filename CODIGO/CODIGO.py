import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
from threading import Thread
import glob
import ctypes

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def is_hidden(filepath):
    name = os.path.basename(filepath)
    if name.startswith('.'):
        return True
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
        return bool(attrs & 2)
    except:
        return False

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AUDIO CONVERTER")

        self.selected_directory = ""
        self.output_format = ctk.StringVar(value="MP3")
        self.clear_metadata = ctk.StringVar(value="NÃO")

        self.scrollable_frame = ctk.CTkScrollableFrame(root, width=700, height=700)
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.scrollable_frame, text="CONVERSOR DE ÁUDIO", font=("Arial", 30, "bold")).pack(pady=10)

        self.format_container = ctk.CTkFrame(self.scrollable_frame, border_width=2, corner_radius=10)
        self.format_container.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.format_container, text="CONVERTER PARA:").pack(pady=(10, 0))
        self.format_frame = ctk.CTkFrame(self.format_container)
        self.format_frame.pack(pady=10)

        formats = ["MP3", "M4A", "WMA", "WAV", "OGG"]
        for fmt in formats:
            ctk.CTkRadioButton(self.format_frame, text=fmt, variable=self.output_format, value=fmt, command=self.update_convert_button_state).pack(side="left", padx=5)

        self.metadata_container = ctk.CTkFrame(self.scrollable_frame, border_width=2, corner_radius=10)
        self.metadata_container.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.metadata_container, text="LIMPAR METADADOS?").pack(pady=(10, 0))
        self.metadata_frame = ctk.CTkFrame(self.metadata_container)
        self.metadata_frame.pack(pady=10)

        ctk.CTkRadioButton(self.metadata_frame, text="SIM", variable=self.clear_metadata, value="SIM", command=self.update_convert_button_state).pack(side="left", padx=10)
        ctk.CTkRadioButton(self.metadata_frame, text="NÃO", variable=self.clear_metadata, value="NÃO", command=self.update_convert_button_state).pack(side="left", padx=10)

        self.button_frame = ctk.CTkFrame(self.scrollable_frame)
        self.button_frame.pack(pady=10)

        self.select_button = ctk.CTkButton(self.button_frame, text="DIRETÓRIO", command=self.select_directory)
        self.select_button.pack(side="left", padx=10)

        self.convert_button = ctk.CTkButton(self.button_frame, text="CONVERTER", command=self.start_conversion, state="disabled")
        self.convert_button.pack(side="left", padx=10)

        self.status_textbox = ctk.CTkTextbox(self.scrollable_frame, width=500, height=165)
        self.status_textbox.pack(pady=10)
        self.status_textbox.configure(state='disabled')

        self.progress_frame = ctk.CTkFrame(self.scrollable_frame)
        self.progress_frame.pack(pady=(0, 5), fill="x", padx=10)

        self.progress_count_label = ctk.CTkLabel(self.progress_frame, text="0/0", width=50, anchor="w")
        self.progress_count_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", expand=True, fill="x", padx=10)

        self.progress_percent_label = ctk.CTkLabel(self.progress_frame, text="0%", width=50, anchor="e")
        self.progress_percent_label.pack(side="right")

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory = directory
            self.clear_status()
            self.append_status(f"Diretório selecionado: {directory}\n")
            self.update_convert_button_state()

    def update_convert_button_state(self):
        if self.selected_directory:
            self.convert_button.configure(state="normal")
        else:
            self.convert_button.configure(state="disabled")

    def start_conversion(self):
        self.clear_status(keep_directory=True)
        self.progress_bar.set(0)
        self.progress_count_label.configure(text="0/0")
        self.progress_percent_label.configure(text="0%")
        Thread(target=self.convert_audios).start()

    def convert_audios(self):
        input_dir = self.selected_directory
        selected_format = self.output_format.get().lower()
        clear_metadata = self.clear_metadata.get() == "SIM"
        output_dir = os.path.join(input_dir, f"CONVERTIDOS_{selected_format.upper()}")
        os.makedirs(output_dir, exist_ok=True)

        audio_extensions = ['*.mp3', '*.wav', '*.ogg', '*.flac', '*.aac', '*.m4a', '*.wma', '*.alac', '*.opus', '*.mp4', '*.mov', '*.webm']
        audio_files = []

        for ext in audio_extensions:
            files = glob.glob(os.path.join(input_dir, ext))
            audio_files.extend([f for f in files if not is_hidden(f)])

        total = len(audio_files)
        if not audio_files:
            self.append_status("Nenhum arquivo de áudio encontrado no diretório!\n")
            return

        for idx, file_path in enumerate(audio_files):
            filename = os.path.basename(file_path)
            name_wo_ext = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, f"{name_wo_ext}.{selected_format}")

            cmd = ["ffmpeg", "-y", "-i", file_path]

            if clear_metadata:
                cmd += ["-map_metadata", "-1"]
            else:
                cmd += ["-map_metadata", "0"]

            input_ext = os.path.splitext(file_path)[1].lower().replace(".", "")
            
            conv = ["-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k"]
            
            if input_ext == selected_format:
                if clear_metadata:
                    cmd += ["-c", "copy"]
                else:
                    cmd += conv
            else:
                cmd += conv

            cmd.append(output_file)

            self.append_status(f"Convertendo: {filename} para {selected_format.upper()}...\n")

            try:
                subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except Exception as e:
                self.append_status(f"Erro ao converter {filename}: {e}\n")
                continue

            progress_value = (idx + 1) / total
            self.progress_bar.set(progress_value)
            self.progress_count_label.configure(text=f"{idx + 1}/{total}")
            self.progress_percent_label.configure(text=f"{int(progress_value * 100)}%")

        self.append_status(f"\nConversão concluída!\nArquivos salvos em: {output_dir}\n")
        messagebox.showinfo("Finalizado", f"Todos os áudios foram convertidos para {selected_format.upper()} com sucesso!")

    def clear_status(self, keep_directory=False):
        text = self.status_textbox.get("1.0", "end")
        self.status_textbox.configure(state='normal')
        self.status_textbox.delete("1.0", "end")
        if keep_directory:
            for line in text.splitlines():
                if line.startswith("Diretório selecionado"):
                    self.status_textbox.insert("end", line + "\n")
        self.status_textbox.configure(state='disabled')

    def append_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert("end", message)
        self.status_textbox.see("end")
        self.status_textbox.configure(state='disabled')

if __name__ == "__main__":
    root = ctk.CTk()
    app = AudioConverterApp(root)
    root.state("zoomed")
    root.resizable(True, True)
    root.mainloop()
