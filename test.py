import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import os

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Code Editor")
        self.numLines = 0

        # Create a Text widget for line numbers
        self.line_number_widget = tk.Text(root, width=4, height=30, borderwidth=0, wrap=tk.NONE)
        self.line_number_widget.grid(row=0, column=0, sticky="nsew")
        self.line_number_widget.config(state=tk.DISABLED)

        # Create a Text widget with a vertical scrollbar
        self.text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, borderwidth=1, highlightthickness=1)
        self.text_widget.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        self.text_widget.config(font=('Courier', 12))

        # Bind the <B1-Motion> event to update line numbers and scroll text
        self.text_widget.bind('<B1-Motion>', self.update_line_numbers_and_scroll)
        
        # Bind the <MouseWheel> event for two-finger scroll
        self.text_widget.bind('<MouseWheel>', self.update_line_numbers_and_scroll)

        # Listbox to display files and subdirectories
        self.file_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=30, height=30, borderwidth=1, highlightthickness=1)
        self.file_listbox.grid(row=0, column=3, sticky="nsew")
        self.file_listbox.bind('<ButtonRelease-1>', self.open_selected_file)

        # Vertical scrollbar for the Listbox
        listbox_scrollbar = tk.Scrollbar(root, command=self.file_listbox.yview)
        listbox_scrollbar.grid(row=0, column=4, sticky="ns")
        self.file_listbox.config(yscrollcommand=listbox_scrollbar.set)

        # Configure row and column weights for expansion
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)

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
        root.bind('<Command-e>', self.custom_destroy)

        # Open a folder prompt when the application launches
        self.open_file()

    def text_widget_click(self, event):
        self.text_widget.focus_set()

    def new_file(self, event=None):
        self.text_widget.delete(1.0, tk.END)
        self.update_line_numbers()

    def open_selected_file(self, event):
        selected_file_index = self.file_listbox.curselection()
        if selected_file_index:
            selected_file = self.file_listbox.get(selected_file_index)
            file_path = os.path.join(self.current_folder_path, selected_file)

            with open(file_path, 'r') as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)

            self.file_path = file_path
            self.root.title(f"Simple Code Editor - {selected_file}")

            self.update_line_numbers()

    def open_file(self, event=None):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.current_folder_path = folder_path
            self.file_listbox.delete(0, tk.END)

            for item in os.listdir(folder_path):
                self.file_listbox.insert(tk.END, item)

            self.update_line_numbers()

    def save_file(self, event=None):
        if hasattr(self, 'file_path') and self.file_path:
            with open(self.file_path, 'w') as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.update_line_numbers()
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("Text files", "*.txt"),
                                                                                    ("All files", "*.*")])
        if file_path:
            if not file_path.endswith((".txt", ".md", ".py")):
                file_type = filedialog.askstring("File Type", "Enter file type (e.g., txt, md, py):")
                if file_type is not None:
                    file_path += f".{file_type.strip().lower()}"

            with open(file_path, 'w') as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.file_path = file_path
            self.update_line_numbers()

    def custom_destroy(self, event=None):
        self.root.destroy()

    def update_line_numbers(self, event=None):
        current_num_lines = int(self.text_widget.index(tk.END).split('.')[0])
        if current_num_lines != self.numLines:
            self.numLines = current_num_lines

            line_numbers = '\n'.join(str(i) for i in range(1, self.numLines + 1))
            self.line_number_widget.config(state=tk.NORMAL)
            self.line_number_widget.delete(1.0, tk.END)
            self.line_number_widget.insert(tk.END, line_numbers)
            self.line_number_widget.config(state=tk.DISABLED)

    def update_line_numbers_and_scroll(self, event):
        self.update_line_numbers()
        self.line_number_widget.yview_moveto(self.text_widget.yview()[0])

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
