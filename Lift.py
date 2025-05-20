import tkinter as tk
from tkinter import font
import time

class Lift:
    def __init__(self, window):
        self.window = window
        self.window.title("Lift")
        self.window.geometry("1000x700")  # Moderate size window for cleaner UI
        self.window.configure(bg='#120a0a')  # Background colour of the window

        # Lift status
        self.current_floor = 1  # Starting at floor 1
        self.total_floors = 8  # Total number of floors in the building
        self.lift_moving = False  # Indicates the lift is currently moving
        self.default_arrow_symbol = "■"  # Default symbol for direction indicator

        # Colours
        self.bg_colour = '#120a0a' 
        self.button_colour = '#4a3b3a' 
        self.button_active_colour = '#e8726d' 
        self.text_colour = '#ffe0e0'  
        self.lift_colour = '#2a1f1f'  
        self.character_colour = '#66b3ff'  
        self.character_outline = '#003366' 

        # Fonts
        self.button_font = font.Font(family='Impact', size=12)  # Font for buttons
        self.floor_font = font.Font(family='Impact', size=28, weight='bold')

        # UI
        self.create_ui()  # Create the user interface

    def create_ui(self):
        main_frame = tk.Frame(self.window, bg=self.bg_colour)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left side for controls
        control_frame = tk.Frame(main_frame, bg=self.bg_colour)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, anchor='n')

        # Floor Indicator
        indicator_frame = tk.Frame(control_frame, bg=self.bg_colour)
        indicator_frame.pack(fill=tk.X, pady=(0, 20))

        self.floor_label = tk.Label(indicator_frame,
                                    text=f"▣ {self.current_floor} ▣",
                                    font=self.floor_font,
                                    fg=self.button_active_colour,
                                    bg=self.bg_colour)
        self.floor_label.pack(anchor='center')

        self.direction_indicator = tk.Label(indicator_frame,
                                            text=self.default_arrow_symbol,
                                            font=('Impact', 24),
                                            fg=self.text_colour,
                                            bg=self.bg_colour)
        self.direction_indicator.pack(anchor='center', pady=(5, 0))

        # Buttons Frame 
        button_frame = tk.Frame(control_frame, bg=self.bg_colour)
        button_frame.pack()

        # Create buttons
        for i, floor in enumerate(range(self.total_floors, 0, -1)):
            floor_button = tk.Button(button_frame,
                                     text=str(floor),
                                     command=lambda f=floor: self.move_to_floor(f),
                                     bg=self.button_colour,
                                     fg=self.text_colour,
                                     activebackground=self.button_active_colour,
                                     activeforeground='black',
                                     font=self.button_font,
                                     width=5,
                                     height=3,
                                     relief=tk.RAISED,
                                     bd=3)
            floor_button.grid(row=i // 2, column=i % 2, padx=6, pady=6)
            setattr(self, f'floor_button_{floor}', floor_button)

        # Exit Button below buttons
        exit_button = tk.Button(control_frame, text="Exit the lift",
                                command=self.exit_program,
                                bg=self.button_colour,
                                fg=self.text_colour,
                                font=self.button_font,
                                width=12,
                                height=2,
                                relief=tk.RAISED,
                                bd=3)
        exit_button.pack(pady=(30, 0))

        # Right side for graphical lift
        graphical_frame = tk.Frame(main_frame, bg=self.bg_colour)
        graphical_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40,0))

        # Canvas for lift shaft and character
        self.floor_height = 80  # Height of each floor
        canvas_height = self.total_floors * self.floor_height + 40
        canvas_width = 220
        self.character_canvas = tk.Canvas(graphical_frame, width=canvas_width,
                                          height=canvas_height,
                                          bg='#241a1a',
                                          bd=3, relief=tk.SUNKEN)
        self.character_canvas.pack(expand=True)

        # Draw floors lines & numbers
        for floor in range(1, self.total_floors + 1):
            y = canvas_height - floor * self.floor_height
            self.character_canvas.create_line(30, y, canvas_width - 30, y,
                                             fill='#4a3b3a', width=2)
            self.character_canvas.create_text(15, y - self.floor_height // 2,
                                             text=str(floor), fill=self.text_colour,
                                             font=('Arial', 14), anchor='w')

        # Lift cage dimensions
        self.lift_left_x = 60
        self.lift_right_x = canvas_width - 60
        self.lift_height = int(self.floor_height * 0.85)
        self.lift_border_colour = '#d1a6a3'

        # Initial lift rectangle position
        initial_y_bottom = canvas_height - (self.current_floor * self.floor_height)
        initial_y_top = initial_y_bottom - self.lift_height
        self.lift_rect = self.character_canvas.create_rectangle(
            self.lift_left_x, initial_y_top, self.lift_right_x, initial_y_bottom,
            fill=self.lift_colour, outline=self.lift_border_colour, width=4
        )

        # Draw character setup (smaller character)
        self.draw_character(initial_y_top, initial_y_bottom)

        # Message log below graphical frame
        log_frame = tk.Frame(graphical_frame, bg='#241a1a')
        log_frame.pack(fill=tk.X, pady=(20,0))

        self.message_log = tk.Text(log_frame, height=6, width=40,
                                   bg='#241a1a', fg=self.text_colour,
                                   font=('Arial', 10), relief=tk.SUNKEN, bd=1)
        self.message_log.pack(padx=6, pady=6, fill='x')
        self.message_log.insert(tk.END, "Ready to go up!\n")
        self.message_log.config(state=tk.DISABLED)


    def draw_character(self, y_top, y_bottom):
        if hasattr(self, "character_parts"):
            for part in self.character_parts:
                self.character_canvas.delete(part)

        self.character_parts = []

        center_x = (self.lift_left_x + self.lift_right_x) / 2
        center_y = (y_top + y_bottom) / 2 + 5  # slight downward offset for no clipping

        # Smaller head
        head_radius = 10
        head = self.character_canvas.create_oval(center_x - head_radius,
                                                 center_y - 30 - head_radius,
                                                 center_x + head_radius,
                                                 center_y - 30 + head_radius,
                                                 fill=self.character_colour,
                                                 outline=self.character_outline,
                                                 width=2)
        self.character_parts.append(head)

        # Body
        body = self.character_canvas.create_line(center_x, center_y - 20,
                                                 center_x, center_y + 10,
                                                 fill=self.character_outline, width=3)
        self.character_parts.append(body)

        # Arms
        left_arm = self.character_canvas.create_line(center_x, center_y - 15,
                                                     center_x - 15, center_y + 5,
                                                     fill=self.character_outline, width=2)
        right_arm = self.character_canvas.create_line(center_x, center_y - 15,
                                                      center_x + 15, center_y + 5,
                                                      fill=self.character_outline, width=2)
        self.character_parts.extend([left_arm, right_arm])

        # Legs
        left_leg = self.character_canvas.create_line(center_x, center_y + 10,
                                                     center_x - 10, center_y + 25,
                                                     fill=self.character_outline, width=2)
        right_leg = self.character_canvas.create_line(center_x, center_y + 10,
                                                      center_x + 10, center_y + 25,
                                                      fill=self.character_outline, width=2)
        self.character_parts.extend([left_leg, right_leg])

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

        step = 1 if destination_floor > self.current_floor else -1
        for _ in range(self.current_floor, destination_floor, step):
            time.sleep(0.18)
            self.current_floor += step
            self.floor_label.config(text=f"▣ {self.current_floor} ▣")
            self.window.update()

            self.update_lift_and_character_position()

        # Reset
        self.direction_indicator.config(text=self.default_arrow_symbol, fg=self.text_colour)
        destination_button.config(bg=self.button_colour)
        self.log_message(f"Arrived at floor {destination_floor}.")
        self.lift_moving = False

    def update_lift_and_character_position(self):
        canvas_height = self.total_floors * self.floor_height + 40
        y_bottom = canvas_height - (self.current_floor * self.floor_height)
        y_top = y_bottom - self.lift_height
        self.character_canvas.coords(self.lift_rect, self.lift_left_x, y_top, self.lift_right_x, y_bottom)
        self.draw_character(y_top, y_bottom)

    def log_message(self, message):
        self.message_log.config(state=tk.NORMAL)
        self.message_log.insert(tk.END, "• " + message + "\n")
        self.message_log.see(tk.END)
        self.message_log.config(state=tk.DISABLED)

    def exit_program(self):
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Lift(root)
    root.mainloop()

