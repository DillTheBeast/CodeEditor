import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Code Editor")

        # Create a Text widget with a vertical scrollbar
        self.text_widget = tk.Text(root, wrap=tk.WORD, width=300, height=300)
        self.text_widget.grid(row=0, column=0, sticky="nsew")

        # Vertical scrollbar
        scrollbar = tk.Scrollbar(root, command=self.text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.config(yscrollcommand=scrollbar.set)

        # Configure row and column weights for expansion
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Bind click event to text widget
        self.text_widget.bind("<Button-1>", self.text_widget_click)

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

    def text_widget_click(self, event):
        self.text_widget.focus_set()

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)

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
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
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

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
