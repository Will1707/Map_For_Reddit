# coding=utf-8
import json
import time
from datetime import datetime
from flask import Flask, request
from flask import render_template, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict
from user_data import user_data
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'B&H', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Bermuda', 'Bhutan', 'Bolivia', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Chile', 'Colombia', 'Comoros', 'Congo-Brazzaville', 'Corn Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'D.R.', 'DR Congo', 'Denmark', 'Djibouti', 'Dominica', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Fiji', 'Finland', 'France', 'France, Polynésie française (eaux territoriales)', 'France, Terres australes et antarctiques françaises, Îles Kerguelen (eaux territoriales)', 'France, Terres australes et antarctiques françaises, Îles Saint-Paul et Nouvelle-Amsterdam - Île Saint-Paul (eaux territoriales)', 'France, Wallis-et-Futuna (eaux territoriales)', "Francis Joseph's Land", 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Metropolitan France', 'Mexico', 'Moldova', 'Mongolia', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'New Zealand', 'Nicaragua', 'Nigeria', 'North Korea', 'Norway', 'Nouvelle-Calédonie, France, Îles Loyauté (eaux territoriales)', 'Oman', 'PRC', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'ROC', 'RSA', 'Romania', 'Russia', 'Rwanda', 'SBA', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Korea', 'South Sudan', 'Spain', 'Spain (territorial waters)', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'São Tomé and Príncipe', 'Tajikistan', 'Tanzania', 'Territorial waters of Bornholm', 'Territorial waters of Greece - Gavdos and Gavdopoula', 'Territorial waters of Italy - Ustica', 'Thailand', 'The Bahamas', 'The Netherlands', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'USA', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States of America', 'United States of America (American Samoa)', 'United States of America (CNMI)', 'United States of America (Dry Tortugas territorial waters)', 'United States of America (Guam)', "United States of America (Island of Hawai'i territorial waters)", "United States of America (Kaua'i, Ni'ihau, Ka'ula)", "United States of America (Middle Hawai'ian Islands territorial waters)", 'United States of America (USVI Saint Croix)', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'eSwatini']

    if request.method == 'POST':
        user_dict = {}
        report_dict = {}
        selected_countries = []
        countries_no = []
        user_countries = None
        imd = ImmutableMultiDict(request.form)
        imd_list = imd.lists()
        for i in imd_list:
            if 'reddit_countries' in i:
                    user_countries = i
        if user_countries is not None:
            for i in user_countries[1]:
                selected_countries.append(countries[int(i)])
                countries_no.append(i)
        else:
            selected_countries = countries
        user_dict['score'] = request.form['reddit_score']
        user_dict['comments'] = request.form['reddit_comments']
        user_dict['cluster'] = request.form['reddit_cluster']
        user_dict['results'] = request.form['reddit_results']
        user_dict['num_country'] = request.form['reddit_country']
        user_dict['date'] = request.form['daterange']
        user_dict['countries'] = selected_countries
        user_dict['countries_no'] = "".join(countries_no)
        user_geoJSON = user_data(user_dict)
        return render_template('home.html', geojson=json.dumps(user_geoJSON))
    client = MongoClient('mongodb://will1:iJzubpOyHD1357Aq@mapforredditdb-shard-00-00-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-01-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-02-j48a5.gcp.mongodb.net:27017/test?ssl=true&replicaSet=mapforredditDB-shard-0&authSource=admin&retryWrites=true')
    data = client['geojson'].featurecollection
    featurecollection = data.find_one({"id":'S155000s10C3500c0D01012017d01012012JG0R5000N100'})
    client.close()
    return render_template('home.html', geojson=json.dumps(featurecollection['feature_collection']))

@app.route('/api/v0.1/reddit_id', methods=['GET'])
def api_id():
    client = MongoClient('mongodb://will1:iJzubpOyHD1357Aq@mapforredditdb-shard-00-00-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-01-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-02-j48a5.gcp.mongodb.net:27017/test?ssl=true&replicaSet=mapforredditDB-shard-0&authSource=admin&retryWrites=true')
    # client = MongoClient('localhost', 27017)
    db = client['earthporn']
    submissions = db.location
    user_db = client['location']
    args = request.args.to_dict()
    find = 'user_posts.' + args['id'] + '.id'
    post = submissions.find_one({find: args['id']})
    results = {
        "extract": post['wiki_extract'],
        "title": post['wiki_title'],
        "reddit_title": post['user_posts'][args['id']]['title'],
        "reddit_image": post['user_posts'][args['id']]['url'],
        "reddit_score": post['user_posts'][args['id']]['score'],
        "reddit_user": post['user_posts'][args['id']]['author'],
        "reddit_comments": post['user_posts'][args['id']]['num_comments'],
        "id": args['id'],
        "other_posts": post['user_posts'][args['id']]['user_content'],
        "pie_chart": post['user_posts'][args['id']]['pie_chart'],
        "subreddit": post['subreddit'],
        "loc": post['loc'],
        "location_info": post['location_info']
    }
    try:
        user = json.loads(args['?ip'])
        results['user'] = user
        user_country = user_db.country.find_one({'country_code': user['country_code'].lower()})
        user_currency_code = user_country['currency']['iso_code']
        results['user_currency_code'] = user_currency_code
        loc_currency_code  = results['location_info']['currency']['iso_code']
        results['loc_currency_code'] = loc_currency_code
        currency_db = user_db.currency.find_one()
        currency = {
            "conversion": round(currency_db['currency'][user_currency_code][loc_currency_code], 2),
            "from_html": user_country['currency']['html'],
            "from_iso": user_country['currency']['iso_code'],
            "from_symbol": user_country['currency']['symbol'],
            "to_html": results['location_info']['currency']['html'],
            "to_iso": results['location_info']['currency']['iso_code'],
            "to_symbol": results['location_info']['currency']['symbol'],
            "flag": user_country['flag']
        }
        results['local_time'] =  time.strftime("%H:%M", time.gmtime(time.time()+results['location_info']['timezone']['offset_sec']))
        results['currency'] = currency
    except:
        pass
    client.close()
    return jsonify(results)

if __name__ == '__main__':
       app.debug = True
       app.run()
