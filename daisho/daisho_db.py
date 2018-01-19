#!/usr/bin/env python3

import pymongo
import sys

HOST = "localhost"
PORT = "27017"


def mongo_conn():
    """
    Connect to the local MongoDB
    Create the local db `daisho`, if it doesn't exist
    """
    print("\nConnecting to MongoDB on {}.".format(PORT))
    try:
        connect = pymongo.MongoClient(HOST + ":" + PORT)
        # Connect to the `daisho` db (will create if non-existing)
        daisho_db = connect.daisho
        if connect.database_names():
            print("Connection successful.")

    except pymongo.errors.ConnectionFailure as err:
        print("Failed to connect to {}".format(err))
        print("Daisho requires an active MongoDB instance on localhost")
        print("Check if the `mongod` service is running\n")
        sys.exit()
    return daisho_db


def add_data(data):
    """
    Add entries in the db
    """
    mongo_conn.daisho_db.subject.insert(data)
    # mongo_conn.daisho_db.table.insert(data)


def get_data(table, query):
    """
    Query the db and return data
    """
    return mongo_conn.daisho_db.table.find_one(query)


if __name__ == "__main__":
    mongo_conn()
