from pymongo import MongoClient
from pymongo.errors import CollectionInvalid


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

    def list_field_names(self, collection_name: str) -> list:
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
