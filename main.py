```python
import tkinter as tk
from tkinter import messagebox, simpledialog

from logger import log
from xiv_api import detect_highest_ilvl, fetch_gear_range
from optimizer import split_by_slot, filter_blacklist
from solver import find_best_sets

current_max_ilvl = None
current_gear_pool = []


def detect_ilvl():
    global current_max_ilvl

    log("Detect iLvl button pressed")

    current_max_ilvl = detect_highest_ilvl()

    if current_max_ilvl:
        messagebox.showinfo("Success", f"Detected highest iLvl: {current_max_ilvl}")
    else:
        messagebox.showerror("Error", "Failed to detect highest item level.")


def build_set():
    global current_max_ilvl
    global current_gear_pool

    if not current_max_ilvl:
        messagebox.showerror("Error", "Detect highest iLvl first.")
        return

    min_ilvl = current_max_ilvl - 30

    log(f"Building gear pool {min_ilvl} - {current_max_ilvl}")

    current_gear_pool = fetch_gear_range(min_ilvl, current_max_ilvl)

    if not current_gear_pool:
        messagebox.showerror("Error", "No gear returned from API.")
        return

    blacklist_input = simpledialog.askstring(
        "Blacklist",
        "Enter item names to blacklist (comma separated):"
    )

    blacklist = []

    if blacklist_input:
        blacklist = [x.strip() for x in blacklist_input.split(",") if x.strip()]

    filtered = filter_blacklist(current_gear_pool, blacklist)

    if not filtered:
        messagebox.showerror("Error", "All items removed by blacklist.")
        return

    slots = split_by_slot(filtered)

    if not slots:
        messagebox.showerror("Error", "Failed to split gear into slots.")
        return

    log("Running solver for best gear sets")

    try:
        best_sets = find_best_sets(slots, blacklist, top_n=10)
    except Exception as e:
        log(f"Solver error: {e}")
        messagebox.showerror("Error", f"Solver crashed: {e}")
        return

    if not best_sets:
        messagebox.showerror("Error", "Solver returned no results.")
        return

    output_lines = []

    for index, (score, gear) in enumerate(best_sets, start=1):

        output_lines.append(f"=== Set #{index} ===")
        output_lines.append(f"Estimated DPS: {round(score)}")

        for item in gear.values():
            output_lines.append(
                f"{item['name']} (i{item['ilvl']})"
            )

        output_lines.append("")

    result_text = "\n".join(output_lines)

    log("Solver completed successfully")

    messagebox.showinfo("Best Gear Sets", result_text)


def start_gui():
    root = tk.Tk()

    root.title("FFXIV BLM Gear Solver")
    root.geometry("320x180")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    detect_button = tk.Button(
        frame,
        text="Detect Highest iLvl",
        command=detect_ilvl,
        width=28
    )
    detect_button.pack(pady=5)

    build_button = tk.Button(
        frame,
        text="Build Best Sets",
        command=build_set,
        width=28
    )
    build_button.pack(pady=5)

    log("===================================")
    log("Application Started")

    root.mainloop()


if __name__ == "__main__":
    start_gui()
```
