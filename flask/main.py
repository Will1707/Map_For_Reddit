# coding=utf-8
import json
import time
# import pytz
import requests
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
    user_geoJSON = {"type": "FeatureCollection", "features": [{"type": "Feature", "id": "2pexpp", "geometry": {"type": "Point", "coordinates": [-118.1, 36.61]}, "properties": {"title": "I just spent 5 days in the Alabama Hills, CA. Finally last night, the clouds cleared enough for me to capture this moment. [OC] [7360 x 4907]", "image_link": "https://imgur.com/YY3bLP7m.jpg", "username": "OurEarthInFocus", "date": 1418688951, "score": 6701, "comments": 787}}, {"type": "Feature", "id": "2n8ut4", "geometry": {"type": "Point", "coordinates": [13.8636111, 68.4711111]}, "properties": {"title": "It's the end of November, so I feel comfortable calling this my favorite photo of 2014. It's from a mid-February night in Norway's Lofoten Islands [OC][2048x1367]", "image_link": "https://i.imgur.com/9lDdLYR.jpg", "username": "elmofoto", "date": 1416815221, "score": 5991, "comments": 491}}, {"type": "Feature", "id": "2h2yzx", "geometry": {"type": "Point", "coordinates": [-8.6730275, 37.1027881]}, "properties": {"title": "I stumbled upon this beautiful abyss while hiking near Lagos, Portugal [2448 x 3264]", "image_link": "https://i.imgur.com/fYYulaIm.jpg", "username": "RTWin80weeks", "date": 1411350017, "score": 5461, "comments": 803}}, {"type": "Feature", "id": "2dhgn4", "geometry": {"type": "Point", "coordinates": [-18.1718158, 63.771279]}, "properties": {"title": "\"If you drive up this dirt road for 5 minutes, You'll reach a small Canyon. It's really quite breathtaking.\" (Fja\u00f0r\u00e1rglj\u00fafur, Iceland) [OC] [2048x1058]", "image_link": "https://i.imgur.com/MJqwwTn.jpg", "username": "xeno_sapien", "date": 1407974654, "score": 5081, "comments": 356}}, {"type": "Feature", "id": "2k2cb0", "geometry": {"type": "Point", "coordinates": [35.4079087, 29.534667]}, "properties": {"title": "Bedouin nomads crossing the Wadi Rum desert, Jordan [6016 x 4000] [OC]", "image_link": "https://i.imgur.com/fIdt7Frm.jpg", "username": "ButtLickinBadBoy", "date": 1414039467, "score": 4979, "comments": 458}}, {"type": "Feature", "id": "2ijq1h", "geometry": {"type": "Point", "coordinates": [-149.8163645, 60.04377640000001]}, "properties": {"title": "Kenai Fjords National Park in Alaska, by Michael McRuiz [2400x1594]", "image_link": "https://i.imgur.com/jypHpBvm.jpg", "username": "jaycrew", "date": 1412683021, "score": 4882, "comments": 237}}, {"type": "Feature", "id": "2lxitm", "geometry": {"type": "Point", "coordinates": [-89.4012302, 43.0730517]}, "properties": {"title": "A beautiful little spot on the lake in Madison, WI [OC][4308x2871]", "image_link": "https://i.imgur.com/KjP1n1M.jpg", "username": "half_caulked_jack", "date": 1415677433, "score": 4829, "comments": 672}}, {"type": "Feature", "id": "2eaqp1", "geometry": {"type": "Point", "coordinates": [-121.1133076, 48.7121596]}, "properties": {"title": "I visited my sister in Washington. She told me the lakes were beautiful but I wasn't expecting this. Diablo Lake, WA. [3648x2736][OC]", "image_link": "https://i.imgur.com/2UPTd9c.jpg", "username": "[deleted]", "date": 1408734635, "score": 4599, "comments": 542}}]}
    return render_template('home.html', geojson=json.dumps(user_geoJSON))

@app.route('/api/v0.1/reddit_id', methods=['GET'])
def api_id():
    # client = MongoClient('mongodb://will1:iJzubpOyHD1357Aq@mapforredditdb-shard-00-00-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-01-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-02-j48a5.gcp.mongodb.net:27017/test?ssl=true&replicaSet=mapforredditDB-shard-0&authSource=admin&retryWrites=true')
    client = MongoClient('localhost', 27017)
    db = client['earthporn']
    submissions = db.location
    user_db = client['location']
    args = request.args.to_dict()
    find = 'user_posts.' + args['id'] + '.id'
    found = submissions.find({find: args['id']})
    urls = {}
    for post in found:
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
        insert = {
            'user': user,
            'time': time.time(),
            'requested_id': args['id']
        }
        # user_db.user.insert_one(insert)
        user_country = user_db.country.find_one({'country_code': user['country_code'].lower()})
        user_currency_code = user_country['currency']['iso_code']
        loc_currency_code  = results['location_info']['currency']['iso_code']
        currency = user_db.currency.find_one()
        currency = {
        "conversion": round(currency['currency'][user_currency_code][loc_currency_code], 2),
        "from_html": user_country['currency']['html'],
        "from_iso": user_country['currency']['iso_code'],
        "from_symbol": user_country['currency']['symbol'],
        "to_html": results['location_info']['currency']['html'],
        "to_iso": results['location_info']['currency']['iso_code'],
        "to_symbol": results['location_info']['currency']['symbol'],
        "flag": user_country['flag']
        }
        date_time = datetime.now(time.time()) #pytz.timezone(results['location_info']['timezone']['name']))
        local_time = {
        "time": date_time.strftime('%H:%M'),
        "timezone": date_time.strftime('%Z')
        }
        s = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={results['loc'][0]}&lon={results['loc'][1]}&APPID=7986ad57675127ce999defef1beaa4dd")
        weather = json.loads(s.content)
        results['weather'] = weather
        results['local_time'] = local_time
        results['currency'] = currency
    except:
        pass
    client.close()
    return jsonify(results)

if __name__ == '__main__':
       app.debug = True
       app.run()
