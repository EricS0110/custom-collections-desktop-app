import os
import sys
from typing import Optional

from dotenv import load_dotenv
from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings

from src.mongo import MongoConnection


class Settings(BaseSettings):
    mongo_connection: Optional[MongoConnection] = None
    mongo_username: str
    mongo_password: SecretStr
    mongo_cluster: str
    mongo_database: str
    mongo_uri: str

    archive_directory: Optional[str] = None
    download_directory: Optional[str] = None

    @computed_field
    @property
    def mongo_connection_string(self) -> str:
        return (
            f"mongodb+srv://{self.mongo_username}:{self.mongo_password.get_secret_value()}@{self.mongo_cluster}"
            f".{self.mongo_uri}.mongodb.net"
        )

    @property
    def mongo_fields_by_collection(self) -> dict:
        """
        Get a dictionary of fields for each available collection within mongo_connection
        :return:
        """
        fields = {}
        for collection in self.mongo_connection.list_collection_names():
            fields[collection] = self.mongo_connection.list_field_names(collection)
        return fields


# noinspection PyArgumentList
def load_settings() -> Settings:
    # Load the settings from the environment
    # Determines the current directory based on execution method (.py or .exe)
    if getattr(sys, "frozen", False):
        current_directory = os.path.dirname(sys.executable)  # For .exe
    else:
        current_directory = os.path.dirname(os.path.abspath(__file__))  # For .py

    settings_file = os.path.join(current_directory, "settings.conf")

    # Check if the settings.conf file exists.  If it does not, notify the user in a pop-up window.
    if not os.path.exists(settings_file):
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            title="Error",
            message=(
                "The settings.conf file is missing.  Please create the settings.conf file in the same"
                " directory as the application."
            ),
        )
        root.destroy()
        sys.exit()

    load_dotenv(settings_file)

    return_settings = Settings()

    # Attempt to connect to the MongoDB instance specified in the connection string
    try:
        return_settings.mongo_connection = MongoConnection(Settings().model_dump())

    except Exception:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            title="Error",
            message=(
                "An error occurred while trying to connect to the MongoDB instance.  Please check the connection "
                "details in the settings.conf file and try again."
            ),
        )
        root.destroy()
        sys.exit()

    return return_settings


if __name__ == "__main__":
    testing_settings = load_settings()
    print(testing_settings.mongo_connection_string)
