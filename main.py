import tkinter as tk
from tkinter import messagebox, simpledialog

from logger import log
from xivapi import detect_highest_ilvl, fetch_gear_range
from optimizer import build_best_set
from materia import apply_materia_logic

current_max_ilvl = None
current_gear_pool = []


def detect_ilvl():
    global current_max_ilvl
    current_max_ilvl = detect_highest_ilvl()

    if current_max_ilvl:
        messagebox.showinfo("Success", f"Detected highest iLvl: {current_max_ilvl}")
    else:
        messagebox.showerror("Error", "Failed to detect iLvl")


def build_set():
    global current_max_ilvl
    global current_gear_pool

    if not current_max_ilvl:
        messagebox.showerror("Error", "Detect iLvl first.")
        return

    min_ilvl = current_max_ilvl - 30
    current_gear_pool = fetch_gear_range(min_ilvl, current_max_ilvl)

    blacklist_input = simpledialog.askstring(
        "Blacklist",
        "Enter item names to blacklist (comma separated):"
    )

    blacklist = []
    if blacklist_input:
        blacklist = [x.strip() for x in blacklist_input.split(",")]

    best = build_best_set(current_gear_pool, blacklist)
    optimized = apply_materia_logic(best)

    output = "\n".join(
        f"{item['Name']} (i{item['LevelItem']}) - Materia Slots: {item['MateriaSlotsUsed']}"
        for item in optimized
    )

    messagebox.showinfo("Best Set", output)


root = tk.Tk()
root.title("FFXIV Gear Optimizer")

tk.Button(root, text="Detect Highest iLvl", command=detect_ilvl, width=30).pack(pady=10)
tk.Button(root, text="Build Best Set", command=build_set, width=30).pack(pady=10)

log("===================================")
log("Application Started")

root.mainloop()
