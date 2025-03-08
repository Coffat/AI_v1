import streamlit as st
import os

# Cấu hình trang
st.set_page_config(
    page_title="Travel Itinerary Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
css_path = os.path.join("pages", "assets", "css", "style.css")
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <div class="logo-section">
                <span class="logo-icon">✈️</span>
                <div class="logo-text">
                    <h2>Travel Planner</h2>
                    <p>Lập lịch trình du lịch thông minh</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="sidebar-menu">
            <a href="/" class="menu-item active">
                <span class="menu-icon">🏠</span>
                <span class="menu-text">Trang chủ</span>
            </a>
            <a href="/input_form" class="menu-item">
                <span class="menu-icon">📝</span>
                <span class="menu-text">Lập lịch trình</span>
            </a>
            <a href="/map_view" class="menu-item">
                <span class="menu-icon">🗺️</span>
                <span class="menu-text">Bản đồ</span>
            </a>
            <a href="/schedule_view" class="menu-item">
                <span class="menu-icon">📅</span>
                <span class="menu-text">Lịch trình</span>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="sidebar-footer">
            <h4>Liên hệ hỗ trợ</h4>
            <div class="contact-item">
                <span class="contact-icon">📧</span>
                <span>support@travelplanner.com</span>
            </div>
            <div class="contact-item">
                <span class="contact-icon">📞</span>
                <span>1900 xxxx</span>
            </div>
            <div class="copyright">
                © 2024 Travel Planner
            </div>
        </div>
    """, unsafe_allow_html=True)

# Chuyển hướng đến trang chủ
st.switch_page("pages/home.py") 