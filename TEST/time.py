import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_hour = hours_combobox.get()
    selected_minute = minutes_combobox.get()
    time_label.config(text=f"Selected time: {selected_hour}:{selected_minute}")

root = tk.Tk()

hours_combobox = ttk.Combobox(root, values=list(range(0, 24)), width=5)
hours_combobox.pack()
hours_combobox.current(0)

minutes_combobox = ttk.Combobox(root, values=list(range(0, 60, 5)), width=5)
minutes_combobox.pack()
minutes_combobox.current(0)

time_label = ttk.Label(root, text="Selected time: 00:00")
time_label.pack()

hours_combobox.bind("<<ComboboxSelected>>", on_select)
minutes_combobox.bind("<<ComboboxSelected>>", on_select)

root.mainloop()