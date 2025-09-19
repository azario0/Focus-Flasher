import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import time

class FocusFlasherGUI:
    def __init__(self, master):
        self.master = master
        master.title("Focus Flasher")
        master.geometry("350x280") # Increased size for new widgets
        master.resizable(False, False)

        # Style for a more modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # --- State Variables ---
        self.is_running = False
        self.reps_left = 0
        self.after_id = None # To store the ID of scheduled events for cancellation
        self.delay_end_time = 0
        self.flash_color_hex = "#FFFFFF" # Default color is white

        # --- GUI Widgets ---
        main_frame = ttk.Frame(master, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)

        # Repetitions
        ttk.Label(main_frame, text="Repetitions:").grid(row=0, column=0, sticky="w", pady=5)
        self.reps_var = tk.StringVar(value="10000")
        self.reps_entry = ttk.Entry(main_frame, textvariable=self.reps_var, width=12)
        self.reps_entry.grid(row=0, column=1, sticky="w")

        # Delay
        ttk.Label(main_frame, text="Delay (seconds):").grid(row=1, column=0, sticky="w", pady=5)
        self.delay_var = tk.StringVar(value="45")
        self.delay_entry = ttk.Entry(main_frame, textvariable=self.delay_var, width=12)
        self.delay_entry.grid(row=1, column=1, sticky="w")

        # Duration
        ttk.Label(main_frame, text="Duration (seconds):").grid(row=2, column=0, sticky="w", pady=5)
        self.duration_var = tk.StringVar(value="0.1")
        self.duration_entry = ttk.Entry(main_frame, textvariable=self.duration_var, width=12)
        self.duration_entry.grid(row=2, column=1, sticky="w")

        # Color Chooser
        ttk.Label(main_frame, text="Flash Color:").grid(row=3, column=0, sticky="w", pady=5)
        color_frame = ttk.Frame(main_frame)
        color_frame.grid(row=3, column=1, sticky="w")
        
        self.color_preview = tk.Frame(color_frame, width=20, height=20, bg=self.flash_color_hex, relief="sunken", borderwidth=1)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 5))
        
        self.color_button = ttk.Button(color_frame, text="Choose...", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)

        self.start_button = ttk.Button(button_frame, text="Start Session", command=self.start_session)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop Session", command=self.stop_session, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_var = tk.StringVar(value="Ready to start.")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, wraplength=320, justify=tk.CENTER)
        status_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

    def choose_color(self):
        """Opens a color chooser dialog and updates the selected color."""
        color_code = colorchooser.askcolor(title="Choose flash color", initialcolor=self.flash_color_hex)
        if color_code and color_code[1]: # Check if a color was chosen (not cancelled)
            self.flash_color_hex = color_code[1] # The second element is the hex string
            self.color_preview.config(bg=self.flash_color_hex)

    def create_flash_window(self, duration_ms):
        """Creates the full-screen Toplevel window with the chosen color."""
        flash_win = tk.Toplevel(self.master)
        flash_win.overrideredirect(True)
        flash_win.configure(bg=self.flash_color_hex)
        
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        flash_win.geometry(f"{width}x{height}+0+0")

        flash_win.wm_attributes("-topmost", True)
        flash_win.lift()
        flash_win.focus_force()
        
        flash_win.after(duration_ms, flash_win.destroy)

    def start_session(self):
        """Validates input and starts the flashing sequence."""
        try:
            reps = int(self.reps_var.get())
            if reps <= 0 or float(self.delay_var.get()) < 0 or float(self.duration_var.get()) <= 0:
                raise ValueError("Values must be positive numbers.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid, positive numbers for all fields.")
            return
            
        self.is_running = True
        self.reps_left = reps
        
        # Lock UI controls
        for widget in [self.reps_entry, self.delay_entry, self.duration_entry, self.start_button, self.color_button]:
            widget.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
            
        self.run_flash_cycle()

    def run_flash_cycle(self):
        """The main loop that controls flashing and waiting."""
        if not self.is_running or self.reps_left <= 0:
            if self.is_running: # Prevents "Session finished" message if stopped manually
                self.reset_ui("Session finished!")
            return

        # --- Perform the flash ---
        reps_total = int(self.reps_var.get())
        current_rep = reps_total - self.reps_left + 1
        self.status_var.set(f"Flashing screen ({current_rep}/{reps_total})...")
        
        duration_sec = float(self.duration_var.get())
        duration_ms = int(duration_sec * 1000)
        self.create_flash_window(duration_ms)
        
        self.reps_left -= 1

        # --- Schedule the next phase (delay or finish) ---
        if self.reps_left > 0:
            # Wait for the flash to finish, then start the delay countdown
            self.after_id = self.master.after(duration_ms + 50, self.start_delay_countdown)
        else:
            # It was the last one, schedule the finish message after the flash is gone.
            self.after_id = self.master.after(duration_ms + 50, self.run_flash_cycle)
            
    def start_delay_countdown(self):
        """Kicks off the real-time countdown timer."""
        delay_sec = float(self.delay_var.get())
        self.delay_end_time = time.time() + delay_sec
        self.update_countdown()

    def update_countdown(self):
        """Updates the status label every second with the time remaining."""
        if not self.is_running:
            return

        remaining = self.delay_end_time - time.time()
        
        if remaining > 0:
            self.status_var.set(f"Waiting... Time left: {int(remaining) + 1}s")
            self.after_id = self.master.after(1000, self.update_countdown) # Check again in 1 sec
        else:
            # Delay is over, trigger the next flash
            self.run_flash_cycle()

    def stop_session(self):
        """Stops the current session and resets the UI."""
        if self.is_running:
            self.is_running = False
            if self.after_id:
                self.master.after_cancel(self.after_id)
            self.reset_ui("Session stopped by user.")

    def reset_ui(self, message):
        """Resets the UI to its initial, unlocked state."""
        self.status_var.set(message)
        for widget in [self.reps_entry, self.delay_entry, self.duration_entry, self.start_button, self.color_button]:
            widget.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = FocusFlasherGUI(root)
    # Ensure stop_session is called if the window is closed
    root.protocol("WM_DELETE_WINDOW", app.stop_session)
    root.mainloop()

if __name__ == "__main__":
    main()
