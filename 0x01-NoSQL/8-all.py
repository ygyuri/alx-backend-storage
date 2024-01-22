#!/usr/bin/env python3
'''
Function that lists all documents in a collection
'''


def list_all(mongo_collection):
    '''returns list of all documents
    '''
    return [doc for doc in mongo_collection.find()]
