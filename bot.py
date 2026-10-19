import tkinter as tk
import os
import json
import sys

# Where we hide the counter
CONFIG_DIR = os.path.join(os.environ["PROGRAMDATA"], "SysUpdate")
COUNTER_FILE = os.path.join(CONFIG_DIR, "respawns.json")

def load_counter():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(COUNTER_FILE):
        return {"count": 0}
    try:
        with open(COUNTER_FILE, "r") as f:
            return json.load(f)
    except:
        return {"count": 0}

def save_counter(data):
    with open(COUNTER_FILE, "w") as f:
        json.dump(data, f)

def show_gui():
    data = load_counter()
    count = data["count"]

    if count >= 5:
        # Dead. The user finally won.
        sys.exit(0)

    # Increment the counter
    data["count"] = count + 1
    save_counter(data)

    # Show the GUI
    root = tk.Tk()
    root.title("System Alert")
    
    # Make it always on top and center it
    root.attributes("-topmost", True)
    root.geometry("300x150")
    
    msg = f"Hello! I am a test script.\nThis is life #{count + 1} of 5."
    tk.Label(root, text=msg, font=("Arial", 12), pady=20).pack()
    
    def on_close():
        root.destroy()
        sys.exit(0)

    tk.Button(root, text="OK", command=on_close, width=10).pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    show_gui()