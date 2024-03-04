import customtkinter
import tkinter

root = customtkinter.CTk()
root.title("Dynamic Checkbox Display")

# Variables for checkboxes
var1 = tkinter.IntVar()
var2 = tkinter.IntVar()

# Create checkboxes
checkbox1 = customtkinter.CTkCheckBox(root, text="Option 1", variable=var1)
checkbox1.pack()
checkbox2 = customtkinter.CTkCheckBox(root, text="Option 2", variable=var2)
checkbox2.pack()

# Display label
display_label = customtkinter.CTkLabel(root, text="")
display_label.pack()

def update_label(*args):
    checked_values = []
    if var1.get() == 1:
        checked_values.append("Option 1")
    if var2.get() == 1:
        checked_values.append("Option 2")

    display_label.configure(text="Checked values: " + ", ".join(checked_values))

# Trace changes to the checkbox variables
var1.trace_add("write", update_label)
var2.trace_add("write", update_label)

root.mainloop()
