import tkinter as tk
from tkinter import ttk, font
import time


#author = Richard Whyte
#version = 1.5.0
#email = Richard.whyte@elev.ga.ntig.se

class Lift:
    def __init__(self, window):
        self.window = window
        self.window.title("Neon Lift Game")
        self.window.geometry("350x550")
        self.window.configure(bg='#120a0a')

        # Lift status
        self.current_floor = 1
        self.total_floors = 8
        self.lift_moving = False
        self.default_arrow_symbol = "■"

        # Colours
        self.bg_colour = '#120a0a'
        self.button_colour = '#4a3b3a'
        self.button_active_colour = '#e8726d'
        self.text_colour = '#ffe0e0'

        # Fonts
        self.button_font = font.Font(family='Impact', size=12)

        #UI
        self.create_ui()

    def create_ui(self):
        # Main frame
        main_frame = tk.Frame(self.window, bg=self.bg_colour)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Floor display attop
        display_frame = tk.Frame(main_frame, bg='#241a1a', bd=2, relief=tk.SUNKEN)
        display_frame.pack(fill=tk.X, pady=(0, 15))

        self.floor_label = tk.Label(display_frame,
                                    text="▣ 1 ▣",
                                    font=('Impact', 24),
                                    fg=self.button_active_colour,
                                    bg='#241a1a',
                                    padx=15)
        self.floor_label.pack(pady=8)

        self.direction_indicator = tk.Label(display_frame,
                                            text=self.default_arrow_symbol,
                                            font=('Impact', 16),
                                            fg=self.text_colour,
                                            bg='#241a1a')
        self.direction_indicator.pack(pady=(0, 8))

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.bg_colour)
        button_frame.pack()

        # Floor buttons
        for i, floor in enumerate(range(self.total_floors, 0, -1)):
            floor_button = tk.Button(button_frame,
                                     text=str(floor),
                                     command=lambda f=floor: self.move_to_floor(f),
                                     bg=self.button_colour,
                                     fg=self.text_colour,
                                     activebackground=self.button_active_colour,
                                     activeforeground='black',
                                     font=self.button_font,
                                     width=3,
                                     height=1,
                                     relief=tk.GROOVE,
                                     bd=2)
            floor_button.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            setattr(self, f'floor_button_{floor}', floor_button)

        # Message log
        log_frame = tk.Frame(main_frame, bg='#241a1a')
        log_frame.pack(fill=tk.X, pady=(15, 0))

        self.message_log = tk.Text(log_frame,
                                   height=5,
                                   width=25,
                                   bg='#241a1a',
                                   fg=self.text_colour,
                                   font=('Arial', 9),
                                   relief=tk.SUNKEN,
                                   bd=1)
        self.message_log.pack(padx=3, pady=3)
        self.message_log.insert(tk.END, "Ready to go up!\n")
        self.message_log.config(state=tk.DISABLED)

    def move_to_floor(self, destination_floor):
        if self.lift_moving:
            self.log_message("Lift is currently moving. Please wait.")
            return

        if destination_floor == self.current_floor:
            self.log_message("You are already on this floor.")
            return

        self.lift_moving = True
        self.log_message(f"Moving to floor {destination_floor}...")

        # Show direction
        if destination_floor > self.current_floor:
            self.direction_indicator.config(text="↑", fg='#e8e84a')
        else:
            self.direction_indicator.config(text="↓", fg='#e84a4a')

        # Highlight destination button
        destination_button = getattr(self, f'floor_button_{destination_floor}')
        destination_button.config(bg=self.button_active_colour)

        # Simulate floor movement
        step = 1 if destination_floor > self.current_floor else -1
        for _ in range(self.current_floor, destination_floor, step):
            time.sleep(0.2)
            self.current_floor += step
            self.floor_label.config(text=f"▣ {self.current_floor} ▣")
            self.window.update()

        # Reset indicators
        self.direction_indicator.config(text=self.default_arrow_symbol, fg=self.text_colour)
        destination_button.config(bg=self.button_colour)
        self.log_message(f"Arrived at floor {destination_floor}.")
        self.lift_moving = False

    def trigger_emergency_stop(self):
        if self.lift_moving:
            self.lift_moving = False
            self.log_message("Emergency stop activated!")
            self.direction_indicator.config(text="✖", fg='#e84a4a')
        else:
            self.log_message("Lift is not moving.")

    def log_message(self, message):
        self.message_log.config(state=tk.NORMAL)
        self.message_log.insert(tk.END, "• " + message + "\n")
        self.message_log.see(tk.END)
        self.message_log.config(state=tk.DISABLED)

    def clear_log(self):
        self.message_log.config(state=tk.NORMAL)
        self.message_log.delete(1.0, tk.END)
        self.message_log.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = Lift(root)
    root.mainloop()
