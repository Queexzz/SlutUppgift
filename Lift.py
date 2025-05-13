import tkinter as tk
from tkinter import ttk, font
import time

class UniqueElevator:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Lift Simulator")
        self.root.geometry("350x550")
        self.root.configure(bg='#0a0a12')
        
        # Elevator state
        self.current_floor = 1
        self.total_floors = 8  # More floors than before but still manageable
        self.is_moving = False
        self.direction = "■"  # Can be ▲ or ▼
        
        # Custom colors
        self.bg_color = '#0a0a12'
        self.btn_color = '#3a3b4a'
        self.active_color = '#6d72e8'
        self.text_color = '#e0e0ff'
        
        # Create custom font
        self.custom_font = font.Font(family='Courier', size=12, weight='bold')
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Elevator display (top panel)
        display_frame = tk.Frame(main_frame, bg='#1a1a24', bd=2, relief=tk.RAISED)
        display_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.floor_display = tk.Label(display_frame, 
                                    text="◼ 1 ◼", 
                                    font=('Courier', 24, 'bold'),
                                    fg=self.active_color,
                                    bg='#1a1a24',
                                    padx=20)
        self.floor_display.pack(pady=10)
        
        # Direction indicator
        self.direction_indicator = tk.Label(display_frame, 
                                          text="■", 
                                          font=('Courier', 18),
                                          fg=self.text_color,
                                          bg='#1a1a24')
        self.direction_indicator.pack(pady=(0, 10))
        
        # Elevator buttons (grid layout)
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack()
        
        # Create floor buttons in a grid
        floors = list(range(self.total_floors, 0, -1))
        for i, floor in enumerate(floors):
            btn = tk.Button(btn_frame, 
                          text=str(floor),
                          command=lambda f=floor: self.call_elevator(f),
                          bg=self.btn_color,
                          fg=self.text_color,
                          activebackground=self.active_color,
                          activeforeground='white',
                          font=self.custom_font,
                          width=4,
                          height=2,
                          relief=tk.RAISED,
                          bd=3)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            setattr(self, f'btn_{floor}', btn)
        
        # Emergency button
        emergency_btn = tk.Button(btn_frame,
                                text="⏻",
                                command=self.emergency_stop,
                                bg='#e84a4a',
                                fg='white',
                                font=('Arial', 14),
                                width=4,
                                height=2,
                                relief=tk.RAISED,
                                bd=3)
        emergency_btn.grid(row=(self.total_floors//3)+1, column=1, pady=(10, 0))
        
        # Status display
        status_frame = tk.Frame(main_frame, bg='#1a1a24')
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.status = tk.Text(status_frame, 
                            height=6, 
                            width=30,
                            bg='#1a1a24',
                            fg=self.text_color,
                            font=('Courier', 10),
                            relief=tk.FLAT,
                            bd=0)
        self.status.pack(padx=5, pady=5)
        self.status.insert(tk.END, "System ready\n")
        self.status.config(state=tk.DISABLED)
        
    def call_elevator(self, target_floor):
        if self.is_moving:
            self.update_status("Elevator already in motion!")
            return
            
        if target_floor == self.current_floor:
            self.update_status(f"Already on floor {target_floor}")
            return
            
        self.is_moving = True
        self.update_status(f"Moving to floor {target_floor}")
        
        # Set direction indicator
        if target_floor > self.current_floor:
            self.direction_indicator.config(text="▲", fg='#4ae84a')  # Green up arrow
        else:
            self.direction_indicator.config(text="▼", fg='#e84a4a')  # Red down arrow
        
        # Get button to highlight during movement
        btn = getattr(self, f'btn_{target_floor}')
        btn.config(bg=self.active_color)
        
        # Simple animation
        direction = 1 if target_floor > self.current_floor else -1
        for floor in range(self.current_floor, target_floor, direction):
            time.sleep(0.3)
            self.current_floor = floor + direction
            self.floor_display.config(text=f"◼ {self.current_floor} ◼")
            self.root.update()
        
        # Reset after arrival
        self.direction_indicator.config(text="■", fg=self.text_color)  # Neutral
        btn.config(bg=self.btn_color)
        self.update_status(f"Arrived at floor {target_floor}")
        self.is_moving = False
        
    def emergency_stop(self):
        if self.is_moving:
            self.is_moving = False
            self.update_status("EMERGENCY STOP ACTIVATED!")
            self.direction_indicator.config(text="⏹", fg='#e84a4a')
        else:
            self.update_status("System is already idle")
        
    def update_status(self, message):
        self.status.config(state=tk.NORMAL)
        self.status.insert(tk.END, "> " + message + "\n")
        self.status.see(tk.END)
        self.status.config(state=tk.DISABLED)
        
    def clear_messages(self):
        self.status.config(state=tk.NORMAL)
        self.status.delete(1.0, tk.END)
        self.status.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = UniqueElevator(root)
    root.mainloop()