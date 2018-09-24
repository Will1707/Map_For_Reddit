$('#score').slider({
  min: 5,
  max: 155000,
  step: 1
});

$("#comments").slider({
  min: 0,
  max: 3500,
  step: 1
});

$('#cluster').slider({});

$("#results").slider({
  min: 1,
  max: 5000,
  step: 1
});

$("#country").slider({});

$(function() {
  $('input[name="daterange"]').daterangepicker({
    opens: 'left'
  })
});

document.getElementById("reportrange").style.display = "none";

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function closeNav() {
  var sidebar = document.getElementById("userform");
  if (sidebar.style.display === "none") {
      sidebar.style.display = "initial";
      document.getElementById("openclose").style.marginLeft = "226px";
      document.getElementById("openclose").style.width = "22px";
      document.getElementById("rightArrow").style.display = "none";
      document.getElementById("leftArrow").style.display = "block";
  } else {
      sidebar.style.display = "none";
      document.getElementById("openclose").style.marginLeft = "-8px";
      document.getElementById("openclose").style.width = "30px";
      document.getElementById("leftArrow").style.display = "none";
      document.getElementById("rightArrow").style.display = "block";
  }
    // document.getElementById("userform").style.display = "none";
    // $("userform").toggle(1);
    // document.getElementById("openclose").style.marginLeft = "0";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function openNav() {
  document.getElementById("userform").style.display = "initial";
  // $("userform").toggle();
  document.getElementById("openclose").style.marginLeft = "226px";
  document.getElementById("openclose").style.boxSizing = "border-box";
}

function darkModeOn() {
  document.getElementById("userform").style.background = "#262626";
  panel = document.getElementsByClassName("panel")
  for (i = 0; i < panel.length; i++){
    panel[i].style.backgroundColor = "#262626";
  }
  accordion = document.getElementsByClassName("accordion")
  for (i = 0; i < accordion.length; i++){
    accordion[i].style.backgroundColor = "#393939";
  }
}

var ip;
// $.getJSON('https://api.ipstack.com/check?access_key=19c1afec565796258fa5b67088886265&format=1', function(data){
$.getJSON('https://geoip.tools/v1/json', function(data){
  delete data.ip
  delete data.type
  ip = JSON.stringify(data)
});

var otherPosts = [];

function getWikiExtract() {

  var apiURL = 'api/v0.1/reddit_id?id=' + document.getElementById("postScore").href.split("/")[6] + "&?ip=" + ip;
  delete ip
  $.ajax({
    type: 'GET',
    url: apiURL,
    dataType: "JSON", // data type expected from server
    success: function (data) {
      document.getElementById("wiki_title").innerHTML = data['title'];
      document.getElementById("wiki_extract").innerHTML = data['extract'];
      document.getElementById("wikipedia").href = "https://en.wikipedia.org/wiki/" + data['title'];
      document.getElementById("placeName").innerHTML = data['location_info']['location_name'];
      document.getElementById("localTime").innerHTML = data['local_time'];
      var lat = data['loc'][0].toString()
      var lng = data['loc'][1].toString()
      var weatherJSON;
      $.getJSON("https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lng + "&APPID=7986ad57675127ce999defef1beaa4dd", function(weather){
        document.getElementById("weatherTemp").innerHTML = (weather['main']['temp'] - 273.15).toFixed(0) + "&#176;C";
        document.getElementById("weatherDesc").innerHTML = weather['weather'][0]['description'];
      });
      document.getElementById("toCurrency").innerHTML = data['currency']['to_symbol'] + data['currency']['conversion'].toFixed(2);
      document.getElementById("fromCurrency").innerHTML = data['currency']['from_symbol'] + "1.00";
      document.getElementById("modalRedditUser").innerHTML      = data['reddit_user'];
      var redditLink     = "https://old.reddit.com/";

      document.getElementById("modalImageTitleLink").innerHTML      = data['reddit_title'];
      document.getElementById("modalImageImage").src                = data['reddit_image'];
      document.getElementById("modalImageSubLink").innerHTML        = 'r/' + data['subreddit'];
      document.getElementById("modalImageUserLink").innerHTML       = data['reddit_user'];
      document.getElementById("modalImageScoreLink").innerHTML      = data['reddit_score']    + ' points';
      document.getElementById("modalImageCommentsLink").innerHTML   = data['reddit_comments'] + ' comments';

      document.getElementById("modalImageTitleLink").href       = redditLink + 'r/earthporn/comments/' + data['id'];
      document.getElementById("modalImageSubLink").href         = redditLink + 'r/'           + data['subreddit'];
      document.getElementById("modalImageUserLink").href        = redditLink + 'user/'        + data['reddit_user'];
      document.getElementById("modalImageScoreLink").href       = redditLink + 'r/earthporn/comments/' + data['id'];
      document.getElementById("modalImageCommentsLink").href    = redditLink + 'r/earthporn/comments/' + data['id'];

      if (data['other_posts'] != null) {
        for (var key in data['other_posts']) {
          for (i=0; i <= data['other_posts'][key].length; i++) {
            if (data['other_posts'][key][i] != undefined){
              otherPosts.push(data['other_posts'][key][i])
            }
          }
        }
      } else {
          otherPosts = [];
      };

      for (i=1; i < 4; i++){
        var image           = "modalMiniImage" + i;
        var subLink         = "modalMiniLinkSub" + i;
        var userLink        = "modalMiniLinkUser" + i;
        var scoreLink       = "modalMiniLinkScore" + i;
        var commmentsLink   = "modalMiniLinkComments" + i;

        document.getElementById(image).src                = "";
        document.getElementById(subLink).innerHTML        = "";
        document.getElementById(userLink).innerHTML       = "";
        document.getElementById(scoreLink).innerHTML      = "";
        document.getElementById(commmentsLink).innerHTML  = "";
      };

      if (data['other_posts'] == null) {
        otherPosts = [];
        for (i=1; i < 5; i++) {
          var modalmini = "modalmini" + i;
          document.getElementById(modalmini).style.display = "none";
        };
      } else {
          if ('earthporn' in data['other_posts']) {
            if ( data['other_posts']['earthporn'].length <= 3) {
              var maxLength = data['other_posts']['earthporn'].length + 1;
              for (i=data['other_posts']['earthporn'].length + 1; i < 4; i++){
                var modalmini = "modalmini" + i;
                document.getElementById(modalmini).style.display = "none";
              };
              document.getElementById('modalmini4').style.display = "block";
            } else {
                var maxLength = 4;
                document.getElementById('modalmini4').style.display = "block";
            }
            var subreddit = 'earthporn'
          } else {
              for (var key in data['other_posts']) {
                if ( data['other_posts'][key].length <= 3) {
                  var maxLength = data['other_posts'][key].length + 1;
                  for (i=data['other_posts'][key].length + 1; i < 4; i++){
                    var modalmini = "modalmini" + i;
                    document.getElementById(modalmini).style.display = "none";
                  };
                  document.getElementById('modalmini4').style.display = "block";
                } else {
                    var maxLength = 4;
                    document.getElementById('modalmini4').style.display = "block";
                }
                var subreddit = key
              }
            }
      };

      for (i=1; i < maxLength; i++) {

        var modalmini      = "modalmini" + i;
        var image          = "modalMiniImage" + i;
        var subLink        = "modalMiniLinkSub" + i;
        var userLink       = "modalMiniLinkUser" + i;
        var scoreLink      = "modalMiniLinkScore" + i;
        var commmentsLink  = "modalMiniLinkComments" + i;

        document.getElementById(modalmini).style.display  = "block";

        var thumb_image = data['other_posts'][subreddit][i - 1]['url']
        if (thumb_image.includes("imgur") && !thumb_image.includes(".jpg") && !thumb_image.includes(".png")) {
          thumb_image = thumb_image + "m.jpg"
        }

        document.getElementById(image).src                = thumb_image;
        document.getElementById(subLink).innerHTML        = 'r/' + data['other_posts'][subreddit][i - 1]['subreddit'];
        document.getElementById(userLink).innerHTML       = data['reddit_user'];
        document.getElementById(scoreLink).innerHTML      = data['other_posts'][subreddit][i - 1]['score']    + ' points';
        document.getElementById(commmentsLink).innerHTML  = data['other_posts'][subreddit][i - 1]['comments'] + ' comments';

        document.getElementById(subLink).href         = redditLink + 'r/'     + data['other_posts'][subreddit][i - 1]['subreddit'];
        document.getElementById(userLink).href        = redditLink + 'user/'  + data['reddit_user'];
        document.getElementById(scoreLink).href       = redditLink + 'r/'     + data['other_posts'][subreddit][i - 1]['subreddit'] + '/comments/' + data['other_posts']['earthporn'][i - 1]['id'];
        document.getElementById(commmentsLink).href   = redditLink + 'r/'     + data['other_posts'][subreddit][i - 1]['subreddit'] + '/comments/' + data['other_posts']['earthporn'][i - 1]['id'];
      };
    },
    error: function() {
      console.log('Error: ' + data);
    }
  });
  }

  function nextImages () {

    for (i=1; i < 4; i++){
      var image = "modalMiniImage" + i;
      src = document.getElementById(image).src
      if (window.location.href != src) {
          otherPosts.shift()
      }
    };
    var otherPostsLength = otherPosts.length;

    if (otherPostsLength => 3){
      for (i=1; i < 4; i++){

        var redditLink     = "https://www.reddit.com/";
        var modalmini      = "modalmini" + i;
        var image          = "modalMiniImage" + i;
        var subLink        = "modalMiniLinkSub" + i;
        var userLink       = "modalMiniLinkUser" + i;
        var scoreLink      = "modalMiniLinkScore" + i;
        var commmentsLink  = "modalMiniLinkComments" + i;

        document.getElementById(modalmini).style.display = "block";

        var thumb_image = otherPosts[i - 1]['url']
        if (thumb_image.includes("imgur") && !thumb_image.includes(".jpg") && !thumb_image.includes(".png")) {
          thumb_image = thumb_image + "m.jpg"
        }

        document.getElementById(image).src                = otherPosts[i - 1]['url'] + "m.jpg";
        document.getElementById(subLink).innerHTML        = 'r/' + otherPosts[i - 1]['subreddit'];
        document.getElementById(userLink).innerHTML       = document.getElementById("modalImageUserLink").innerHTML;
        document.getElementById(scoreLink).innerHTML      = otherPosts[i - 1]['score']    + ' points';
        document.getElementById(commmentsLink).innerHTML  = otherPosts[i - 1]['comments'] + ' comments';

        document.getElementById(subLink).href         = redditLink + 'r/'     + otherPosts[i - 1]['subreddit'];
        document.getElementById(userLink).href        = redditLink + 'user/'  + "Willlll";
        document.getElementById(scoreLink).href       = redditLink + 'r/'     + otherPosts[i - 1]['subreddit'] + '/comments/' + otherPosts[i - 1]['id'];
        document.getElementById(commmentsLink).href   = redditLink + 'r/'     + otherPosts[i - 1]['subreddit'] + '/comments/' + otherPosts[i - 1]['id'];
      };
    };
  }

    function getPieChart() {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(makePieChart);
    };

    function makePieChart() {
      var apiURL = 'api/v0.1/reddit_id?id=' + document.getElementById("postScore").href.split("/")[6];
      $.ajax({
        'type': "Get",
        'dataType': 'JSON',
        'url': apiURL,
        'success': function (data) {
          pie_chart = [];
          pie_chart.push(['Subreddit', 'Posts']);
          for (var key in data['pie_chart']) {
            pie_chart.push([key, data['pie_chart'][key]]);
          }
          var data = google.visualization.arrayToDataTable(pie_chart);

          var options = {
            width: 700,
            height: 400,
            backgroundColor: '#f7f7f7',
            pieSliceText: 'none'
          };

          var chart = new google.visualization.PieChart(document.getElementById('piechart'));

          chart.draw(data, options);
        }
      })
    };

    function locationSelected() {
      document.getElementById("toptabsUser").style.backgroundColor = "#eff7ff";
      document.getElementById("toptabsUser").style.borderBottomStyle = "none";
      document.getElementById("toptabsUserLink").style.color = "#336699";
      var userTab = document.getElementById("toptabsUser");
      userTab.style.borderTop = "none";
      userTab.style.borderLeft = "none";
      userTab.style.borderRight = "none";
      var locationTab = document.getElementById("toptabsLocation");
      locationTab.style.borderBottom = "solid #f7f7f7 2px";
      locationTab.style.borderTop = "solid #5f99cf 1px";
      locationTab.style.borderLeft = "solid #5f99cf 1px";
      locationTab.style.borderRight = "solid #5f99cf 1px";
      locationTab.style.backgroundColor = "#f7f7f7";
      document.getElementById("toptabsLocationLink").style.color = "orangered";
      document.getElementById("redditUser").style.display = "none";
      document.getElementById("locationInfo").style.display = "block";
    };

    function userSelected() {
      document.getElementById("toptabsLocation").style.backgroundColor = "#eff7ff";
      document.getElementById("toptabsLocation").style.borderBottomStyle = "none";
      document.getElementById("toptabsLocationLink").style.color = "#336699";
      var locationTab = document.getElementById("toptabsLocation");
      locationTab.style.borderTop = "none";
      locationTab.style.borderLeft = "none";
      locationTab.style.borderRight = "none";
      var userTab = document.getElementById("toptabsUser");
      userTab.style.borderBottom = "solid #f7f7f7 2px";
      userTab.style.borderTop = "solid #5f99cf 1px";
      userTab.style.borderLeft = "solid #5f99cf 1px";
      userTab.style.borderRight = "solid #5f99cf 1px";
      userTab.style.backgroundColor = "#f7f7f7";
      document.getElementById("toptabsUserLink").style.color = "orangered";
      document.getElementById("locationInfo").style.display = "none";
      document.getElementById("redditUser").style.display = "block";
    };
