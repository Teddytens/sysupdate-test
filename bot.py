import tkinter as tk
import os
import json
import sys
import subprocess
import random

CONFIG_DIR = os.path.join(os.environ.get("PROGRAMDATA", os.path.expanduser("~")), "SysUpdate")
STATE_FILE = os.path.join(CONFIG_DIR, "hydra.json")

def load_state():
    if not os.path.exists(CONFIG_DIR):
        try: os.makedirs(CONFIG_DIR)
        except: pass
    if not os.path.exists(STATE_FILE):
        return {"spawned": 0, "active": 0}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"spawned": 0, "active": 0}

def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except: pass

def show_window():
    root = tk.Tk()
    root.title("Message")
    
    # Scatter them randomly
    x = random.randint(200, 1000)
    y = random.randint(200, 600)
    root.geometry(f"340x180+{x}+{y}")
    
    root.attributes("-topmost", True)
    root.resizable(False, False)

    msg = "Love you <3 -TeddyL"
    label = tk.Label(root, text=msg, font=("Segoe UI", 14, "bold"), pady=30)
    label.pack()

    def on_close():
        state = load_state()
        state["active"] -= 1
        
        spawns_left = 20 - state["spawned"]
        to_spawn = min(2, spawns_left)
        
        for _ in range(to_spawn):
            state["active"] += 1
            state["spawned"] += 1
            subprocess.Popen([sys.executable, sys.argv[0], "--child"])
            
        save_state(state)
        root.destroy()

    btn = tk.Button(root, text="OK", command=on_close, width=12, font=("Segoe UI", 10))
    btn.pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    root.mainloop()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        show_window()
        return

    state = load_state()
    
    if state["spawned"] >= 20:
        sys.exit(0)

    if state["active"] == 0:
        state["spawned"] = 1
        state["active"] = 1
        save_state(state)
        subprocess.Popen([sys.executable, sys.argv[0], "--child"])

if __name__ == "__main__":
    main()