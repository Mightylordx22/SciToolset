import folium
from scripts.model_objects import total_missions
from folium.plugins.timestamped_geo_json import *




total_missions

the_map = folium.Map(location=[51.5074, 0.1278])

folium.TileLayer('OpenStreetMap').add_to(the_map)

folium.LayerControl().add_to(the_map)

def get_mission_coverage():
    polygons = []
    for mission in total_missions:
        for scene in mission.scenes:
            #print(scene.get_time())
            polygon = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': scene.get_scene_coords()
                },
                'properties': {
                    'style': {
                        'color': 'blue',
                    },
                    'times': scene.get_time()
                }
            }
            #print(scene.get_scene_coords())
            #folium.Marker(location=scene.get_scene_coords()[0][0][middle(scene.get_scene_coords())], popup= 'test',
                       #icon=folium.Icon(icon='green')).add_to(the_map)
            polygons.append(polygon)
    return polygons


TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': get_mission_coverage()},
    period='PT20S',
    duration='PT12H',
    auto_play=False,
    loop=True,
    loop_button=True,
    date_options='YYYY/MM/DD HH/mm/ss',
).add_to(the_map)

the_map.save("index.html")