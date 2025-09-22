import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
from threading import Thread
import glob
import ctypes

AUDIO_EXTENSIONS = [
    '*.mp3', '*.wav', '*.ogg', '*.flac', '*.aac',
    '*.m4a', '*.wma', '*.alac', '*.opus', '*.mp4',
    '*.mov', '*.webm'
]

def is_hidden(filepath):
    name = os.path.basename(filepath)
    if name.startswith('.'):
        return True
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
        return bool(attrs & 2)
    except:
        return False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AUDIO CONVERTER")

        self.selected_directory = ""
        self.output_format = ctk.StringVar(value="MP3")
        self.limpar_metadados = ctk.StringVar(value="NAO")
        self.audio_quality = ctk.StringVar(value="192K")  

        self.scrollable_frame = ctk.CTkScrollableFrame(root, width=700, height=700)
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.scrollable_frame, text="CONVERSOR DE ÁUDIO", font=("Arial", 30, "bold")).pack(pady=10)

        self.create_format_selection()
        self.create_quality_selection()   
        self.create_metadata_selection()
        self.create_buttons()
        self.create_status_frame()

    def create_format_selection(self):
        frame = ctk.CTkFrame(self.scrollable_frame, border_width=2, corner_radius=10)
        frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(frame, text="CONVERTER PARA:").pack(pady=(10, 0))

        inner = ctk.CTkFrame(frame)
        inner.pack(pady=10)
        formats = ["MP3", "M4A", "WMA", "WAV", "OGG"]
        for fmt in formats:
            ctk.CTkRadioButton(inner, text=fmt, variable=self.output_format, value=fmt,
                               command=self.update_convert_button_state).pack(side="left", padx=5)

    def create_quality_selection(self):
        frame = ctk.CTkFrame(self.scrollable_frame, border_width=2, corner_radius=10)
        frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(frame, text="QUALIDADE (KBPS):").pack(pady=(10, 0))

        inner = ctk.CTkFrame(frame)
        inner.pack(pady=10)

        qualities = ["128K", "192K", "256K", "320K"]
        for q in qualities:
            ctk.CTkRadioButton(inner, text=q, variable=self.audio_quality, value=q).pack(side="left", padx=10)

    def create_metadata_selection(self):
        frame = ctk.CTkFrame(self.scrollable_frame, border_width=2, corner_radius=10)
        frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(frame, text="LIMPAR METADADOS?").pack(pady=(10, 0))

        inner = ctk.CTkFrame(frame)
        inner.pack(pady=10)

        self.radio_sim = ctk.CTkRadioButton(inner, text="SIM", variable=self.limpar_metadados, value="SIM",
                                            command=self.update_convert_button_state)
        self.radio_sim.pack(side="left", padx=10)

        self.radio_nao = ctk.CTkRadioButton(inner, text="NÃO", variable=self.limpar_metadados, value="NAO",
                                            command=self.update_convert_button_state)
        self.radio_nao.pack(side="left", padx=10)

        self.radio_cm = ctk.CTkRadioButton(inner, text="MET", variable=self.limpar_metadados, value="MET",
                                           command=self.update_convert_button_state)
        self.radio_cm.pack(side="left", padx=10)
        self.radio_cm.pack_forget()

    def create_buttons(self):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(pady=10)

        self.select_button = ctk.CTkButton(frame, text="DIRETÓRIO", command=self.select_directory)
        self.select_button.pack(side="left", padx=10)

        self.convert_button = ctk.CTkButton(frame, text="CONVERTER", command=self.start_conversion, state="disabled")
        self.convert_button.pack(side="left", padx=10)

        self.cm_button = ctk.CTkButton(frame, text="MET", command=self.start_clean_metadata, fg_color="orange")
        self.cm_button.pack(side="left", padx=10)
        self.cm_button.pack_forget()

    def create_status_frame(self):
        self.status_textbox = ctk.CTkTextbox(self.scrollable_frame, width=500, height=160)
        self.status_textbox.pack(pady=10)
        self.status_textbox.configure(state='disabled')

        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(pady=(0, 5), fill="x", padx=10)

        self.progress_count_label = ctk.CTkLabel(frame, text="0/0", width=50, anchor="w")
        self.progress_count_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", expand=True, fill="x", padx=10)

        self.progress_percent_label = ctk.CTkLabel(frame, text="0%", width=50, anchor="e")
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
            self.check_same_format()
        else:
            self.convert_button.configure(state="disabled")
            self.cm_button.pack_forget()

    def check_same_format(self):
        selected_format = self.output_format.get().lower()
        audio_files = self.get_audio_files()
        
        if not audio_files:
            self.radio_cm.pack_forget()
            self.limpar_metadados.set("NAO")
            return

        all_same = all(os.path.splitext(f)[1].lower().replace(".", "") == selected_format for f in audio_files)
        
        if all_same:
            self.radio_cm.pack(side="left", padx=10)
        else:
            self.radio_cm.pack_forget()
            if self.limpar_metadados.get() == "MET":
                self.limpar_metadados.set("NAO")

    def get_audio_files(self):
        files_list = []
        for ext in AUDIO_EXTENSIONS:
            files = glob.glob(os.path.join(self.selected_directory, ext))
            files_list.extend([f for f in files if not is_hidden(f)])
        return files_list

    def start_conversion(self):
        self.clear_status(keep_directory=True)
        self.reset_progress()
        Thread(target=self.convert_audios).start()

    def start_clean_metadata(self):
        self.clear_status(keep_directory=True)
        self.reset_progress()
        Thread(target=self.clean_metadata_only).start()

    def clean_metadata_only(self):
        self.run_ffmpeg_process(limpar_metadados=True, converter=True)

    def run_ffmpeg_process(self, limpar_metadados=True, converter=False):
        input_dir = self.selected_directory
        selected_format = self.output_format.get().lower()
        output_dir = os.path.join(input_dir, f"CONVERTIDOS_{selected_format.upper()}")
        os.makedirs(output_dir, exist_ok=True)

        audio_files = self.get_audio_files()
        total = len(audio_files)
        if not audio_files:
            self.append_status("Nenhum arquivo de áudio encontrado no diretório!\n")
            return

        for idx, file_path in enumerate(audio_files):
            filename = os.path.basename(file_path)
            name_wo_ext = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, f"{name_wo_ext}.{selected_format}")

            cmd = ["ffmpeg", "-y", "-i", file_path]
            if converter:
                cmd += ["-vn", "-ar", "44100", "-ac", "2", "-b:a", self.audio_quality.get()]
            else:
                cmd += ["-c", "copy"]

            cmd += ["-map_metadata", "-1"] if limpar_metadados else ["-map_metadata", "0"]
            cmd.append(output_file)

            self.append_status(f"Processando: {filename}...\n")
            
            try:
                subprocess.run(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, encoding="utf-8", errors="ignore",
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except Exception as e:
                self.append_status(f"Erro ao converter {filename}: {e}\n")
                continue

            self.update_progress(idx + 1, total)

        self.append_status(f"\nProcesso concluído com sucesso!\nArquivos salvos em: {output_dir}\n")
        messagebox.showinfo("Finalizado", f"Processo concluído com sucesso! Arquivos salvos em {output_dir}!")

    def convert_audios(self):
        choice = self.limpar_metadados.get()
        if choice == "SIM":
            self.run_ffmpeg_process(converter=True, limpar_metadados=True)
        elif choice == "NAO":
            self.run_ffmpeg_process(converter=True, limpar_metadados=False)
        elif choice == "MET":
            self.run_ffmpeg_process(converter=False, limpar_metadados=True)

    def reset_progress(self):
        self.progress_bar.set(0)
        self.progress_count_label.configure(text="0/0")
        self.progress_percent_label.configure(text="0%")

    def update_progress(self, current, total):
        progress_value = current / total
        self.progress_bar.set(progress_value)
        self.progress_count_label.configure(text=f"{current}/{total}")
        self.progress_percent_label.configure(text=f"{int(progress_value * 100)}%")

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
