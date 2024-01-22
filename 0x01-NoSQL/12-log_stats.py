#!/usr/bin/env python3
'''
Function that provides some stats about Nginx logs stored in MongoDB
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''prints number of documents in collection
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, count))
    status_checks_num = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_num))


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()