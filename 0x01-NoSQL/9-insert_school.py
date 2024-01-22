#!/usr/bin/env python3
'''
Function that inserts a new document in a collection based on kwargs
'''


def insert_school(mongo_collection, **kwargs):
    '''
    Returns inserted new document in a collection
    '''
    results = mongo_collection.insert_one(kwargs)
    return results.inserted_id
