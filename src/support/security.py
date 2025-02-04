import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings

from . import mongo_conn as mc


class Settings(BaseSettings):
    mongo_connection: Optional[mc.MongoConnection] = None
    mongo_username: str
    mongo_password: SecretStr
    mongo_cluster: str
    mongo_database: str
    mongo_uri: str

    collections_cache: Optional[list] = None
    fields_cache: Optional[dict] = None

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

    def update_setting(self, key: str, value: Any) -> None:
        setattr(self, key, value)


def load_settings() -> Settings:
    # Load the settings from the environment
    current_directory = Path(os.path.dirname(os.path.abspath(__file__))).parent
    print(current_directory)

    settings_file = os.path.join(current_directory, "settings.conf")

    # Check if the settings.conf file exists.  If it does not, notify the user in a pop-up window.
    if not os.path.exists(settings_file):
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
        return_settings.mongo_connection = mc.MongoConnection(return_settings.model_dump())
    except Exception:
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

    # Update the settings with the collection and fields info
    return_settings.collections_cache = return_settings.mongo_connection.list_collection_names()
    return_settings.fields_cache = return_settings.mongo_fields_by_collection

    return return_settings


if __name__ == "__main__":
    testing_settings = load_settings()
    print(testing_settings.mongo_connection_string)
