# MongoDB Collection Validator Initialization

This project contains a Python script that initializes MongoDB collections with validators based on JSON configuration files stored in a specified directory structure. The script will create collections in the corresponding MongoDB database with the defined validation rules.

## Folder Structure
```
init_spec
│ 
└─── {dataase_name}
│   │
│   └─── {collection_name}
│       │
│       │   validator.json
│       │   index.json
initialize_collection.py
Readme.md
```

- `{database_name}`: The name of the MongoDB database.
- `{collection_name}`: The name of the collection within the database.
- `validator.json`: The JSON file containing the MongoDB collection validator.
- `index.json`: The JSON file containing the MongoDB collection index.

## Features

- **Dynamic Validator & Index Loading**: The script loads the validator configuration from the `validator.json`, `index.json` file for each collection.
- **Automatic Collection Creation**: If the collection doesn't already exist, it will be created along with the validator.
- **Validator & Index Update**: If the collection already exists, the script will update the validator & index without modifying the existing collection.

## Prerequisites

- Python 3.x
- `pymongo` package installed. You can install it with:

```bash
pip install pymongo
```

## Script Description

The script will traverse the init_spec directory structure.
For each validator.json file found in a collection folder, it will read the validator and attempt to create the collection with the validator in the corresponding database.
If the collection already exists, the validator will be updated without recreating the collection.

For each index.json file found in a collection folder, it will read the index and attempt to create the collection with the index in the corresponding database.
If the collection already exists, the index will be updated without recreating the collection.

## Notes

Ensure that the MongoDB URI is correctly set in the uri variable, replacing ```<username>```, ```<password>```, and ```<cluster-address>``` with your actual MongoDB credentials and cluster details.
The script supports a folder structure where each database is represented by a subfolder, and each collection inside the database folder has a validator.json file.
