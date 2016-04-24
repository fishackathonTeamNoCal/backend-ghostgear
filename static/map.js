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
            if (object.get('location')) {
                heatmapData.push(new google.maps.LatLng(object.get('location')['_latitude'], object.get('location')['_longitude']))
            }
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
            timestamp = String(object.get('timestamp'));
            date = timestamp.substring(0, timestamp.length-23);
            time = timestamp.substring(timestamp.length-23, timestamp.length-18);
            feed_title = '<b>Reported by </b><em>' + object.get('firstName') + '</em> <br> on ' + date + ' at ' + time;
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

function donutChart() {
    var width = 400,
        height = 400,
        radius = Math.min(width, height) / 2;

    var color = d3.scale.ordinal()
        .range(["#e6ff56", "#43bbca", "#ff1774", "#62646C", "#ff9b5a", "#3ac1f3", "#7f94f7"]);

    var arc = d3.svg.arc()
        .outerRadius(radius - 10)
        .innerRadius(radius - 70);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d) { return d.count; });

    var svg = d3.select("#donutChart").append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var data = [{'mesh_size':'<24mm', 'count':'10'}, {'mesh_size':'25-41mm', 'count':'17'}, {'mesh_size':'42-57mm', 'count':'37'},
        {'mesh_size':'58-75mm', 'count':'58'}, {'mesh_size':'76-94mm', 'count':'42'}, {'mesh_size':'95-124mm', 'count':'22'}]

    var g = svg.selectAll(".arc")
      .data(pie(data))
    .enter().append("g")
      .attr("class", "arc");

    g.append("path")
      .attr("d", arc)
      .style("fill", function(d) { return color(d.data.mesh_size); });

    g.append("text")
      .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
      .attr("dy", ".35em")
      .text(function(d) { return d.data.mesh_size; });
}
donutChart();

function type(d) {
  d.count = +d.count;
  return d;
}
