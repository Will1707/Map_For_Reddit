import pymongo
import json
from geojson import FeatureCollection
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://will1:iJzubpOyHD1357Aq@mapforredditdb-shard-00-00-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-01-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-02-j48a5.gcp.mongodb.net:27017/test?ssl=true&replicaSet=mapforredditDB-shard-0&authSource=admin&retryWrites=true')
# client = MongoClient('localhost', 27017)
submission = client['earthporn'].post
data = client['geojson'].featurecollection
user_dict = {}

def user_data(user_dict):
    feature_collection_list = []
    split_score = user_dict['score'].split(',')
    user_dict['score_upper'] = split_score[1]
    user_dict['score_lower'] = split_score[0]
    split_comments = user_dict['comments'].split(',')
    user_dict['comments_upper'] = split_comments[1]
    user_dict['comments_lower'] = split_comments[0]
    split_comments = user_dict['date'].split(' - ')
    user_dict['date_upper'] = split_comments[1]
    user_dict['date_lower'] = split_comments[0]
    date_upper_utc = int((datetime.strptime(user_dict['date_upper'], "%m/%d/%Y") - datetime(1970, 1, 1)).total_seconds())
    date_lower_utc = int((datetime.strptime(user_dict['date_lower'], "%m/%d/%Y") - datetime(1970, 1, 1)).total_seconds())
    date_upper = "".join(user_dict['date_upper'].split("/"))
    date_lower = "".join(user_dict['date_lower'].split("/"))
    user_dict['date_upper'] = date_upper_utc
    user_dict['date_lower'] = date_lower_utc
    user_dict['id'] = ( 'S' + user_dict['score_upper'] + 's' + user_dict['score_lower'] +
                        'C' + user_dict['comments_upper'] + 'c' + user_dict['comments_lower'] +
                        'D' + date_upper + 'd' + date_lower + 'J' + user_dict['countries_no'] +
                        'G' + user_dict['cluster'] + 'R' + user_dict['results'] + 'N' + user_dict['num_country'])

    featurecollection = data.find({"id":user_dict['id']})
    if featurecollection.count(with_limit_and_skip=True) == 0:
        user_form = {
                'id': user_dict['id'],
                'score_upper': int(user_dict['score_upper']),
                'score_lower': int(user_dict['score_lower']),
                'comments_upper': int(user_dict['comments_upper']),
                'comments_lower': int(user_dict['comments_lower']),
                'date_upper': user_dict['date_upper'],
                'date_lower': user_dict['date_lower'],
                'cluster': int(user_dict['cluster']),
                'results': int(user_dict['results']),
                'num_country': int(user_dict['num_country']),
                'countries': user_dict['countries']
                }
        if user_form['cluster'] == 0:
            found = submission.find({"geoJSON.properties.comments": {"$gt": user_form['comments_lower'], "$lt": user_form['comments_upper']},
                                    "geoJSON.properties.score": {"$gt": user_form['score_lower'], "$lt": user_form['score_upper']},
                                    "geoJSON.properties.date": {"$gt": user_form['date_lower'], "$lt": user_form['date_upper']},
                                    "country": {"$in": user_form['countries']}}).sort("score", pymongo.DESCENDING)
        else:
            cluster = 'cluster.level_' + str(user_form['cluster'])
            found = submission.find({"geoJSON.properties.comments": {"$gt": user_form['comments_lower'], "$lt": user_form['comments_upper']},
                                    "geoJSON.properties.score": {"$gt": user_form['score_lower'], "$lt": user_form['score_upper']},
                                    "geoJSON.properties.date": {"$gt": user_form['date_lower'], "$lt": user_form['date_upper']},
                                    "country": {"$in": user_form['countries']}, cluster: True}).sort("score", pymongo.DESCENDING)

        print(found.count(with_limit_and_skip=True))
        result = []
        remainder = []
        for loc in found:
            if loc['country_rank'] <= user_form['num_country'] and loc['country_rank'] is not None:
                result.append(loc['geoJSON'])
            else:
                remainder.append(loc['geoJSON'])

        # print(user_form['results'])
        # print("result:" + str(len(result)))
        # print("remainder:" + str(len(remainder)))

        remaining = user_form['results'] - len(result)
        if remaining > 0:
            result = result + remainder[:remaining]
        elif remaining < 0:
            result = result[:remaining]

        locations = []
        for geoJSON in result:
            if geoJSON['geometry']['coordinates'] not in locations:
                locations.append(geoJSON['geometry']['coordinates'])
                feature_collection_list.append(geoJSON)

        user_form['feature_collection'] = FeatureCollection(feature_collection_list)
        data.insert_one(user_form)
        return user_form['feature_collection']

    else:
        # for post in found:
        #     user_geoJSON = post['feature_collection']
        return 2
