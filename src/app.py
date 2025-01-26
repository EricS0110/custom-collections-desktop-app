import customtkinter

APP_TITLE = "Collection Manager"
APP_GEOMETRY = "900x800"

class WelcomeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.heading_label = customtkinter.CTkLabel(
            self, text=f"Welcome to the {APP_TITLE} application", font=('Arial', 20)
        )
        self.heading_label.grid(row=0, column=0, sticky='we', padx=10, pady=10)
        main_body_text = """
        This app will help you manage what items are stored in your MongoDB collection.
        
        Tabs:
        
        - Welcome: This tab
        
        - New Collection: Create a new collection
        
        - Add One: Add one item to the collection
        
        - Add Bulk: Add multiple items to the collection
        
        - Download: Download a collection as an Excel file
        
        - Search: Search for items in the collection
        
        - Delete: Delete items from the collection
        """
        self.main_body_label = customtkinter.CTkLabel(self, text=main_body_text, font=('Arial', 16), anchor='w', justify='left')
        self.main_body_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)



class MainTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.add("    Welcome    ")
        self.add("    New Collection    ")
        self.add("    Add One    ")
        self.add("    Add Bulk    ")
        self.add("    Download    ")
        self.add("    Search    ")
        self.add("    Delete    ")

        self.welcome_frame = WelcomeFrame(master=self.tab("    Welcome    "))
        self.welcome_frame.pack(anchor='w', expand=True, fill='both')



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        self.main_tab_view = MainTabView(self)
        self.main_tab_view.pack(anchor='e', expand=True, fill='both')


if __name__ == '__main__':
    app = App()
    app.mainloop()
