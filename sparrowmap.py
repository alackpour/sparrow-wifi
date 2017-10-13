#!/usr/bin/python3

import os
import webbrowser

# ------------------  Map Markers  ------------------------------
class MapMarker(object):
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.label = ""
        self.barCount = 4
        
    def __str__(self):
        retVal = 'latitude: ' + str(self.latitude) + '\n'
        retVal += 'longitude: ' + str(self.longitude) + '\n'
        retVal += 'Label: ' + self.label + '\n'
        retVal += 'Bar Count: ' + str(self.barCount) + '\n'
        return retVal
        
# ------------------  Google Map Generator  ------------------------------
class MapEngine(object):
    MAP_TYPE_DEFAULT = 1
    MAP_TYPE_HYBRID = 2
    MAP_TYPE_SATELLITE_ONLY = 3
    MAP_TYPE_TERRAIN = 4
    
    def CenterCoord(markers):
        minlat = None
        maxlat = None
        minlong = None
        maxlong = None
        
        for curMarker in markers:
            if minlat == None:
                minlat = curMarker.latitude
            if maxlat == None:
                maxlat = curMarker.latitude
            if minlong == None:
                minlong = curMarker.longitude
            if maxlong == None:
                maxlong = curMarker.longitude
            
            if (curMarker.latitude < minlat):
                minlat = curMarker.latitude
                
            if (curMarker.latitude > maxlat):
                maxlat = curMarker.latitude
                
            if (curMarker.longitude < minlong):
                minlong = curMarker.longitude
                
            if (curMarker.longitude > maxlong):
                maxlong = curMarker.longitude

        meanLat = minlat + (maxlat - minlat)/2
        meanLong = minlong + (maxlong - minlong)/2
        
        return meanLat, meanLong
        
    def createMap(fileName,title,markers, connectMarkers=False, openWhenDone=True, mapType=MAP_TYPE_DEFAULT):
        centerLat, centerLong = MapEngine.CenterCoord(markers)
        
        # For satellite and hybrid maps, need to change the font color to white or it won't show up well
        labelColor = 'black'
        
        htmlString = '<html><head><meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n'
        htmlString += '<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n'
        htmlString += '<title>' + title + '</title>\n'
        htmlString += '<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false"></script>\n'
        htmlString += '<script type="text/javascript">\n'
        htmlString += '	function initialize() {\n'
        htmlString +='		var centerlatlng = new google.maps.LatLng('+str(centerLat) + ',' + str(centerLong) + ');\n'
        htmlString +='		var myOptions = {\n'
        htmlString +='			zoom: 16,\n'
        htmlString +='			center: centerlatlng,\n'
        if mapType == MapEngine.MAP_TYPE_HYBRID:
            htmlString +='			mapTypeId: google.maps.MapTypeId.HYBRID\n'
            labelColor = 'white'
        elif mapType == MapEngine.MAP_TYPE_SATELLITE_ONLY:
            htmlString +='			mapTypeId: google.maps.MapTypeId.SATELLITE_ONLY\n'
            labelColor = 'white'
        elif mapType == MapEngine.MAP_TYPE_TERRAIN:
            htmlString +='			mapTypeId: google.maps.MapTypeId.TERRAIN\n'
        else:
            htmlString +='			mapTypeId: google.maps.MapTypeId.ROADMAP\n'
        htmlString +='		};\n'
        
        # Map Canvas
        htmlString +='		var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n\n'
        
        markerPath = os.path.dirname(os.path.abspath(__file__)) + '/images'
        # Reusable markers
        htmlString +='		var iconSize = 24;\n'
        htmlString +='		var midPoint = iconSize / 2;\n'
        htmlString +='		var markerIcon4 = {\n'
        htmlString +="		  url: '" + markerPath + "/4_bars2.png',\n"
        htmlString +='		  scaledSize: new google.maps.Size(iconSize, iconSize),\n'
        htmlString +='		  origin: new google.maps.Point(0, 0),\n'
        htmlString +='		  anchor: new google.maps.Point(midPoint,iconSize-5),\n'
        htmlString +='		  labelOrigin: new google.maps.Point(15,33)\n'
        htmlString +='		};\n'
        htmlString +='		\n'
        htmlString +='		var markerIcon3 = {\n'
        htmlString +="		  url: '" + markerPath + "/3_bars2.png',\n"
        htmlString +='		  scaledSize: new google.maps.Size(iconSize, iconSize),\n'
        htmlString +='		  origin: new google.maps.Point(0, 0),\n'
        htmlString +='		  anchor: new google.maps.Point(midPoint,iconSize-5),\n'
        htmlString +='		  labelOrigin: new google.maps.Point(15,33)\n'
        htmlString +='		};\n'
        htmlString +='		\n'
        htmlString +='		var markerIcon2 = {\n'
        htmlString +="		  url: '" + markerPath + "/2_bars2.png',\n"
        htmlString +='		  scaledSize: new google.maps.Size(iconSize, iconSize),\n'
        htmlString +='		  origin: new google.maps.Point(0, 0),\n'
        htmlString +='		  anchor: new google.maps.Point(midPoint,iconSize-5),\n'
        htmlString +='		  labelOrigin: new google.maps.Point(15,33)\n'
        htmlString +='		};\n'
        htmlString +='		\n'
        htmlString +='		var markerIcon1 = {\n'
        htmlString +="		  url: '" + markerPath + "/1_bar2.png',\n"
        htmlString +='		  scaledSize: new google.maps.Size(iconSize, iconSize),\n'
        htmlString +='		  origin: new google.maps.Point(0, 0),\n'
        htmlString +='		  anchor: new google.maps.Point(midPoint,iconSize-5),\n'
        htmlString +='		  labelOrigin: new google.maps.Point(15,33)\n'
        htmlString +='		};\n'
        
        # create markers
        for curMarker in markers:
            htmlString +='		var latlng = new google.maps.LatLng(' + str(curMarker.latitude) + ', ' + str(curMarker.longitude) + ');\n'
            # htmlString +="		var img = new google.maps.MarkerImage('/usr/local/lib/python3.5/dist-packages/gmplot/markers/32CD32.png');\n"
            htmlString +='		var marker = new google.maps.Marker({\n'
            htmlString +='		title: "' + curMarker.label + '",\n'
            htmlString +='		label: {\n'
            htmlString +="		        text: '" + curMarker.label + "',\n"
            htmlString +="		        color: '" + labelColor+ "',\n"
            htmlString +='		},\n'
            # htmlString +='		icon: img,\n'
            htmlString +='		icon: markerIcon' + str(curMarker.barCount) + ',\n'
            htmlString +='		position: latlng\n'
            htmlString +='		});\n'
            htmlString +='		marker.setMap(map);\n'

        # If we're drawing lines between markers, draw the polyline
        if connectMarkers:
            htmlString +='		var PolylineCoordinates = [\n'
            for curMarker in markers:
                htmlString +='		new google.maps.LatLng(' + str(curMarker.latitude) + ', ' + str(curMarker.longitude) + '),\n'
            htmlString +='		];\n'

            htmlString +='		var Path = new google.maps.Polyline({\n'
            htmlString +='		clickable: false,\n'
            htmlString +='		geodesic: true,\n'
            htmlString +='		path: PolylineCoordinates,\n'
            htmlString +='		strokeColor: "#6495ED",\n'
            htmlString +='		strokeOpacity: 1.000000,\n'
            htmlString +='		strokeWeight: 10\n'
            htmlString +='		});\n'
            htmlString +='		Path.setMap(map);\n'

        htmlString +='	}\n'
        htmlString +='</script></head><body style="margin:0px; padding:0px;" onload="initialize()">\n'
        htmlString +='	<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n'
        htmlString +='</body></html>\n'

        # Write the new HTML file
        try:
            outputFile = open(fileName, 'w')
            outputFile.write(htmlString)
            outputFile.close()
            
            if openWhenDone:
                webbrowser.open(fileName)
                
            return True
        except:
            return False


# -------  Main Routine For Debugging-------------------------

if __name__ == '__main__':
    fileName = '/tmp/test.html'
    # centerLat = 37.428
    # centerLong = -122.145
    title = 'Google Map'
    
    markers = []
    newMarker = MapMarker()
    newMarker.latitude = 37.424000
    newMarker.longitude = -122.140000
    newMarker.label = '2 Bars'
    newMarker.barCount = 2
    markers.append(newMarker)
    
    newMarker = MapMarker()
    newMarker.latitude = 37.428000
    newMarker.longitude = -122.145000
    newMarker.label = '3 Bars'
    newMarker.barCount = 3
    markers.append(newMarker)
    
    newMarker = MapMarker()
    newMarker.latitude = 37.428000
    newMarker.longitude = -122.138000
    newMarker.label = '4 Bars'
    newMarker.barCount = 4
    markers.append(newMarker)
    
    MapEngine.createMap(fileName,title,markers, connectMarkers=True, openWhenDone=True, mapType=MapEngine.MAP_TYPE_HYBRID)
