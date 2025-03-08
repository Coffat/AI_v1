import streamlit as st
import folium
from streamlit_folium import folium_static
import json
from datetime import datetime

class MapComponent:
    def __init__(self):
        self.map = None
        self.markers = []
        self.routes = []
        
    def create_map(self, center_lat=16.047079, center_lng=108.206230, zoom_start=6):
        """Khởi tạo bản đồ với tọa độ trung tâm và mức zoom"""
        self.map = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=zoom_start,
            tiles='OpenStreetMap'
        )
        
    def add_marker(self, lat, lng, popup_text, icon_color='red', icon_type='info-sign'):
        """Thêm marker vào bản đồ"""
        if self.map:
            folium.Marker(
                location=[lat, lng],
                popup=popup_text,
                icon=folium.Icon(color=icon_color, icon=icon_type)
            ).add_to(self.map)
            self.markers.append({'lat': lat, 'lng': lng, 'popup': popup_text})
            
    def add_route(self, points, color='blue', weight=3):
        """Thêm tuyến đường vào bản đồ"""
        if self.map and len(points) >= 2:
            folium.PolyLine(
                points,
                color=color,
                weight=weight,
                opacity=0.8
            ).add_to(self.map)
            self.routes.append(points)
            
    def add_circle(self, lat, lng, radius, color='red', fill=True):
        """Thêm vòng tròn vào bản đồ"""
        if self.map:
            folium.Circle(
                radius=radius,
                location=[lat, lng],
                color=color,
                fill=fill,
                popup=f'Bán kính: {radius}m'
            ).add_to(self.map)
            
    def add_heatmap(self, data_points):
        """Thêm bản đồ nhiệt"""
        if self.map:
            folium.plugins.HeatMap(data_points).add_to(self.map)
            
    def add_cluster(self, markers):
        """Thêm cluster markers"""
        if self.map:
            marker_cluster = folium.plugins.MarkerCluster()
            for marker in markers:
                folium.Marker(
                    location=[marker['lat'], marker['lng']],
                    popup=marker['popup'],
                    icon=folium.Icon(color=marker.get('color', 'red'))
                ).add_to(marker_cluster)
            marker_cluster.add_to(self.map)
            
    def add_control(self, control_type='zoom'):
        """Thêm các điều khiển vào bản đồ"""
        if self.map:
            if control_type == 'zoom':
                folium.plugins.ZoomControl().add_to(self.map)
            elif control_type == 'fullscreen':
                folium.plugins.Fullscreen().add_to(self.map)
            elif control_type == 'mouseposition':
                folium.plugins.MousePosition().add_to(self.map)
                
    def render(self, height=600):
        """Hiển thị bản đồ"""
        if self.map:
            return folium_static(self.map, height=height)
        return None

def create_interactive_map(locations, routes=None, center=None):
    """Hàm tiện ích để tạo bản đồ tương tác"""
    if not center:
        center = [16.047079, 108.206230]  # Tọa độ mặc định
        
    map_component = MapComponent()
    map_component.create_map(center[0], center[1])
    
    # Thêm các marker cho địa điểm
    for loc in locations:
        map_component.add_marker(
            lat=loc['lat'],
            lng=loc['lng'],
            popup_text=loc['name'],
            icon_color=loc.get('color', 'red')
        )
    
    # Thêm các tuyến đường nếu có
    if routes:
        for route in routes:
            map_component.add_route(
                points=route['points'],
                color=route.get('color', 'blue')
            )
    
    # Thêm các điều khiển
    map_component.add_control('zoom')
    map_component.add_control('fullscreen')
    map_component.add_control('mouseposition')
    
    return map_component.render() 