import json
from flask import Flask, request
from flask import render_template, request, jsonify
from user_data import user_data
from pymongo import MongoClient

client = MongoClient('mongodb://will1:iJzubpOyHD1357Aq@mapforredditdb-shard-00-00-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-01-j48a5.gcp.mongodb.net:27017,mapforredditdb-shard-00-02-j48a5.gcp.mongodb.net:27017/test?ssl=true&replicaSet=mapforredditDB-shard-0&authSource=admin&retryWrites=true')
db = client['earthporn']
submissions = db.location

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        user_dict = {}
        report_dict = {}
        user_dict['score'] = request.form['reddit_score']
        user_dict['comments'] = request.form['reddit_comments']
        user_dict['cluster'] = request.form['reddit_cluster']
        user_dict['results'] = request.form['reddit_results']
        user_dict['num_country'] = request.form['reddit_country']
        user_dict['date'] = request.form['daterange']
        user_geoJSON = user_data(user_dict)
        return render_template('home.html', geojson=json.dumps(user_geoJSON))
    user_geoJSON = {"type": "FeatureCollection", "features": [{"type": "Feature", "id": "2pexpp", "geometry": {"type": "Point", "coordinates": [-118.1, 36.61]}, "properties": {"title": "I just spent 5 days in the Alabama Hills, CA. Finally last night, the clouds cleared enough for me to capture this moment. [OC] [7360 x 4907]", "image_link": "http://imgur.com/YY3bLP7m.jpg", "username": "OurEarthInFocus", "date": 1418688951, "score": 6701, "comments": 787}}, {"type": "Feature", "id": "2n8ut4", "geometry": {"type": "Point", "coordinates": [13.8636111, 68.4711111]}, "properties": {"title": "It's the end of November, so I feel comfortable calling this my favorite photo of 2014. It's from a mid-February night in Norway's Lofoten Islands [OC][2048x1367]", "image_link": "http://i.imgur.com/9lDdLYR.jpg", "username": "elmofoto", "date": 1416815221, "score": 5991, "comments": 491}}, {"type": "Feature", "id": "2h2yzx", "geometry": {"type": "Point", "coordinates": [-8.6730275, 37.1027881]}, "properties": {"title": "I stumbled upon this beautiful abyss while hiking near Lagos, Portugal [2448 x 3264]", "image_link": "http://i.imgur.com/fYYulaIm.jpg", "username": "RTWin80weeks", "date": 1411350017, "score": 5461, "comments": 803}}, {"type": "Feature", "id": "2dhgn4", "geometry": {"type": "Point", "coordinates": [-18.1718158, 63.771279]}, "properties": {"title": "\"If you drive up this dirt road for 5 minutes, You'll reach a small Canyon. It's really quite breathtaking.\" (Fja\u00f0r\u00e1rglj\u00fafur, Iceland) [OC] [2048x1058]", "image_link": "http://i.imgur.com/MJqwwTn.jpg", "username": "xeno_sapien", "date": 1407974654, "score": 5081, "comments": 356}}, {"type": "Feature", "id": "2k2cb0", "geometry": {"type": "Point", "coordinates": [35.4079087, 29.534667]}, "properties": {"title": "Bedouin nomads crossing the Wadi Rum desert, Jordan [6016 x 4000] [OC]", "image_link": "http://i.imgur.com/fIdt7Frm.jpg", "username": "ButtLickinBadBoy", "date": 1414039467, "score": 4979, "comments": 458}}, {"type": "Feature", "id": "2ijq1h", "geometry": {"type": "Point", "coordinates": [-149.8163645, 60.04377640000001]}, "properties": {"title": "Kenai Fjords National Park in Alaska, by Michael McRuiz [2400x1594]", "image_link": "https://i.imgur.com/jypHpBvm.jpg", "username": "jaycrew", "date": 1412683021, "score": 4882, "comments": 237}}, {"type": "Feature", "id": "2lxitm", "geometry": {"type": "Point", "coordinates": [-89.4012302, 43.0730517]}, "properties": {"title": "A beautiful little spot on the lake in Madison, WI [OC][4308x2871]", "image_link": "http://i.imgur.com/KjP1n1M.jpg", "username": "half_caulked_jack", "date": 1415677433, "score": 4829, "comments": 672}}, {"type": "Feature", "id": "2eaqp1", "geometry": {"type": "Point", "coordinates": [-121.1133076, 48.7121596]}, "properties": {"title": "I visited my sister in Washington. She told me the lakes were beautiful but I wasn't expecting this. Diablo Lake, WA. [3648x2736][OC]", "image_link": "http://i.imgur.com/2UPTd9c.jpg", "username": "[deleted]", "date": 1408734635, "score": 4599, "comments": 542}}]}
    return render_template('home.html', geojson=json.dumps(user_geoJSON))

@app.route('/api/v0.1/reddit_id', methods=['GET'])
def api_id():

    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    find = 'user_posts.' + id + '.id'
    found = submissions.find({find: id})
    urls = {}
    for post in found:
        results = {
            "extract": post['wiki_extract'],
            "title": post['wiki_title'],
            "reddit_title": post['user_posts'][id]['title'],
            "reddit_image": post['user_posts'][id]['thumb_url'],
            "reddit_score": post['user_posts'][id]['score'],
            "reddit_user": post['user_posts'][id]['author'],
            "reddit_comments": post['user_posts'][id]['num_comments'],
            "id": id,
            "other_posts": post['user_posts'][id]['user_content'],
            "pie_chart": post['user_posts'][id]['pie_chart'],
            "subreddit": post['subreddit']
        }
    return jsonify(results)

if __name__ == '__main__':
       app.debug = True
       app.run()
