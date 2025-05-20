import tkinter as tk
from tkinter import ttk, font
import time


# author = Richard Whyte
# version = 1.6.0
# email = Richard.whyte@elev.ga.ntig.se

class Lift:
    def __init__(self, window):
        self.window = window
        self.window.title("Lift")  
        self.window.geometry("1920x1080")  # Setting the window size to 1080p 
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
        self.button_font = font.Font(family='Impact', size=11)  # Font for buttons

        # UI
        self.create_ui()  # Create the user interface

    def create_ui(self):
        # Main frame for the lift application
        main_frame = tk.Frame(self.window, bg=self.bg_colour)  
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)  # Packing the main frame

        # Floor display at the top of the window
        display_frame = tk.Frame(main_frame, bg='#241a1a', bd=2, relief=tk.SUNKEN)  
        display_frame.pack(fill=tk.X, pady=(0, 10))  # Packing the display frame

        # Label to show the current floor
        self.floor_label = tk.Label(display_frame,
                                    text="▣ 1 ▣",  # floor display
                                    font=('Impact', 22),  # Font size for the floor label
                                    fg=self.button_active_colour,
                                    bg='#241a1a')
        self.floor_label.pack(pady=6)  # Packing the floor

        # Direction indicator for the lift
        self.direction_indicator = tk.Label(display_frame,
                                            text=self.default_arrow_symbol,  #Arrow symbol
                                            font=('Impact', 16),
                                            fg=self.text_colour,
                                            bg='#241a1a')
        self.direction_indicator.pack(pady=(0, 6))  # Packing the direction indicator

        # Lift and Character canvas
        self.floor_height = 20  # Height of each floor
        canvas_height = self.total_floors * self.floor_height + 20  # Total height of the canvas
        self.character_canvas = tk.Canvas(main_frame, width=110, height=canvas_height, bg='#241a1a', bd=2, relief=tk.SUNKEN)
        self.character_canvas.pack(pady=(0, 12))  # Packing the character canvas

        # Draw lift shaft background for each floor
        for floor in range(1, self.total_floors + 1):
            y = canvas_height - (floor * self.floor_height)  # Calculate the y position for each floor
            self.character_canvas.create_line(10, y, 100, y, fill='#4a3b3a', width=1)  # Draw the floor line
            self.character_canvas.create_text(5, y - (self.floor_height // 2), text=str(floor), fill=self.text_colour, font=('Arial', 9), anchor='w')  # Label the floor

        # Draw lift cage 
        self.lift_left_x = 20  # Left side of the lift
        self.lift_right_x = 90  # Right side of the lift
        self.lift_height = int(self.floor_height * 0.7)  # Height of the lift
        self.lift_border_colour = '#d1a6a3'  # Border colour for the lift
        initial_y_bottom = canvas_height - (self.current_floor * self.floor_height)  # Bottom position of the lift
        initial_y_top = initial_y_bottom - self.lift_height  # Top position of the lift
        self.lift_rect = self.character_canvas.create_rectangle(
            self.lift_left_x, initial_y_top, self.lift_right_x, initial_y_bottom,
            fill=self.lift_colour, outline=self.lift_border_colour, width=3
        )

        # Draw character inside the lift
        self.draw_character(initial_y_top, initial_y_bottom)  # Draw the character in the lift

        # Buttons for each floor
        button_frame = tk.Frame(main_frame, bg=self.bg_colour)  # Frame for buttons
        button_frame.pack()

        # Create buttons for each floor
        for i, floor in enumerate(range(self.total_floors, 0, -1)):
            floor_button = tk.Button(button_frame,
                                     text=str(floor),
                                     command=lambda f=floor: self.move_to_floor(f),  # Move to the selected floor
                                     bg=self.button_colour,
                                     fg=self.text_colour,
                                     activebackground=self.button_active_colour,
                                     activeforeground='black',
                                     font=self.button_font,
                                     width=4,
                                     height=2,
                                     relief=tk.GROOVE,
                                     bd=2)
            floor_button.grid(row=i // 4, column=i % 4, padx=3, pady=3)  # Grid layout for buttons
            setattr(self, f'floor_button_{floor}', floor_button)  # Set the button

        # Message log to display actions
        log_frame = tk.Frame(main_frame, bg='#241a1a')  # Log frame
        log_frame.pack(fill=tk.X, pady=(12, 0))

        self.message_log = tk.Text(log_frame,
                                   height=5,
                                   width=25,
                                   bg='#241a1a',
                                   fg=self.text_colour,
                                   font=('Arial', 9),
                                   relief=tk.SUNKEN,
                                   bd=1)
        self.message_log.pack(padx=3, pady=3)  # Packing the message log
        self.message_log.insert(tk.END, "Ready to go up!\n")  # message
        self.message_log.config(state=tk.DISABLED)  # Disable editing of the log

        # Exit button to close the application
        exit_button = tk.Button(main_frame, text="Exit the lift", command=self.exit_program, bg=self.button_colour, fg=self.text_colour, font=self.button_font, width=10, height=2)
        exit_button.pack(pady=(10, 0))  # Packing the exit button

    def draw_character(self, y_top, y_bottom):
        # Clear previous character parts if they already exist
        if hasattr(self, "character_parts"):
            for part in self.character_parts:
                self.character_canvas.delete(part)  # Delete previous character parts

        self.character_parts = []  # Resetting character parts

        # Character position - vertical centre inside lift cage
        center_x = (self.lift_left_x + self.lift_right_x) / 2  # Centre x position
        center_y = (y_top + y_bottom) / 2  # Centre y position

        # Head - circle
        head_radius = 6  # Radius of the head
        head = self.character_canvas.create_oval(center_x - head_radius, center_y - 18 - head_radius,
                                                 center_x + head_radius, center_y - 18 + head_radius,
                                                 fill=self.character_colour, outline=self.character_outline, width=2)
        self.character_parts.append(head)  # Adding head to parts

        # Body - line
        body = self.character_canvas.create_line(center_x, center_y - 12, center_x, center_y + 7, fill=self.character_outline, width=3)
        self.character_parts.append(body)  # Adding body to parts

        # Arms - lines
        left_arm = self.character_canvas.create_line(center_x, center_y - 7, center_x - 14, center_y + 1, fill=self.character_outline, width=2)
        right_arm = self.character_canvas.create_line(center_x, center_y - 7, center_x + 14, center_y + 1, fill=self.character_outline, width=2)
        self.character_parts.extend([left_arm, right_arm])  # Adding arms to parts

        # Legs - lines
        left_leg = self.character_canvas.create_line(center_x, center_y + 7, center_x - 9, center_y + 23, fill=self.character_outline, width=2)
        right_leg = self.character_canvas.create_line(center_x, center_y + 7, center_x + 9, center_y + 23, fill=self.character_outline, width=2)
        self.character_parts.extend([left_leg, right_leg])  # Adding legs to parts

    def move_to_floor(self, destination_floor):
        if self.lift_moving:
            self.log_message("Lift is currently moving. Please wait.")  # Can't move while moving
            return

        if destination_floor == self.current_floor:
            self.log_message("You are already on this floor.")  # Already at the selected floor
            return

        self.lift_moving = True  # Lift is now moving
        self.log_message(f"Moving to floor {destination_floor}...")  # Log the movement

        # Show direction
        if destination_floor > self.current_floor:
            self.direction_indicator.config(text="↑", fg='#e8e84a')  # Up arrow
        else:
            self.direction_indicator.config(text="↓", fg='#e84a4a')  # Down arrow

        # Highlight destination button
        destination_button = getattr(self, f'floor_button_{destination_floor}')  # Get the button for the destination floor
        destination_button.config(bg=self.button_active_colour)  # Change button colour

        step = 1 if destination_floor > self.current_floor else -1  # Determine direction
        for _ in range(self.current_floor, destination_floor, step):
            time.sleep(0.16)  # Wait a bit
            self.current_floor += step  # Move the lift
            self.floor_label.config(text=f"▣ {self.current_floor} ▣")  # Update floor label
            self.window.update()  # Refresh the window

            # Update lift position and character position
            self.update_lift_and_character_position()  # Update positions

        # Reset indicators
        self.direction_indicator.config(text=self.default_arrow_symbol, fg=self.text_colour)  # Reset arrow
        destination_button.config(bg=self.button_colour)  # Reset button colour
        self.log_message(f"Arrived at floor {destination_floor}.")  # Log arrival
        self.lift_moving = False  # Lift has stopped moving

    def update_lift_and_character_position(self):
        canvas_height = self.total_floors * self.floor_height + 20  # Total height of the canvas
        y_bottom = canvas_height - (self.current_floor * self.floor_height)  # Bottom position of the lift
        y_top = y_bottom - self.lift_height  # Top position of the lift

        # Move the lift cage rectangle
        self.character_canvas.coords(self.lift_rect, self.lift_left_x, y_top, self.lift_right_x, y_bottom)  # Move the lift

        # Redraw character
        self.draw_character(y_top, y_bottom)  # Redraw character

    def trigger_emergency_stop(self):
        if self.lift_moving:
            self.lift_moving = False  # Stop the lift
            self.log_message("Emergency stop activated!")  # Log the emergency
            self.direction_indicator.config(text="✖", fg='#e84a4a')  # Show emergency symbol
        else:
            self.log_message("Lift is not moving.")  # Can't stop if not moving

    def log_message(self, message):
        self.message_log.config(state=tk.NORMAL)  # Enable log editing
        self.message_log.insert(tk.END, "• " + message + "\n")  # Log the message
        self.message_log.see(tk.END)  # Scroll to the end
        self.message_log.config(state=tk.DISABLED)  # Disable editing again

    def clear_log(self):
        self.message_log.config(state=tk.NORMAL)  # Enable log editing
        self.message_log.delete(1.0, tk.END)  # Clear the log
        self.message_log.config(state=tk.DISABLED)  # Disable editing again

    def exit_program(self):
        self.window.destroy()  # Close the window

if __name__ == "__main__":
    root = tk.Tk()
    app = Lift(root)
    root.mainloop()  # Start the main loop
