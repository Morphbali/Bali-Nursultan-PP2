import pygame

class Player:
    def __init__(self):
        self.playing = False
        self.current_track = 0
        self.tracks = ["music/track1.wav", "music/track2.wav"]
        self.track_name = self.tracks[self.current_track]
        pygame.mixer.music.load(self.track_name)
        pygame.mixer.music.set_volume(0.5)

    def handle_keys(self, keys):
        if keys[pygame.K_p]:
            self.play()
        elif keys[pygame.K_s]:
            self.stop()
        elif keys[pygame.K_n]:
            self.next_track()
        elif keys[pygame.K_b]:
            self.previous_track()
        elif keys[pygame.K_q]:
            pygame.quit()

    def play(self):
        if not self.playing:
            pygame.mixer.music.play(loops=0, start=0.0)  # Используем music.play()
            self.playing = True

    def stop(self):
        if self.playing:
            pygame.mixer.music.stop()  # Используем music.stop()
            self.playing = False

    def next_track(self):
        self.stop()
        self.current_track = (self.current_track + 1) % len(self.tracks)
        self.track_name = self.tracks[self.current_track]
        pygame.mixer.music.load(self.track_name)
        self.play()

    def previous_track(self):
        self.stop()
        self.current_track = (self.current_track - 1) % len(self.tracks)
        self.track_name = self.tracks[self.current_track]
        pygame.mixer.music.load(self.track_name)
        self.play()

    def display_info(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Track: {self.track_name.split('/')[-1]}", True, (0, 0, 0))
        screen.blit(text, (20, 20))

        # Прогресс
        progress = pygame.mixer.music.get_pos() / 1000  # Время в секундах
        progress_text = font.render(f"Progress: {int(progress)} sec", True, (0, 0, 0))
        screen.blit(progress_text, (20, 60))