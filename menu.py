import tkinter as tk
from tkinter import ttk

def main_screen():
    root = tk.Tk()
    root.title("Main Screen")

    def on_select(event):
        selected_table = table_combobox.get()
        if selected_table:
            # Perform action to generate screen based on selected table
            generate_dynamic_screen(selected_table)

    tables = ["Table 1", "Table 2", "Table 3"]  # Example list of tables
    table_combobox = ttk.Combobox(root, values=tables)
    table_combobox.grid(row=0, column=0, padx=10, pady=10)
    table_combobox.bind("<<ComboboxSelected>>", on_select)

    root.mainloop()

def generate_dynamic_screen(selected_table):
    # Placeholder function to generate dynamic screen based on selected table
    print(f"Generating screen for {selected_table}")

if __name__ == "__main__":
    main_screen()