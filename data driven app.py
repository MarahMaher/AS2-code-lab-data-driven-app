import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Reference: Data Driven App - Brief (3).docx
# API Source: https://potterdb.com/

class PotterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wizarding World Data Explorer")
        self.geometry("700x600")
        self.configure(bg="#1A1A1A")  # Dark background for a magical feel

        # Define styles for ttk buttons
        style = ttk.Style()
        style.configure("TButton", font=("Verdana", 10, "bold"), padding=5)

        container = tk.Frame(self, bg="#1A1A1A")
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, SearchPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#740001")  # Gryffindor Red
        self.controller = controller
        
        # Header Section
        header = tk.Label(self, text="HARRY POTTER EXPLORER", 
                         font=("Garamond", 28, "bold"), fg="#EEBA30", bg="#740001")
        header.pack(pady=40)

        # Instruction Box[cite: 1]
        instr_frame = tk.LabelFrame(self, text=" Instructions ", fg="#EEBA30", bg="#740001", font=("Arial", 10, "bold"))
        instr_frame.pack(pady=10, padx=50, fill="both")

        instructions = tk.Label(instr_frame, 
                                text="• Enter the Search area to find characters\n"
                                     "• Type a name (e.g., 'Hermione') and hit Search\n"
                                     "• Results include House and Patronus details", 
                                justify="left", font=("Arial", 11), fg="white", bg="#740001", padx=10, pady=10)
        instructions.pack()

        enter_btn = tk.Button(self, text="ENTER THE GREAT HALL", font=("Verdana", 12, "bold"),
                             bg="#EEBA30", fg="#740001", command=lambda: controller.show_frame("SearchPage"),
                             cursor="hand2", relief="raised")
        enter_btn.pack(pady=40)

class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2A2A2A")
        self.controller = controller

        # Navigation Header
        nav_bar = tk.Frame(self, bg="#740001", height=50)
        nav_bar.pack(side="top", fill="x")
        
        back_btn = tk.Button(nav_bar, text="← Back", bg="#EEBA30", command=lambda: controller.show_frame("StartPage"))
        back_btn.pack(side="left", padx=10, pady=5)

        # Search Control Group
        search_group = tk.LabelFrame(self, text=" Find Wizard/Witch ", bg="#2A2A2A", fg="#EEBA30", padx=10, pady=10)
        search_group.pack(pady=20, padx=20, fill="x")

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_group, textvariable=self.search_var, font=("Arial", 12), width=30)
        search_entry.pack(side="left", padx=10)

        search_btn = tk.Button(search_group, text="Search API", bg="#EEBA30", font=("Arial", 10, "bold"),
                              command=self.fetch_data)
        search_btn.pack(side="left", padx=5)

        # Results Display[cite: 1]
        self.results_list = tk.Listbox(self, font=("Courier", 10), bg="#FDF5E6", fg="#1A1A1A", 
                                      selectbackground="#740001", width=80, height=18)
        self.results_list.pack(pady=10, padx=20)

    def fetch_data(self):
        """Fetches data from API and handles errors[cite: 1]"""
        query = self.search_var.get()
        if not query:
            messagebox.showwarning("System Message", "Please provide a name to query the database.")
            return

        self.results_list.delete(0, tk.END)
        self.results_list.insert(tk.END, "Fetching data from Ministry of Magic...")

        try:
            # Querying the PotterDB API as required[cite: 1]
            api_url = f"https://api.potterdb.com/v1/characters?filter[name_cont]={query}"
            response = requests.get(api_url, timeout=10)
            data = response.json()
            characters = data.get('data', [])

            self.results_list.delete(0, tk.END)

            if not characters:
                messagebox.showinfo("No Results", f"No record found for '{query}'.")
            else:
                for char in characters:
                    attrs = char['attributes']
                    name = attrs.get('name', 'Unknown')
                    house = attrs.get('house', 'N/A')
                    patronus = attrs.get('patronus', 'None')
                    self.results_list.insert(tk.END, f" {name.upper()}")
                    self.results_list.insert(tk.END, f"   ↳ House: {house} | Patronus: {patronus}")
                    self.results_list.insert(tk.END, "-"*60)

        except Exception as e:
            messagebox.showerror("API Error", "Could not connect to the Harry Potter API. Check connection.")

if __name__ == "__main__":
    app = PotterApp()
    app.mainloop()