import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:8000"

class ApiGui:
    def __init__(self, root):
        self.root = root
        self.root.title("API Client")
        self.root.geometry("800x500")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # Add buttons
        self.refresh_btn = ttk.Button(self.button_frame, text="Refresh Data", command=self.refresh_data)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.insert_btn = ttk.Button(self.button_frame, text="Insert Data", command=self.insert_data)
        self.insert_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_btn = ttk.Button(self.button_frame, text="Update Selected", command=self.update_data)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(self.button_frame, text="Delete Selected", command=self.delete_data)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Create table frame with scrollbar
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(self.table_frame)
        self.tree["columns"] = ("id", "nome", "idade")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.W, width=50)
        self.tree.column("nome", anchor=tk.W, width=200)
        self.tree.column("idade", anchor=tk.W, width=100)
        
        self.tree.heading("#0", text="")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("idade", text="Idade")
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load initial data
        self.refresh_data()
    
    # /------------------
    # Functions to interact with the API
    async def refresh_data(self):
        """Fetch data from API and update the table"""
        try:
            response = requests.get(f"{API_URL}/items")
            data = response.json()
            
            # Clear current table
            for i in self.tree.get_children():
                self.tree.delete(i)
                
            # Populate with new data
            for item in data:
                self.tree.insert("", tk.END, values=(item["id"], item["nome"], item["idade"]))
            
            self.status_var.set(f"Loaded {len(data)} records successfully")
        except Exception as e:
            self.status_var.set(f"Error loading data: {str(e)}")
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")
    
    def insert_data(self):
        """Open a dialog to insert new data"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Insert New Data")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nome:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        nome_var = tk.StringVar()
        nome_entry = ttk.Entry(dialog, textvariable=nome_var, width=30)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Idade:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        idade_var = tk.StringVar()
        idade_entry = ttk.Entry(dialog, textvariable=idade_var, width=30)
        idade_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def save_data():
            try:
                nome = nome_var.get()
                idade = int(idade_var.get())
                
                data = {"nome": nome, "idade": idade}
                response = requests.post(f"{API_URL}/items", json=data)
                
                if response.status_code == 200:
                    self.status_var.set("Data inserted successfully")
                    self.refresh_data()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to insert data: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save_data).grid(row=2, column=1, padx=10, pady=20)
        nome_entry.focus_set()
    
    def update_data(self):
        """Update the selected record"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Info", "Please select an item to update")
            return
        
        item_id = self.tree.item(selected_item[0], "values")[0]
        current_nome = self.tree.item(selected_item[0], "values")[1]
        current_idade = self.tree.item(selected_item[0], "values")[2]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update Record #{item_id}")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nome:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        nome_var = tk.StringVar(value=current_nome)
        nome_entry = ttk.Entry(dialog, textvariable=nome_var, width=30)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Idade:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        idade_var = tk.StringVar(value=current_idade)
        idade_entry = ttk.Entry(dialog, textvariable=idade_var, width=30)
        idade_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def update():
            try:
                nome = nome_var.get()
                idade = int(idade_var.get())
                
                data = {"nome": nome, "idade": idade}
                response = requests.put(f"{API_URL}/items/{item_id}", json=data)
                
                if response.status_code == 200:
                    self.status_var.set("Data updated successfully")
                    self.refresh_data()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to update data: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        ttk.Button(dialog, text="Update", command=update).grid(row=2, column=1, padx=10, pady=20)
        nome_entry.focus_set()
    
    def delete_data(self):
        """Delete the selected record"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Info", "Please select an item to delete")
            return
        
        item_id = self.tree.item(selected_item[0], "values")[0]
        
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete record #{item_id}?")
        if not confirm:
            return
        
        try:
            response = requests.delete(f"{API_URL}/items/{item_id}")
            
            if response.status_code == 200:
                self.status_var.set(f"Record #{item_id} deleted successfully")
                self.refresh_data()
            else:
                messagebox.showerror("Error", f"Failed to delete data: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ApiGui(root)
    root.mainloop()