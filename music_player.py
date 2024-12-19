import customtkinter as ctk
import pygame
import os
from PIL import Image
from tkinter import filedialog
import time

class MusicPlayer:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Spotify Clone")
        self.window.geometry("1100x600")
        self.window.configure(fg_color="#191414")  # Spotify's dark theme

        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Current playing track
        self.current_track = None
        self.is_playing = False
        self.songs_list = []
        self.current_song_index = 0

        self.create_gui()

    def create_gui(self):
        # Create main frames
        self.sidebar = ctk.CTkFrame(self.window, fg_color="#121212", width=200)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        self.main_content = ctk.CTkFrame(self.window, fg_color="#121212")
        self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Sidebar content
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Spotify Clone", 
                                     font=("Helvetica", 20, "bold"), 
                                     text_color="#1DB954")
        self.logo_label.pack(pady=20)

        # Add music button
        self.add_button = ctk.CTkButton(self.sidebar, 
                                      text="Add Music", 
                                      command=self.add_songs,
                                      fg_color="#1DB954",
                                      hover_color="#1ed760")
        self.add_button.pack(pady=10, padx=20)

        # Create playlist view
        self.playlist = ctk.CTkTextbox(self.main_content, fg_color="#121212", 
                                     text_color="white", width=400)
        self.playlist.pack(pady=20, fill="both", expand=True)

        # Control buttons frame
        self.controls_frame = ctk.CTkFrame(self.main_content, fg_color="#121212")
        self.controls_frame.pack(pady=20)

        # Previous button
        self.prev_button = ctk.CTkButton(self.controls_frame, 
                                       text="⏮", 
                                       command=self.play_previous,
                                       fg_color="#1DB954",
                                       hover_color="#1ed760",
                                       width=60)
        self.prev_button.pack(side="left", padx=5)

        # Play/Pause button
        self.play_button = ctk.CTkButton(self.controls_frame, 
                                       text="▶", 
                                       command=self.play_pause,
                                       fg_color="#1DB954",
                                       hover_color="#1ed760",
                                       width=60)
        self.play_button.pack(side="left", padx=5)

        # Next button
        self.next_button = ctk.CTkButton(self.controls_frame, 
                                       text="⏭", 
                                       command=self.play_next,
                                       fg_color="#1DB954",
                                       hover_color="#1ed760",
                                       width=60)
        self.next_button.pack(side="left", padx=5)

        # Volume slider
        self.volume_slider = ctk.CTkSlider(self.controls_frame, 
                                         from_=0, 
                                         to=1, 
                                         command=self.change_volume)
        self.volume_slider.pack(side="left", padx=20)
        self.volume_slider.set(0.5)

    def add_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for file in files:
            self.songs_list.append(file)
            # Display only the filename in the playlist
            self.playlist.insert("end", os.path.basename(file) + "\n")

    def play_pause(self):
        if not self.songs_list:
            return

        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.configure(text="▶")
            self.is_playing = False
        else:
            if self.current_track != self.songs_list[self.current_song_index]:
                self.current_track = self.songs_list[self.current_song_index]
                pygame.mixer.music.load(self.current_track)
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            self.play_button.configure(text="⏸")
            self.is_playing = True

    def play_next(self):
        if not self.songs_list:
            return

        self.current_song_index = (self.current_song_index + 1) % len(self.songs_list)
        self.current_track = self.songs_list[self.current_song_index]
        pygame.mixer.music.load(self.current_track)
        pygame.mixer.music.play()
        self.is_playing = True
        self.play_button.configure(text="⏸")

    def play_previous(self):
        if not self.songs_list:
            return

        self.current_song_index = (self.current_song_index - 1) % len(self.songs_list)
        self.current_track = self.songs_list[self.current_song_index]
        pygame.mixer.music.load(self.current_track)
        pygame.mixer.music.play()
        self.is_playing = True
        self.play_button.configure(text="⏸")

    def change_volume(self, value):
        pygame.mixer.music.set_volume(value)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MusicPlayer()
    app.run()
