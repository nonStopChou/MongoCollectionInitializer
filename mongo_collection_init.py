
from pymongo.mongo_client import MongoClient
from pymongo import ASCENDING, DESCENDING
import os
import json


USER = os.getenv("MONGO_RESUME_USER")
PASSWORD = os.getenv("MONGO_RESUME_PASS")
CLUSTER_ADDRESS = "resume.xg22b.mongodb.net"
MONGO_URL = f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER_ADDRESS}/?retryWrites=true&w=majority&appName=Resume"

SPEC_PATH = "./initial_spec"
FUNCTION_LIST = ["validator", "index"]

try:

    db_relation_map = {}

    database_directory = os.listdir(SPEC_PATH)
    print("Directories under initial_spec:")
    for database in database_directory:

        collection_path = os.path.join(SPEC_PATH, database)
        if os.path.isdir(collection_path):

            db_relation_map[database] = {}
            collection_directory = os.listdir(collection_path)
            
            for collection in collection_directory:
                
                json_path = os.path.join(collection_path, collection)
                if os.path.isdir(json_path):

                    json_directory = os.listdir(json_path)
                    db_relation_map[database][collection] = {}

                    for json_file in json_directory:
                        function_name = os.path.splitext(json_file)[0]
                        print(f"JSON_FILE : {json_file}, Function Name : {function_name}")

                        if function_name in FUNCTION_LIST:
                            print(f"JSON file found for database[{database}] and collection[{collection}]: {json_file}")

                            with open(os.path.join(json_path, json_file), 'r') as file:
                                json_data = json.load(file)
                                db_relation_map[database][collection][function_name] = json_data
                                file.close()


except Exception as e:
    print(f"Error listing directories: {e}")


# Send a ping to confirm a successful connection
try:
    
    # Create a new client and connect to the server
    print(f"UserName : {USER}")
    client = MongoClient(MONGO_URL)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    
    for database in db_relation_map:
        
        db = client[database]

        collections = db_relation_map[database]

        for collection in collections:

            for function_name in FUNCTION_LIST:

                if function_name == "validator":
                    try:
                        validator = db_relation_map[database][collection][function_name]
                        if collection in db.list_collection_names():
                            print(f"Start update collection with validator.")
                            # udpate validator
                            db.command({
                                'collMod': collection,
                                'validator': validator
                            })
                            print(f"Update Collection[{collection}] with validator successfully.")
                        else:
                            print(f"Start create collection with validator.")
                            db.create_collection(
                                collection,
                                validator = validator
                            )
                            print(f"Create Collection[{collection}] with validator successfully.")
                            # create validator
                    except Exception as e:
                        print(f"Action perform fail ...")
                        print(f"Database[{database}], Collection[{collection}, Validator[{validator}]")
                
                if function_name == "index":

                    if collection not in db.list_collection_names():
                        db.create_collection(
                            collection
                        )
                    db_collection = db[collection]
                    db_collection.drop_indexes() 

                    try:
                        
                        indexes = db_relation_map[database][collection][function_name]['indexes']

                        for single_index in indexes:  
                            
                            print(f"Start create collection with index.")
                            index_keys = [(field, ASCENDING if direction == "ASCENDING" else DESCENDING) for entry in single_index['keys'] for field, direction in entry.items()]
                            db_collection.create_index(index_keys, **single_index['options'])
                            print(f"Update Collection[{collection}] with index successfully.")

                    except Exception as e:
                        print(f"Action perform fail ...")
                        print(f"Database[{database}], Collection[{collection}, Indexes[{indexes}]")
                

except Exception as e:
    print(e)