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
countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'B&H', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Bermuda', 'Bhutan', 'Bolivia', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Chile', 'Colombia', 'Comoros', 'Congo-Brazzaville', 'Corn Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'D.R.', 'DR Congo', 'Denmark', 'Djibouti', 'Dominica', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Fiji', 'Finland', 'France', 'France, Polynésie française (eaux territoriales)', 'France, Terres australes et antarctiques françaises, Îles Kerguelen (eaux territoriales)', 'France, Terres australes et antarctiques françaises, Îles Saint-Paul et Nouvelle-Amsterdam - Île Saint-Paul (eaux territoriales)', 'France, Wallis-et-Futuna (eaux territoriales)', "Francis Joseph's Land", 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Metropolitan France', 'Mexico', 'Moldova', 'Mongolia', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'New Zealand', 'Nicaragua', 'Nigeria', 'North Korea', 'Norway', 'Nouvelle-Calédonie, France, Îles Loyauté (eaux territoriales)', 'Oman', 'PRC', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'ROC', 'RSA', 'Romania', 'Russia', 'Rwanda', 'SBA', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Korea', 'South Sudan', 'Spain', 'Spain (territorial waters)', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'São Tomé and Príncipe', 'Tajikistan', 'Tanzania', 'Territorial waters of Bornholm', 'Territorial waters of Greece - Gavdos and Gavdopoula', 'Territorial waters of Italy - Ustica', 'Thailand', 'The Bahamas', 'The Netherlands', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'USA', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States of America', 'United States of America (American Samoa)', 'United States of America (CNMI)', 'United States of America (Dry Tortugas territorial waters)', 'United States of America (Guam)', "United States of America (Island of Hawai'i territorial waters)", "United States of America (Kaua'i, Ni'ihau, Ka'ula)", "United States of America (Middle Hawai'ian Islands territorial waters)", 'United States of America (USVI Saint Croix)', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'eSwatini']


user_form = {
        'id': user_dict['id'],
        'score_upper': 150000,
        'score_lower': 0,
        'comments_upper': 5000,
        'comments_lower': 0,
        'date_upper': 9999999999999,
        'date_lower': 0,
        'results': 5000,
        'num_country': 50,
        'countries': countries
        }
found = submission.find({"geoJSON.properties.comments": {"$gt": user_form['comments_lower'], "$lt": user_form['comments_upper']},
                        "geoJSON.properties.score": {"$gt": user_form['score_lower'], "$lt": user_form['score_upper']},
                        "geoJSON.properties.date": {"$gt": user_form['date_lower'], "$lt": user_form['date_upper']},
                        "country": {"$in": user_form['countries']}}).sort("score", pymongo.DESCENDING)

result = []
remainder = []
for loc in found:
    if loc['country_rank'] <= user_form['num_country'] and loc['country_rank'] is not None:
        result.append(loc['geoJSON'])
    else:
        remainder.append(loc['geoJSON'])

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
