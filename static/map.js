function initParse() {
    Parse.initialize("t40pLblmf3Tc1Lu8VL2eLup2VV0k8oyvbM5KFHNF", "lh5OvA4Ws2GGecGk2QK1qoiZmlrFjCJcYZl0rc3d");
}

function initMap() {
    initParse();
    var NetReport = Parse.Object.extend("NetReport");
    var query = new Parse.Query(NetReport);
    query.limit(200);
    query.find({
      success: function(results) {
        var heatmapData = [];
        // Do something with the returned Parse.Object values
        for (var i = 0; i < results.length; i++) {
            var object = results[i];
            //console.log(object.get('location')['_longitude']);
            heatmapData.push(new google.maps.LatLng(object.get('location')['_latitude'], object.get('location')['_longitude']))
        }
        var sanFrancisco = new google.maps.LatLng(17.774546, -92.433523);
        map = new google.maps.Map(document.getElementById('map'), {
            center: sanFrancisco,
            zoom: 2,
            mapTypeId: google.maps.MapTypeId.SATELLITE
        });

        var heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatmapData
        });
        heatmap.setMap(map);
      },
      error: function(error) {
            //alert("Error: " + error.code + " " + error.message);
      }
    });
}

var HTMLimg = '<img class="feed-img img-responsive" src=%data%>';
var HTMLtitle = '<div class="feed-title">%data%</div>';

function reloadLatest(){
    initParse();
    var NetReport = Parse.Object.extend("NetReport");
    var query = new Parse.Query(NetReport);
    query.limit(3);
    query.descending("timestamp");
    query.find({
      success: function(results) {
      for (var i = 0; i < results.length; i++) {
            var object = results[i];
            feed_title = 'Reported by ' + object.get('firstName') + ' at ' + object.get('timestamp');
            $( "#instantFeed" ).append(HTMLtitle.replace("%data%", feed_title));
            if (object.get('overallPhoto')) {
                $( "#instantFeed" ).append(HTMLimg.replace("%data%", object.get('overallPhoto')['_url']));
            } else {
                $( "#instantFeed" ).append(HTMLimg.replace("%data%", 'static/net_default.png'));
            }
        }
      },
      error: function(error) {
            //alert("Error: " + error.code + " " + error.message);
      }
    });
}
reloadLatest();