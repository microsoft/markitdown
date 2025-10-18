import tkinter as tk
from tkinter import filedialog, messagebox
import os
from markitdown._markitdown import MarkItDown

class MarkitdownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Markitdown GUI")

        self.input_files = []
        self.output_dir = ""

        # Input files selection
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        self.input_label = tk.Label(self.input_frame, text="Input Files:")
        self.input_label.pack(side=tk.LEFT)
        self.input_listbox = tk.Listbox(self.input_frame, width=50, height=5)
        self.input_listbox.pack(side=tk.LEFT, padx=5)
        self.browse_input_button = tk.Button(self.input_frame, text="Browse", command=self.browse_input_files)
        self.browse_input_button.pack(side=tk.LEFT)

        # Output directory selection
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=10)
        self.output_label = tk.Label(self.output_frame, text="Output Directory:")
        self.output_label.pack(side=tk.LEFT)
        self.output_entry = tk.Entry(self.output_frame, width=40)
        self.output_entry.pack(side=tk.LEFT, padx=5)
        self.browse_output_button = tk.Button(self.output_frame, text="Browse", command=self.browse_output_dir)
        self.browse_output_button.pack(side=tk.LEFT)

        # Convert button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_files)
        self.convert_button.pack(pady=20)

        # Status label
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

    def browse_input_files(self):
        files = filedialog.askopenfilenames(
            title="Select Input Files",
            filetypes=(("All files", "*.*"),)
        )
        if files:
            self.input_files = list(files)
            self.input_listbox.delete(0, tk.END)
            for file in self.input_files:
                self.input_listbox.insert(tk.END, file)

    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, self.output_dir)

    def convert_files(self):
        if not self.input_files:
            messagebox.showerror("Error", "Please select at least one input file.")
            return

        output_dir = self.output_entry.get()
        if not output_dir:
            output_dir = None

        md = MarkItDown()

        for file_path in self.input_files:
            try:
                self.status_label.config(text=f"Converting {file_path}...")
                self.root.update_idletasks()

                result = md.convert(file_path)

                if output_dir:
                    output_path = os.path.join(output_dir, os.path.basename(file_path) + ".md")
                else:
                    output_path = os.path.splitext(file_path)[0] + ".md"

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result.text_content)

                self.status_label.config(text=f"Successfully converted {file_path}")

            except Exception as e:
                self.status_label.config(text=f"Error converting {file_path}: {e}")
                messagebox.showerror("Error", f"Could not convert {file_path}:\n{e}")

        self.status_label.config(text="Conversion complete.")
        messagebox.showinfo("Success", "All files converted successfully.")

def main():
    root = tk.Tk()
    app = MarkitdownGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
