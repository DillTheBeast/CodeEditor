import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import os
import keyboard
os.environ['TK_SILENCE_DEPRECATION'] = '1'


class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Code Editor")
        
        self.numLines = 1

        # Create a Text widget for line numbers
        self.line_number_widget = tk.Text(root, width=4, height=30, borderwidth=0, highlightthickness=0, wrap=tk.NONE)
        self.line_number_widget.grid(row=0, column=0, sticky="nsew")
        self.line_number_widget.config(state=tk.DISABLED)

        # Create a Text widget with a vertical scrollbar
        self.text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, borderwidth=1, highlightthickness=1)
        self.text_widget.grid(row=0, column=1, sticky="nsew")
        self.text_widget.bind('<Configure>', self.update_line_numbers)
        self.text_widget.config(font=('Courier', 12))  # Adjust font size and family as needed

        # Vertical scrollbar for the Text widget
        scrollbar = tk.Scrollbar(root, command=self.text_widget.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.text_widget.config(yscrollcommand=scrollbar.set)
        root.bind('<Return>', self.handle_key_press)  # Bind the Return key to the handle_key_press method

        # Listbox to display files and subdirectories
        self.file_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=30, height=30, borderwidth=1, highlightthickness=1)
        self.file_listbox.grid(row=0, column=3, sticky="nsew")

        # Vertical scrollbar for the Listbox
        listbox_scrollbar = tk.Scrollbar(root, command=self.file_listbox.yview)
        listbox_scrollbar.grid(row=0, column=4, sticky="ns")
        self.file_listbox.config(yscrollcommand=listbox_scrollbar.set)

        # Configure row and column weights for expansion
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)
        root.grid_columnconfigure(3, weight=1)

        # Bind click event to text widget
        self.text_widget.bind("<Button-1>", self.text_widget_click)
        # Bind click event to scrollbar (to focus on Text widget when scrollbar is clicked)
        scrollbar.bind("<Button-1>", self.text_widget_click)

        # Menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)


        # Adding Commands to work
        root.bind('<Command-s>', self.save_file)
        root.bind('<Control-s>', self.save_file)
        root.bind('<Command-n>', self.new_file)
        root.bind('<Control-n>', self.new_file)
        root.bind('<Command-o>', self.open_file)
        root.bind('<Control-o>', self.open_file)
        root.bind('<Command-e>', self.custom_destroy)  # Rename destroy method

        # Open a folder prompt when the application launches
        self.open_file()

    def handle_key_press(self, event):
        print("Test")

    def text_widget_click(self, event):
        self.text_widget.focus_set()

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)

    def open_selected_file(self, event):
        # Get the selected file from the Listbox
        selected_file_index = self.file_listbox.curselection()
        if selected_file_index:
            selected_file = self.file_listbox.get(selected_file_index)
            file_path = os.path.join(self.current_folder_path, selected_file)

            # Open the file and load its content into the Text widget
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)

            # Update the file_path attribute for save operations
            self.file_path = file_path  # Update the file_path here

            # Additionally, update the window title to display the current file name
            self.root.title(f"Simple Code Editor - {selected_file}")

    def open_file(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            # Store the current folder path for later use
            self.current_folder_path = folder_path

            # Clear existing items in the listbox
            self.file_listbox.delete(0, tk.END)

            # List files and subdirectories in the selected folder
            for item in os.listdir(folder_path):
                self.file_listbox.insert(tk.END, item)

    def save_file(self, event=None):
        # Check if there is a file_path associated with the current content
        if hasattr(self, 'file_path') and self.file_path:
            with open(self.file_path, 'w') as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
        else:
            # If no file_path is associated, prompt for a file name to save as
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            # Check if the user entered a file extension
            if not file_path.endswith((".txt", ".md", ".py")):
                # If no file extension is provided, ask the user for the file type
                file_type = filedialog.askstring("File Type", "Enter file type (e.g., txt, md, py):")
                if file_type is not None:  # Check if file_type is not None
                    # Add the file extension to the file_path
                    file_path += f".{file_type.strip().lower()}"

            with open(file_path, 'w') as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.file_path = file_path

    def custom_destroy(self):
        self.root.destroy()

    def update_line_numbers(self, event=None):
        line_numbers = '\n'.join(str(i) for i in range(1, self.numLines + 2))
        self.line_number_widget.config(state=tk.NORMAL)
        self.line_number_widget.delete(1.0, tk.END)
        self.line_number_widget.insert(tk.END, line_numbers)
        self.line_number_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()