# api is always up, so it mongo
# listen for a post
# once a post, then grab info from mongo
# get info then translate into language of app
# return

import pymongo

client = pymongo.MongoClient("mongodb://elia:squiggle@db-hacksc-shard-00-00-thwez.gcp.mongodb.net:27017,db-hacksc-shard-00-01-thwez.gcp.mongodb.net:27017,db-hacksc-shard-00-02-thwez.gcp.mongodb.net:27017/test?ssl=true&replicaSet=db-hacksc-shard-0&authSource=admin&retryWrites=true&w=majority")

plantsWithDx = [
    {
        "disease_name": "healthy",
        "treatments": ["No disease, good job!"]
    },
    {
        "disease_name": "Apple scab",
        "treatments": ["Weekly Liquid Copper Soap"]
    },
    {
        "disease_name": "Black rot",
        "treatments": ["Weekly Sulfur Powder"]
    },
    {
        "disease_name": "Cedar apple rust",
        "treatments": ["4x Month Copper Solution"]
    }
]

with client:
    db = client.plants
    db.treatments.insert_many(plantsWithDx)

    tmp = db.treatments.find()
    for t in tmp:
        print(t)
