import pandas as pd
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from pymongo.results import DeleteResult


class MongoConnection:
    def __init__(self, settings: dict) -> None:
        """
        Initialize the MongoDB connection
        :param settings: dictionary of MongoDB connection settings
        """
        try:
            self.settings = settings
            self.mongo_client = MongoClient(settings["mongo_connection_string"])
            self.db = self.mongo_client[settings["mongo_database"]]
        except Exception as e:
            raise e

        return

    def summarize_collection_counts(self) -> dict:
        """
        Summarize the number of documents in each collection
        :return: dictionary of collection names and their document counts
        """
        collection_counts = {}
        for collection in self.db.list_collection_names():
            collection_counts[collection] = self.db[collection].count_documents({})
        return collection_counts

    def add_collection(self, collection_name):
        """
        Add a collection to the active database
        :return: None
        """
        try:
            self.db.create_collection(collection_name)
        except CollectionInvalid as e:
            raise e

        return

    def list_collection_names(self) -> list:
        """
        List the names of all collections in the active database
        :return: list of collection names
        """
        return self.db.list_collection_names()

    def list_field_names(self, collection_name: str) -> list | None:
        """
        List the field names in a given collection by checking all documents in the collection
        :param collection_name: string name of the collection
        :return: list of field names
        """
        try:
            field_names = set()
            for doc in self.db[collection_name].find():
                field_names.update(doc.keys())
            field_names.remove("_id")
            return list(field_names)
        except KeyError:
            pass

    def list_field_names_with_id(self, collection_name: str) -> list | None:
        """
        List the field names in a given collection by checking all documents in the collection
        :param collection_name: string name of the collection
        :return: list of field names
        """
        try:
            field_names = set()
            for doc in self.db[collection_name].find():
                field_names.update(doc.keys())
            return list(field_names)
        except KeyError:
            pass

    def add_item(self, collection_name: str, item: dict) -> None:
        """
        Add an item to a collection
        :param collection_name: string name of the collection
        :param item: dictionary of the item to be added
        :return: None
        """
        self.db[collection_name].insert_one(item)
        return

    def add_bulk_data(self, data: dict[str, pd.DataFrame]):
        """
        Add bulk data to the MongoDB database
        :param data: dictionary of DataFrames to be added
        :return: None
        """
        for collection_name, df in data.items():
            if not df.empty:
                # Check if the collection exists
                if collection_name not in self.db.list_collection_names():
                    # Create the collection if it does not exist
                    self.db.create_collection(collection_name)

                # Convert DataFrame to list of dictionaries
                data = df.to_dict(orient="records")

                # Insert data into the collection
                self.db[collection_name].insert_many(data)
        return

    def get_collection_as_df(self, collection_name) -> pd.DataFrame:
        """
        Get a collection as a DataFrame
        :param collection_name: string name of the collection
        :return: DataFrame of the collection
        """
        return pd.DataFrame(self.db[collection_name].find())

    def generate_fields_by_collection(self) -> dict:
        """
        Generate a dictionary of fields for each available collection within the database
        :return: dictionary of fields by collection
        """
        fields = {}
        for collection in self.db.list_collection_names():
            fields[collection] = self.list_field_names_with_id(collection)
        return fields

    def search(self, collection_name: str, field: str, value: str) -> list:
        """
        Search a collection for a specific value as a regex cast to lower case
        :param collection_name: string name of the collection
        :param field: string name of the field to search
        :param value: string value to search for
        :return: DataFrame of the search results
        """
        if field == "_id":
            try:
                search_results = self.db[collection_name].find({"_id": ObjectId(value)})
            except Exception:
                return []  # Return an empty list if the ObjectId conversion fails
        else:
            item_query = {f"{field}": {"$regex": value, "$options": "i"}}
            search_results = [document for document in self.db[collection_name].find(item_query)]
        return list(search_results)

    def delete_item(self, collection_name: str, item_id: str) -> DeleteResult:
        """
        Delete an item from a collection
        :param collection_name: string name of the collection
        :param item_id: string ID of the item to be deleted
        :return: None
        """
        result = self.db[collection_name].delete_one({"_id": ObjectId(item_id)})
        return result
