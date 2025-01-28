import datetime
import logging
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter
import pandas as pd
from customtkinter import CTkFont

from src.logging_config import setup_logging
from src.security import load_settings

APP_TITLE = "Collection Manager"
APP_GEOMETRY = "900x800"

# Initialize logging
setup_logging()


class WelcomeFrame(customtkinter.CTkFrame):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)
        self.heading_label = customtkinter.CTkLabel(
            self,
            text=f"Welcome to the {APP_TITLE} application",
            font=CTkFont(family="Arial", size=24, weight="bold", underline=True),
        )
        self.heading_label.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        main_body_text = """
        This app will help you manage what items are stored in your MongoDB collection.


        Tabs:

        - Welcome: This tab

        - Settings: Application settings (not persistent)

        - New Collection: Create a new collection

        - Add One: Add one item to the collection

        - Add Bulk: Add multiple items to the collection

        - Download: Download a collection as an Excel file

        - Search: Search for items in the collection

        - Delete: Delete items from the collection
        """
        self.main_body_label = customtkinter.CTkLabel(
            self, text=main_body_text, font=CTkFont(family="Arial", size=16), anchor="w", justify="left"
        )
        self.main_body_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        at_a_glance_text = f"""
        Database: {settings.mongo_database}
        """
        for key, value in settings.mongo_connection.summarize_collection_counts().items():
            at_a_glance_text += f"\n\t{key}: {value}"
        self.at_a_glance_label = customtkinter.CTkLabel(
            self, text=at_a_glance_text, font=("Arial", 16), anchor="w", justify="left"
        )
        self.at_a_glance_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)


class DarkModeToggleFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        def switch_event():
            if self.switch_var.get() == "on":
                customtkinter.set_appearance_mode("dark")
            elif self.switch_var.get() == "off":
                customtkinter.set_appearance_mode("light")

        self.switch_var = customtkinter.StringVar(value="on")
        self.dark_mode_toggle = customtkinter.CTkSwitch(
            master, text="Dark Mode", command=switch_event, variable=self.switch_var, onvalue="on", offvalue="off"
        )
        self.dark_mode_toggle.pack(side="top", padx=10, pady=10)


class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)
        self.dark_mode_toggle_frame = DarkModeToggleFrame(self)
        self.dark_mode_toggle_frame.pack(side="top", anchor="w", expand=True, fill="both")


class NewCollectionFrame(customtkinter.CTkFrame):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)

        def create_collection():
            collection_name = self.collection_name_entry.get()
            if collection_name == "":
                return
            try:
                settings.mongo_connection.add_collection(collection_name)
            except Exception as e:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(title="Error", message=f"Error creating collection: {e}\n\nIt may already exist.")
                root.destroy()
            self.collection_name_entry.delete(0, "end")
            self.collections = settings.mongo_connection.list_collection_names()
            self.collection_list.configure(text=", ".join(self.collections))
            logging.info(f"NEW COLLECTION CREATED: {collection_name}")
            return

        self.heading_label = customtkinter.CTkLabel(
            self, text="Create a new collection", font=CTkFont(family="Arial", size=24, weight="bold", underline=True)
        )
        self.heading_label.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        self.collection_name_label = customtkinter.CTkLabel(self, text="Collection Name:")
        self.collection_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.collection_name_entry = customtkinter.CTkEntry(self)
        self.collection_name_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        self.create_collection_button = customtkinter.CTkButton(
            self, text="Create Collection", command=create_collection
        )
        self.create_collection_button.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        # Add a list of the current collections for the user and a button to refresh the list
        self.collection_list_label = customtkinter.CTkLabel(self, text="Current Collections:")
        self.collection_list_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.collection_list = customtkinter.CTkLabel(self)
        self.collection_list.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        self.collections = settings.mongo_connection.list_collection_names()
        self.collection_list.configure(text=", ".join(self.collections))

        def refresh_list():
            self.collections = settings.mongo_connection.list_collection_names()
            self.collection_list.configure(text=", ".join(self.collections))
            return

        self.refresh_button = customtkinter.CTkButton(self, text="Refresh List", command=refresh_list)
        self.refresh_button.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)


class CollectionsDropdownWithAllFrame(customtkinter.CTkFrame):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)
        self.collection_label = customtkinter.CTkLabel(self, text="Collection:")
        self.collection_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.collection_dropdown = customtkinter.CTkComboBox(
            self, values=["All"] + settings.mongo_connection.list_collection_names()
        )
        self.collection_dropdown.grid(row=0, column=1, sticky="w", padx=10, pady=10)


class AddOneFrame(customtkinter.CTkFrame):
    """
    Frame for adding a single item to a collection. Populate the currently available fields for all documents in the selected collection.
    Update the available fields when the collection is changed to reflect the new collection's fields.
    """

    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)
        self.settings = settings
        self.item_to_add = {}
        self.collection_label = customtkinter.CTkLabel(self, text="Collection:")
        self.collection_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.collection_dropdown = customtkinter.CTkComboBox(
            self, values=settings.mongo_connection.list_collection_names(), command=self.refresh_fields
        )
        self.collection_dropdown.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        self.fields_frame = customtkinter.CTkFrame(self)
        self.fields_frame.grid(row=1, column=0, sticky="w", padx=10, pady=10, columnspan=2)

        self.create_fields()

        # Add a button to preview the item to the collection based on the fields and values entered by the user
        self.preview_item_button = customtkinter.CTkButton(self, text="Check Item", command=self.preview_item)
        self.preview_item_button.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        # Add a label in column 2 to display a preview of the item to be added
        # based on the available fields and values entered by the user
        self.preview_label = customtkinter.CTkLabel(self, text="Preview:")
        self.preview_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.preview_text = customtkinter.CTkTextbox(self, width=200, height=100)
        self.preview_text.grid(row=3, column=1, sticky="w", padx=10, pady=10)

        # Add a button to add the item to the collection
        self.add_item_button = customtkinter.CTkButton(self, text="Add Item", command=self.add_item)
        self.add_item_button.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

    def create_fields(self):
        collection_name = self.collection_dropdown.get()
        if not collection_name:
            return
        fields = self.settings.mongo_connection.list_field_names(collection_name)
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        try:
            for i, field in enumerate(fields):
                label = customtkinter.CTkLabel(self.fields_frame, text=field)
                label.grid(
                    row=i,
                    column=0,
                    sticky="w",
                    padx=10,
                    pady=5,
                )
                entry = customtkinter.CTkEntry(self.fields_frame)
                entry.grid(row=i, column=1, sticky="w", padx=10, pady=5)
                entry.configure(placeholder_text=field)
        except TypeError:
            pass

    def refresh_fields(self, event=None):
        self.create_fields()

    def preview_item(self):
        """
        Preview the item to be added to the collection based on the fields and values entered by the user
        :return: None
        """
        item = {}
        self.item_to_add = {}
        for widget in self.fields_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkEntry):
                item[widget.cget("placeholder_text")] = widget.get()
        self.preview_text.delete("1.0", "end")
        # Insert a cleanly-formatted constructed string with a field and value pair on each line
        for field, value in item.items():
            if value == "":
                pass
            else:
                self.preview_text.insert("end", f"{field}: {value}\n")
                self.item_to_add[field] = value
        return

    def add_item(self):
        """
        Add the item to the collection
        :return: None
        """
        # Todo: Long-term, add a toggle to allow the user to specify the input as a text box that
        #  can be parsed as a series of key: value pairs separated by newlines
        collection_name = self.collection_dropdown.get()
        if not collection_name:
            return
        try:
            self.settings.mongo_connection.add_item(collection_name, self.item_to_add)
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(title="Error", message=f"Error adding item: {e}")
            root.destroy()
        self.preview_text.delete("1.0", "end")
        self.create_fields()
        logging.info(f"ITEM ADDED TO COLLECTION: {collection_name}")
        logging.info(f"ITEM: {self.item_to_add}")
        return


class AddBulkFrame(customtkinter.CTkFrame):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)
        self.settings = settings
        self.file_path = None
        self.file_data = None

        # Add a button that will open a file dialog to select the Excel file to upload
        self.upload_button = customtkinter.CTkButton(self, text="Select Excel File", command=self.select_file)
        self.upload_button.pack(side="top", padx=10, pady=10)
        self.file_path_label = customtkinter.CTkLabel(self, text="No file selected")
        self.file_path_label.pack(side="top", padx=10, pady=10)

        # Add a label to display the count of rows in each of the read-in DataFrames
        self.row_count_label = customtkinter.CTkLabel(self, text="Rows in each sheet:")
        self.row_count_label.pack(side="top", padx=10, pady=10)

        # Add a button to upload the data from the Excel file to the database
        self.upload_data_button = customtkinter.CTkButton(self, text="Upload Data", command=self.upload_data)
        self.upload_data_button.pack(side="top", padx=10, pady=10)

    def select_file(self):
        """
        Open a file dialog to select an Excel file to upload
        :return: None
        """
        try:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="Select an Excel file to upload",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialdir=Path(__file__).parent,
            )
            root.destroy()
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(title="Error", message=f"Error selecting file: {e}")
            root.destroy()
            return
        if file_path:
            self.file_path = file_path
            self.file_path_label.configure(text=file_path)
            # Open the Excel file and read each sheet into a dictionary of DataFrames using Pandas
            try:
                self.file_data = pd.read_excel(self.file_path, sheet_name=None)
            except Exception as e:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(title="Error", message=f"Error reading file: {e}")
                root.destroy()
                return
            # Display the number of rows in each sheet in the Excel file
            row_counts = {}
            for sheet_name, df in self.file_data.items():
                row_counts[sheet_name] = len(df)
            self.row_count_label.configure(text="\n".join([f"{k}: {v}" for k, v in row_counts.items()]))

    def upload_data(self):
        self.settings.mongo_connection.add_bulk_data(self.file_data)

        # Copy the file to a local archive location with a timestamp in the filename
        archive_path = Path(__file__).parent / "archive"
        archive_path.mkdir(exist_ok=True)
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = archive_path / f"{Path(self.file_path).stem}_{timestamp}.xlsx"
            archive_file = archive_file.resolve()
            shutil.copy(self.file_path, archive_file)
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(title="Error", message=f"Error archiving file: {e}")
            root.destroy()
            return
        logging.info(f"FILE UPLOADED: {self.file_path}")
        logging.info(f"FILE ARCHIVED: {archive_file}")
        return


class MainTabView(customtkinter.CTkTabview):
    def __init__(self, master, settings, **kwargs):
        super().__init__(master, **kwargs)
        self.add("    Welcome    ")
        self.add("    Settings    ")
        self.add("    New Collection    ")
        self.add("    Add One    ")
        self.add("    Add Bulk    ")
        self.add("    Download    ")
        self.add("    Search    ")
        self.add("    Delete    ")

        self.welcome_frame = WelcomeFrame(master=self.tab("    Welcome    "), settings=settings)
        self.welcome_frame.pack(anchor="w", expand=True, fill="both")
        self.settings_frame = SettingsFrame(master=self.tab("    Settings    "), settings=settings)
        self.settings_frame.pack(anchor="w", expand=True, fill="both")
        self.settings_frame = NewCollectionFrame(master=self.tab("    New Collection    "), settings=settings)
        self.settings_frame.pack(anchor="w", expand=True, fill="both")
        self.add_one_frame = AddOneFrame(master=self.tab("    Add One    "), settings=settings)
        self.add_one_frame.pack(anchor="w", expand=True, fill="both")
        self.add_bulk_frame = AddBulkFrame(master=self.tab("    Add Bulk    "), settings=settings)
        self.add_bulk_frame.pack(anchor="w", expand=True, fill="both")


class App(customtkinter.CTk):
    def __init__(self, settings):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        self.main_tab_view = MainTabView(self, settings=settings)
        self.main_tab_view.pack(anchor="e", expand=True, fill="both")


if __name__ == "__main__":
    setup_logging()
    logging.info("Application starting")
    main_settings = load_settings()
    app = App(settings=main_settings)
    app.mainloop()
    logging.info("Exiting application")
