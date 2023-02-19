#!/usr/bin/env python3
"""Defines a function that  provides some stats
   about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_stats_check():
    """provides some stats about Nginx logs stored in MongoDB:"""
    client = MongoClient()
    collection = client.logs.nginx

    doc_count = collection.count_documents({})
    print('{} logs'.format(doc_count))

    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods_list:
        method_count = collection.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, method_count))
    status_count = collection.count_documents({
        "method": "GET", "path": "/status"
    })
    print('{} status check'.format(status_count))


if __name__ == "__main__":
    nginx_stats_check()
