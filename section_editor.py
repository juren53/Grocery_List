import tkinter as tk
from tkinter import messagebox
import json
import os


class SectionEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Sections Editor")
        self.root.geometry("500x600")
        
        self.sections_file = "sections.json"
        self.sections = []
        self.drag_start_index = None
        
        # Load sections
        self.load_sections()
        
        # Create UI
        self.create_widgets()
        self.refresh_listbox()
    
    def load_sections(self):
        """Load sections from JSON file"""
        try:
            if os.path.exists(self.sections_file):
                with open(self.sections_file, 'r', encoding='utf-8') as f:
                    self.sections = json.load(f)
            else:
                messagebox.showerror("Error", f"{self.sections_file} not found!")
                self.sections = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sections: {e}")
            self.sections = []
    
    def save_sections(self):
        """Save sections to JSON file"""
        try:
            with open(self.sections_file, 'w', encoding='utf-8') as f:
                json.dump(self.sections, f, indent=4)
            messagebox.showinfo("Success", "Sections saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sections: {e}")
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Title label
        title_label = tk.Label(self.root, text="Grocery Store Sections", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="Drag and drop to reorder • Double-click to edit",
                               font=("Arial", 9), fg="gray")
        instructions.pack()
        
        # Listbox frame with scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                  font=("Arial", 10), selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Bind drag and drop events
        self.listbox.bind('<Button-1>', self.on_drag_start)
        self.listbox.bind('<B1-Motion>', self.on_drag_motion)
        self.listbox.bind('<ButtonRelease-1>', self.on_drag_release)
        self.listbox.bind('<Double-Button-1>', self.on_edit)
        
        # Entry frame for adding new sections
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(entry_frame, text="New Section:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.entry = tk.Entry(entry_frame, font=("Arial", 10))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind('<Return>', lambda e: self.add_section())
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add", command=self.add_section,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                 width=10).grid(row=0, column=0, padx=5)
        
        tk.Button(button_frame, text="Insert Before", command=self.insert_before,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 width=12).grid(row=0, column=1, padx=5)
        
        tk.Button(button_frame, text="Delete", command=self.delete_section,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                 width=10).grid(row=0, column=2, padx=5)
        
        tk.Button(button_frame, text="Save", command=self.save_sections,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                 width=10).grid(row=0, column=3, padx=5)
    
    def refresh_listbox(self):
        """Refresh the listbox with current sections"""
        self.listbox.delete(0, tk.END)
        for section in self.sections:
            self.listbox.insert(tk.END, section)
    
    def add_section(self):
        """Add a new section to the end"""
        section = self.entry.get().strip()
        if section:
            self.sections.append(section)
            self.refresh_listbox()
            self.entry.delete(0, tk.END)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(tk.END)
            self.listbox.see(tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a section name")
    
    def insert_before(self):
        """Insert a new section before the selected item"""
        selection = self.listbox.curselection()
        section = self.entry.get().strip()
        
        if not section:
            messagebox.showwarning("Warning", "Please enter a section name")
            return
        
        if selection:
            index = selection[0]
            self.sections.insert(index, section)
            self.refresh_listbox()
            self.entry.delete(0, tk.END)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
        else:
            messagebox.showwarning("Warning", "Please select a section first")
    
    def delete_section(self):
        """Delete the selected section"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            section_name = self.sections[index]
            if messagebox.askyesno("Confirm Delete", 
                                  f"Delete '{section_name}'?"):
                del self.sections[index]
                self.refresh_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a section to delete")
    
    def on_edit(self, event):
        """Edit the selected section on double-click"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            old_value = self.sections[index]
            
            # Create edit dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Section")
            dialog.geometry("400x100")
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(dialog, text="Section Name:", font=("Arial", 10)).pack(pady=5)
            
            edit_entry = tk.Entry(dialog, font=("Arial", 10), width=40)
            edit_entry.pack(pady=5)
            edit_entry.insert(0, old_value)
            edit_entry.select_range(0, tk.END)
            edit_entry.focus()
            
            def save_edit():
                new_value = edit_entry.get().strip()
                if new_value:
                    self.sections[index] = new_value
                    self.refresh_listbox()
                    self.listbox.selection_set(index)
                    dialog.destroy()
                else:
                    messagebox.showwarning("Warning", "Section name cannot be empty")
            
            edit_entry.bind('<Return>', lambda e: save_edit())
            
            btn_frame = tk.Frame(dialog)
            btn_frame.pack(pady=5)
            
            tk.Button(btn_frame, text="Save", command=save_edit,
                     bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                     bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=5)
    
    def on_drag_start(self, event):
        """Start dragging an item"""
        self.drag_start_index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.drag_start_index)
    
    def on_drag_motion(self, event):
        """During drag motion, highlight target position"""
        current_index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(current_index)
    
    def on_drag_release(self, event):
        """Drop the item at the new position"""
        if self.drag_start_index is None:
            return
        
        drop_index = self.listbox.nearest(event.y)
        
        if self.drag_start_index != drop_index:
            # Move the section
            section = self.sections.pop(self.drag_start_index)
            self.sections.insert(drop_index, section)
            self.refresh_listbox()
            self.listbox.selection_set(drop_index)
        
        self.drag_start_index = None


def main():
    root = tk.Tk()
    app = SectionEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
