import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Code Editor")

        # Create a scrolled text widget
        self.text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
        self.text_widget.pack(expand=True, fill='both')

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
        
        # Bind Command+S (or Control+S) to save_file function
        root.bind('<Command-s>', self.save_file)
        root.bind('<Control-s>', self.save_file)

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
            with open(file_path, 'w') as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.file_path = file_path


if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
