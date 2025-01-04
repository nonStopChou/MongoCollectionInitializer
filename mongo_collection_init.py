
from pymongo.mongo_client import MongoClient
import os
import json


USER = os.getenv("MONGO_RESUME_USER")
PASSWORD = os.getenv("MONGO_RESUME_PASS")
CLUSTER_ADDRESS = "resume.xg22b.mongodb.net"
MONGO_URL = f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER_ADDRESS}/?retryWrites=true&w=majority&appName=Resume"

SPEC_PATH = "./initial_spec"
try:

    db_relation_map = {}

    database_directory = os.listdir(SPEC_PATH)
    print("Directories under initial_spec:")
    for database in database_directory:
        db_relation_map[database] = {}

        collection_path = os.path.join(SPEC_PATH, database)
        if os.path.isdir(collection_path):
            collection_directory = os.listdir(collection_path)
            
            for collection in collection_directory:
                        
                validator_path = os.path.join(collection_path, collection)
                if os.path.isdir(validator_path):
                    validator_directory = os.listdir(validator_path)
                    
                    for validator in validator_directory:
                        if validator.endswith('.json'):
                            print(f"Validator file found for database[{database}] and collection[{collection}]: {validator}")

                            with open(os.path.join(validator_path, validator), 'r') as file:
                                json_data = json.load(file)
                                db_relation_map[database][collection] = json_data
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
            try:
                if collection in db.list_collection_names():
                    print(f"Start update collection with validator.")
                    # udpate validator
                    db.command({
                        'collMod': collection,
                        'validator': db_relation_map[database][collection]
                    })
                    print(f"Update Collection[{collection}] with validator successfully.")
                else:
                    print(f"Start create collection with validator.")
                    db.create_collection(
                        collection,
                        validator = db_relation_map[database][collection]
                    )
                    print(f"Create Collection[{collection}] with validator successfully.")
                    # create validator
            except Exception as e:
                print(f"Action perform fail ...")
                print(f"Database[{database}], Collection[{collection}, Validator[{db_relation_map[database][collection]}]")

except Exception as e:
    print(e)