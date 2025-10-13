import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pygame
import time
import threading
import pickle
from modules import converter

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Docs")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1A1A1A")

        self.main_frame = tk.Frame(self.root, bg="#1A1A1A")
        self.main_frame.pack(expand=True, fill="both")

        self.create_welcome_frame()

        pygame.mixer.init()
        self.is_playing = False
        self.is_paused = False
        self.conversion_history = self.load_history()
        self.audio_window = None
        self.pdf_file = None

    def create_welcome_frame(self):
        self.welcome_frame = tk.Frame(self.main_frame, bg="#2B2B2B", padx=20, pady=20, borderwidth=0)
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")

        welcome_label = tk.Label(self.welcome_frame, text="Welcome To WhisperDocs!", font=("Helvetica Neue", 32, "bold"), fg="#FFFFFF", bg="#2B2B2B")
        welcome_label.pack(pady=(0, 20))

        continue_button = tk.Button(self.welcome_frame, text="Continue", font=("Helvetica Neue", 14), bg="#007AFF", fg="#FFFFFF", command=self.continue_to_app, activebackground="#005BB5", bd=0, relief="flat")
        continue_button.pack(fill="x")

    def continue_to_app(self):
        self.welcome_frame.place_forget()
        self.create_action_buttons()

    def create_action_buttons(self):
        button_style = {
            "font": ("Helvetica Neue", 14),
            "bg": "#007AFF",
            "fg": "#FFFFFF",
            "activebackground": "#005BB5",
            "bd": 0,
            "relief": "flat",
            "width": 20
        }

        action_frame = tk.Frame(self.main_frame, bg="#1A1A1A")
        action_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.upload_button = tk.Button(action_frame, text="Upload PDF", command=self.upload_pdf, **button_style)
        self.upload_button.pack(pady=10)

        self.convert_button = tk.Button(action_frame, text="Convert PDF to Audio", command=self.convert_to_audio, **button_style)
        self.convert_button.pack(pady=10)

        self.play_button = tk.Button(action_frame, text="Play Audio", command=self.play_audio, **button_style)
        self.play_button.pack(pady=10)

        self.history_button = tk.Button(action_frame, text="History", command=self.show_history, **button_style)
        self.history_button.pack(pady=10)

        self.progress_label = tk.Label(self.main_frame, bg="#1A1A1A", fg="#A3C1DA", font=("Helvetica Neue", 14))
        self.progress_label.pack_forget()

    def upload_pdf(self):
        pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_file:
            self.pdf_file = pdf_file
            messagebox.showinfo("File Uploaded", f"PDF file '{os.path.basename(pdf_file)}' uploaded successfully.")

    def convert_to_audio(self):
        self.loading_screen = tk.Toplevel(self.root)
        self.loading_screen.title("Loading...")
        self.loading_screen.geometry("300x150")
        self.loading_screen.configure(bg="#2B2B2B")
        self.loading_screen.overrideredirect(True)

        loading_label = tk.Label(self.loading_screen, text="Converting PDF to Audio...", font=("Helvetica Neue", 14), fg="#A3C1DA", bg="#2B2B2B")
        loading_label.pack(pady=20)

        threading.Thread(target=self.perform_conversion).start()

    def perform_conversion(self):
        try:
            if self.pdf_file:
                audio_filename = "recordedaudio.mp3"
                converter.convert(pdflocation=self.pdf_file)
                time.sleep(1)
                self.loading_screen.destroy()
                self.add_to_history(os.path.basename(self.pdf_file), audio_filename, time.strftime("%Y-%m-%d %H:%M:%S"))
                messagebox.showinfo("AUDIO CONVERTED", "Audio can be played now.")
            else:
                self.loading_screen.destroy()
                messagebox.showwarning("No PDF", "Please upload a PDF before converting.")
        except Exception as error:
            self.loading_screen.destroy()
            messagebox.showerror("Conversion Error", f"An error occurred: {error}")

    def play_audio(self):
        audio_file = "recordedaudio.mp3"
        if os.path.exists(audio_file):
            if self.audio_window is None or not self.audio_window.winfo_exists():
                self.audio_window = tk.Toplevel(self.root)
                self.audio_window.title("Audio Control")
                self.audio_window.geometry("300x150")
                self.audio_window.configure(bg="#2B2B2B")

                self.play_pause_button = tk.Button(self.audio_window, text="Play", font=("Helvetica Neue", 14), bg="#007AFF", fg="#FFFFFF", command=self.toggle_play_pause, activebackground="#005BB5", bd=0, relief="flat")
                self.play_pause_button.pack(fill="x", pady=20)

            if not self.is_playing and not self.is_paused:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play(loops=0, start=0.0)
                self.is_playing = True
                self.is_paused = False
                self.play_pause_button.config(text="Pause")
            elif self.is_playing and not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_pause_button.config(text="Play")
            elif self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_pause_button.config(text="Pause")
        else:
            messagebox.showerror("File Not Found", "Please convert a PDF to audio first.")

    def toggle_play_pause(self):
        if not self.is_playing:
            self.play_audio()
        else:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_pause_button.config(text="Pause")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_pause_button.config(text="Play")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Conversion History")
        history_window.geometry("1000x1000")
        history_window.configure(bg="#2B2B2B")

        history_listbox = tk.Listbox(history_window, font=("Helvetica Neue", 12), bg="#3B3B3B", fg="#FFFFFF", selectmode=tk.SINGLE)
        history_listbox.pack(fill="both", expand=True, padx=20, pady=20)

        for entry in self.conversion_history:
            history_listbox.insert(tk.END, f"PDF: {entry['pdf_filename']} | Audio: {entry['audio_filename']} | Date: {entry['timestamp']}")

        close_button = tk.Button(history_window, text="Close", font=("Helvetica Neue", 14), bg="#007AFF", fg="#FFFFFF", command=history_window.destroy, activebackground="#005BB5", bd=0, relief="flat")
        close_button.pack(pady=10)

    def load_history(self):
        history_file = "conversion_history.dat"
        if os.path.exists(history_file):
            with open(history_file, "rb") as f:
                return pickle.load(f)
        else:
            return []

    def add_to_history(self, pdf_filename, audio_filename, timestamp):
        entry = {
            "pdf_filename": pdf_filename,
            "audio_filename": audio_filename,
            "timestamp": timestamp
        }
        self.conversion_history.append(entry)
        with open("conversion_history.dat", "wb") as f:
            pickle.dump(self.conversion_history, f)

root = tk.Tk()
app = AudioConverterApp(root)
root.mainloop()
