import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import folium_static
import pandas as pd
import os
from datetime import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Bản đồ lộ trình - Travel Itinerary Planner",
    page_icon="🗺️",
    layout="wide"
)

# Load custom CSS
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, '..', 'assets', 'css', 'style.css')
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    # If CSS file is not found, we'll skip loading it
    # The inline CSS defined later will still work
    pass

# Background với Gradient Overlay và Particles
st.markdown("""
    <div class="background-overlay"></div>
    <div class="particles"></div>
""", unsafe_allow_html=True)

# Tiêu đề trang với animation
st.markdown("""
    <div class="page-header">
        <div class="header-content glass-morphism">
            <div class="header-icon-wrapper">
                <div class="header-icon">🗺️</div>
                <div class="icon-ring"></div>
            </div>
            <h1>Bản đồ lộ trình</h1>
            <p>Xem lộ trình du lịch của bạn trên bản đồ tương tác</p>
            <div class="header-decoration"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Container cho lựa chọn hiển thị
st.markdown("""
    <div class="options-container glass-morphism">
        <div class="options-header">
            <h3>Tùy chọn hiển thị</h3>
        </div>
        <div class="options-content">
""", unsafe_allow_html=True)

# Tạo các tùy chọn hiển thị
col1, col2, col3 = st.columns(3)
with col1:
    show_hotels = st.checkbox("Hiển thị khách sạn", value=True)
with col2:
    show_restaurants = st.checkbox("Hiển thị nhà hàng", value=True)
with col3:
    show_attractions = st.checkbox("Hiển thị điểm tham quan", value=True)

st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# Tọa độ các điểm du lịch (mẫu)
LOCATIONS = {
    "Hà Nội": [21.0285, 105.8542],
    "Hồ Chí Minh": [10.8231, 106.6297],
    "Đà Nẵng": [16.0544, 108.2022],
    "Huế": [16.4637, 107.5909],
    "Hội An": [15.8802, 108.3383],
    "Nha Trang": [12.2388, 109.1967],
    "Phú Quốc": [10.3468, 103.9213],
    "Sapa": [22.3402, 103.8440],
    "Hạ Long": [20.9516, 107.0784],
    "Phong Nha": [17.5897, 106.2833],
    "Mũi Né": [10.9589, 108.2729],
    "Đà Lạt": [11.9404, 108.4587],
    "Côn Đảo": [8.6821, 106.6077]
}

# Tạo bản đồ
m = folium.Map(location=[16.047079, 108.206230], zoom_start=6, tiles="CartoDB positron")

# Custom icon cho các điểm đến
icon_tourist = folium.Icon(color='red', icon='info-sign')
icon_hotel = folium.Icon(color='blue', icon='home')
icon_restaurant = folium.Icon(color='green', icon='cutlery')
icon_attraction = folium.Icon(color='purple', icon='camera')

# Thêm markers cho các điểm
for dest, coords in LOCATIONS.items():
    popup_content = f'''
    <div class="custom-popup">
        <h4>{dest}</h4>
        <p>Điểm du lịch nổi tiếng</p>
        <div class="popup-footer">
            <span>Thêm vào lịch trình</span>
        </div>
    </div>
    '''
    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_content, max_width=300),
        icon=icon_tourist,
        tooltip=dest
    ).add_to(m)

# Thêm khách sạn mẫu nếu được chọn
if show_hotels:
    hotels = {
        "Khách sạn Hà Nội": [21.0305, 105.8500],
        "Khách sạn Hồ Chí Minh": [10.8260, 106.6330],
        "Khách sạn Đà Nẵng": [16.0570, 108.2050],
    }
    for hotel, coords in hotels.items():
        folium.Marker(
            location=coords,
            popup=hotel,
            icon=icon_hotel,
            tooltip=hotel
        ).add_to(m)

# Thêm nhà hàng mẫu nếu được chọn
if show_restaurants:
    restaurants = {
        "Nhà hàng Hà Nội": [21.0320, 105.8570],
        "Nhà hàng Hồ Chí Minh": [10.8290, 106.6350],
        "Nhà hàng Đà Nẵng": [16.0590, 108.2080],
    }
    for restaurant, coords in restaurants.items():
        folium.Marker(
            location=coords,
            popup=restaurant,
            icon=icon_restaurant,
            tooltip=restaurant
        ).add_to(m)

# Thêm điểm tham quan mẫu nếu được chọn
if show_attractions:
    attractions = {
        "Hồ Gươm": [21.0285, 105.8525],
        "Bến Nhà Rồng": [10.8231, 106.6280],
        "Cầu Rồng": [16.0610, 108.2240],
    }
    for attraction, coords in attractions.items():
        folium.Marker(
            location=coords,
            popup=attraction,
            icon=icon_attraction,
            tooltip=attraction
        ).add_to(m)

# Vẽ đường đi (mẫu)
route_coords = [
    [21.0285, 105.8542],  # Hà Nội
    [16.4637, 107.5909],  # Huế
    [15.8802, 108.3383],  # Hội An
    [10.8231, 106.6297]   # Hồ Chí Minh
]

# Thêm đường đi với kiểu dáng đẹp hơn
folium.PolyLine(
    route_coords,
    weight=5,
    color='#4F46E5',
    opacity=0.7,
    dash_array='10'
).add_to(m)

# Thêm mũi tên chỉ hướng trên đường đi
folium.plugins.AntPath(
    route_coords,
    color='#6366F1',
    weight=4,
    opacity=0.7,
    delay=500,
    dash_array=[10, 20],
    pulse_color='#818CF8'
).add_to(m)

# Hiển thị bản đồ trong container đẹp hơn
st.markdown("""
    <div class="map-container glass-morphism">
        <div class="map-header">
            <h2><i class="fas fa-map-marked-alt"></i> Bản đồ lộ trình du lịch</h2>
            <p>Các điểm đến và đường đi tối ưu cho hành trình của bạn</p>
        </div>
""", unsafe_allow_html=True)

folium_static(m, width=1150, height=600)

st.markdown("""
    </div>
""", unsafe_allow_html=True)

# Thông tin lộ trình trong card hiện đại
st.markdown("""
    <div class="route-info glass-morphism">
        <div class="route-header">
            <div class="route-header-icon">
                <i class="fas fa-route"></i>
            </div>
            <h2>Thông tin lộ trình</h2>
            <p>Chi tiết về hành trình du lịch của bạn</p>
        </div>
        <div class="route-details">
            <div class="route-item">
                <div class="route-item-icon">🛣️</div>
                <span class="route-label">Tổng quãng đường</span>
                <span class="route-value">1,500 km</span>
            </div>
            <div class="route-item">
                <div class="route-item-icon">⏱️</div>
                <span class="route-label">Thời gian di chuyển</span>
                <span class="route-value">24 giờ</span>
            </div>
            <div class="route-item">
                <div class="route-item-icon">📍</div>
                <span class="route-label">Số điểm dừng</span>
                <span class="route-value">4 điểm</span>
            </div>
            <div class="route-item">
                <div class="route-item-icon">💰</div>
                <span class="route-label">Chi phí di chuyển</span>
                <span class="route-value">2,500,000 VNĐ</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Danh sách các điểm đến theo trình tự
st.markdown("""
    <div class="timeline-container glass-morphism">
        <div class="timeline-header">
            <h2>Lộ trình chi tiết</h2>
            <p>Hành trình của bạn theo trình tự thời gian</p>
        </div>
        <div class="timeline">
            <div class="timeline-item">
                <div class="timeline-date">Ngày 1</div>
                <div class="timeline-content">
                    <h3>Hà Nội</h3>
                    <p>Bắt đầu hành trình tại thủ đô nghìn năm văn hiến</p>
                    <div class="timeline-details">
                        <span class="timeline-tag">Khách sạn: Sofitel Legend Metropole</span>
                        <span class="timeline-tag">Hoạt động: Tham quan Văn Miếu</span>
                    </div>
                </div>
            </div>
            <div class="timeline-item">
                <div class="timeline-date">Ngày 3</div>
                <div class="timeline-content">
                    <h3>Huế</h3>
                    <p>Khám phá cố đô Huế với các di sản văn hóa</p>
                    <div class="timeline-details">
                        <span class="timeline-tag">Khách sạn: Azerai La Residence</span>
                        <span class="timeline-tag">Hoạt động: Tham quan Đại Nội</span>
                    </div>
                </div>
            </div>
            <div class="timeline-item">
                <div class="timeline-date">Ngày 5</div>
                <div class="timeline-content">
                    <h3>Hội An</h3>
                    <p>Trải nghiệm không gian cổ kính của phố cổ Hội An</p>
                    <div class="timeline-details">
                        <span class="timeline-tag">Khách sạn: Anantara Hoi An</span>
                        <span class="timeline-tag">Hoạt động: Dạo phố đèn lồng</span>
                    </div>
                </div>
            </div>
            <div class="timeline-item">
                <div class="timeline-date">Ngày 7</div>
                <div class="timeline-content">
                    <h3>Hồ Chí Minh</h3>
                    <p>Kết thúc hành trình tại thành phố năng động</p>
                    <div class="timeline-details">
                        <span class="timeline-tag">Khách sạn: Park Hyatt Saigon</span>
                        <span class="timeline-tag">Hoạt động: Tham quan Nhà thờ Đức Bà</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Nút chuyển hướng
st.markdown("""
    <div class="nav-buttons">
        <a href="./input_form" class="nav-button back-button">
            <span class="nav-icon">←</span>
            <span class="nav-text">Quay lại nhập thông tin</span>
        </a>
        <a href="./schedule_view" class="nav-button next-button">
            <span class="nav-text">Xem lịch trình chi tiết</span>
            <span class="nav-icon">→</span>
        </a>
    </div>
""", unsafe_allow_html=True)

# Floating Action Button để tải xuống bản đồ
st.markdown("""
    <div class="floating-download">
        <div class="download-button">
            <span class="download-icon">⬇️</span>
            <div class="download-tooltip">Tải xuống bản đồ</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Thêm CSS cho trang bản đồ
st.markdown("""
    <style>
        /* Global Styles */
        :root {
            --primary-gradient: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            --secondary-gradient: linear-gradient(135deg, #EC4899 0%, #D946EF 100%);
            --background-gradient: linear-gradient(135deg, #E0F2FE 0%, #DBEAFE 50%, #E0E7FF 100%);
            --glass-background: rgba(255, 255, 255, 0.7);
            --glass-border: rgba(255, 255, 255, 0.5);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Glass Morphism */
        .glass-morphism {
            background: var(--glass-background);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow);
            border-radius: 20px;
        }
        
        /* Background & Particles */
        .background-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--background-gradient);
            z-index: -2;
        }
        
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(99, 102, 241, 0.1) 1%, transparent 1%),
                radial-gradient(circle at 75% 75%, rgba(236, 72, 153, 0.1) 1%, transparent 1%);
            background-size: 100px 100px;
            animation: particleMove 20s linear infinite;
            z-index: -1;
        }
        
        @keyframes particleMove {
            0% {
                background-position: 0 0;
            }
            100% {
                background-position: 100px 100px;
            }
        }
        
        /* Header Styles */
        .header-content {
            position: relative;
            overflow: hidden;
            padding: 3rem 4rem;
            border-radius: 30px;
            text-align: center;
            margin: 2rem 0 3rem;
        }
        
        .header-icon-wrapper {
            position: relative;
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
        }
        
        .header-icon {
            position: relative;
            z-index: 2;
            font-size: 3.5rem;
            animation: iconFloat 3s ease-in-out infinite;
        }
        
        .icon-ring {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100%;
            height: 100%;
            border: 3px solid rgba(99, 102, 241, 0.2);
            border-radius: 50%;
            animation: ringPulse 2s ease-out infinite;
        }
        
        .header-decoration {
            position: absolute;
            bottom: -20px;
            left: 0;
            right: 0;
            height: 40px;
            background: linear-gradient(transparent, rgba(255, 255, 255, 0.1));
            filter: blur(10px);
        }
        
        /* Options Container */
        .options-container {
            padding: 1.5rem;
            margin-bottom: 2rem;
            animation: fadeIn 0.8s ease;
        }
        
        .options-header {
            margin-bottom: 1rem;
        }
        
        .options-header h3 {
            font-size: 1.2rem;
            margin: 0;
            color: #4F46E5;
        }
        
        /* Map Container */
        .map-container {
            padding: 2rem;
            margin: 2rem auto;
            max-width: 1200px;
            animation: slideUp 0.8s ease;
        }
        
        .map-header {
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .map-header h2 {
            font-size: 1.8rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .map-header p {
            color: #666;
            font-size: 1rem;
        }
        
        /* Route Info */
        .route-info {
            padding: 2rem;
            margin: 2rem auto;
            max-width: 1000px;
            animation: slideUp 0.8s ease 0.2s;
        }
        
        .route-header {
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
        }
        
        .route-header-icon {
            font-size: 2.5rem;
            color: #4F46E5;
            margin-bottom: 1rem;
        }
        
        .route-header h2 {
            font-size: 1.8rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .route-header p {
            color: #666;
            font-size: 1rem;
        }
        
        .route-details {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
        }
        
        .route-item {
            text-align: center;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        .route-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .route-item-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        .route-label {
            display: block;
            color: #666;
            margin-bottom: 0.5rem;
        }
        
        .route-value {
            display: block;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        /* Timeline */
        .timeline-container {
            padding: 2rem;
            margin: 2rem auto;
            max-width: 1000px;
            animation: slideUp 0.8s ease 0.4s;
        }
        
        .timeline-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .timeline-header h2 {
            font-size: 1.8rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .timeline-header p {
            color: #666;
            font-size: 1rem;
        }
        
        .timeline {
            position: relative;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .timeline::after {
            content: '';
            position: absolute;
            width: 6px;
            background-color: #E0E7FF;
            top: 0;
            bottom: 0;
            left: 50px;
            margin-left: -3px;
            border-radius: 10px;
        }
        
        .timeline-item {
            padding: 0 0 2rem 80px;
            position: relative;
        }
        
        .timeline-date {
            position: absolute;
            width: 50px;
            height: 50px;
            left: 0;
            background: var(--primary-gradient);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            z-index: 1;
        }
        
        .timeline-content {
            padding: 1.5rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .timeline-content:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .timeline-content h3 {
            margin-top: 0;
            color: #4F46E5;
        }
        
        .timeline-details {
            margin-top: 1rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .timeline-tag {
            background: #E0E7FF;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #4F46E5;
        }
        
        /* Navigation Buttons */
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin: 3rem auto;
            max-width: 800px;
        }
        
        .nav-button {
            display: flex;
            align-items: center;
            padding: 1rem 2rem;
            background: var(--glass-background);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 10px;
            text-decoration: none;
            color: #333;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .nav-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        
        .back-button {
            color: #6B7280;
        }
        
        .next-button {
            background: var(--primary-gradient);
            color: white;
        }
        
        .nav-icon {
            font-size: 1.2rem;
            margin: 0 0.5rem;
        }
        
        /* Floating Download Button */
        .floating-download {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 100;
        }
        
        .download-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--primary-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 5px 20px rgba(79, 70, 229, 0.3);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .download-button:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
        }
        
        .download-icon {
            font-size: 1.8rem;
            color: white;
        }
        
        .download-tooltip {
            position: absolute;
            right: 70px;
            background: white;
            padding: 8px 15px;
            border-radius: 8px;
            font-size: 0.9rem;
            white-space: nowrap;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        
        .download-button:hover .download-tooltip {
            opacity: 1;
            visibility: visible;
        }
        
        /* Custom Folium Popup */
        .custom-popup .leaflet-popup-content-wrapper {
            background: white;
            color: #333;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        
        .custom-popup .leaflet-popup-content {
            margin: 0;
            padding: 10px 15px;
        }
        
        .custom-popup .leaflet-popup-tip {
            background: white;
        }
        
        .popup-footer {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
            color: #4F46E5;
            font-weight: 600;
            cursor: pointer;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { 
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes iconFloat {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        
        @keyframes ringPulse {
            0% {
                transform: translate(-50%, -50%) scale(0.8);
                opacity: 0.5;
            }
            100% {
                transform: translate(-50%, -50%) scale(1.5);
                opacity: 0;
            }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .header-content {
                padding: 2rem;
            }
            
            .route-details {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .timeline::after {
                left: 30px;
            }
            
            .timeline-item {
                padding-left: 60px;
            }
            
            .timeline-date {
                width: 40px;
                height: 40px;
                font-size: 0.8rem;
            }
            
            .nav-buttons {
                flex-direction: column;
                gap: 1rem;
            }
            
            .nav-button {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
    
    <script>
        // Add FontAwesome for icons
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css';
        document.head.appendChild(link);
    </script>
""", unsafe_allow_html=True) 