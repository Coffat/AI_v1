import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Lịch trình chi tiết - Travel Itinerary Planner",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# Additional CSS for enhanced UI
st.markdown("""
<style>
    /* Animation Keyframes */
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Modern Color Variables */
    :root {
        --primary: #3b82f6;
        --secondary: #6366f1;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --background: #f8fafc;
        --text: #1e293b;
        --text-light: #64748b;
        --border: #e2e8f0;
    }

    /* Timeline Styles */
    .timeline-container {
        position: relative;
        padding: 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin: 2rem 0;
        animation: fadeIn 0.6s ease-out;
    }

    .timeline-item {
        display: flex;
        align-items: flex-start;
        padding: 1.5rem;
        margin: 1rem 0;
        background: var(--background);
        border-radius: 12px;
        border-left: 4px solid var(--primary);
        transition: all 0.3s ease;
    }

    .timeline-item:hover {
        transform: translateX(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .timeline-time {
        min-width: 100px;
        font-weight: 600;
        color: var(--primary);
    }

    .timeline-content {
        margin-left: 2rem;
    }

    /* Activity Card Styles */
    .activity-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
    }

    .activity-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }

    .activity-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    /* Stats Card Styles */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .stats-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }

    .stats-card:hover {
        transform: translateY(-5px);
    }

    .stats-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0.5rem 0;
    }

    /* Weather Widget Styles */
    .weather-widget {
        background: linear-gradient(135deg, #6366f1, #3b82f6);
        color: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }

    .weather-icon {
        font-size: 3rem;
        margin: 1rem 0;
    }

    /* Cost Breakdown Styles */
    .cost-breakdown {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }

    .cost-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid var(--border);
    }

    .cost-category {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    /* Button Styles */
    .custom-button {
        background: var(--primary);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
    }

    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown("""
<div class="page-header">
    <h1>📅 Lịch trình chi tiết</h1>
    <p>Xem và quản lý lịch trình du lịch của bạn</p>
</div>
""", unsafe_allow_html=True)

# Sample data (in practice, this would come from your database)
schedule_data = {
    'Ngày': ['Ngày 1', 'Ngày 1', 'Ngày 1', 'Ngày 2', 'Ngày 2', 'Ngày 2', 'Ngày 3', 'Ngày 3', 'Ngày 3'],
    'Thời gian': ['08:00', '10:00', '12:00', '09:00', '11:00', '14:00', '08:00', '10:00', '12:00'],
    'Hoạt động': ['Ăn sáng', 'Tham quan', 'Ăn trưa', 'Ăn sáng', 'Tham quan', 'Ăn trưa', 'Ăn sáng', 'Tham quan', 'Ăn trưa'],
    'Địa điểm': ['Khách sạn A', 'Văn Miếu', 'Nhà hàng B', 'Khách sạn A', 'Hoàng thành', 'Nhà hàng C', 'Khách sạn A', 'Chùa Một Cột', 'Nhà hàng D'],
    'Chi phí (VNĐ)': [50000, 30000, 150000, 50000, 40000, 150000, 50000, 25000, 150000],
    'Loại': ['Ăn uống', 'Văn hóa', 'Ăn uống', 'Ăn uống', 'Văn hóa', 'Ăn uống', 'Ăn uống', 'Văn hóa', 'Ăn uống'],
    'Icon': ['🍳', '🏛️', '🍜', '🍳', '🏰', '🍜', '🍳', '⛩️', '🍜']
}

df = pd.DataFrame(schedule_data)

# Stats Cards
total_cost = df['Chi phí (VNĐ)'].sum()
total_activities = len(df)
unique_locations = len(df['Địa điểm'].unique())

st.markdown("""
<div class="stats-container">
    <div class="stats-card">
        <div class="stats-icon">💰</div>
        <div class="stats-value">{:,.0f} VNĐ</div>
        <div class="stats-label">Tổng chi phí</div>
    </div>
    <div class="stats-card">
        <div class="stats-icon">📍</div>
        <div class="stats-value">{}</div>
        <div class="stats-label">Địa điểm</div>
    </div>
    <div class="stats-card">
        <div class="stats-icon">✨</div>
        <div class="stats-value">{}</div>
        <div class="stats-label">Hoạt động</div>
    </div>
</div>
""".format(total_cost, unique_locations, total_activities), unsafe_allow_html=True)

# Timeline View
st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
st.markdown('<h2>🗓️ Lịch trình theo thời gian</h2>', unsafe_allow_html=True)

current_day = None
for _, row in df.iterrows():
    if current_day != row['Ngày']:
        current_day = row['Ngày']
        st.markdown(f'<h3 style="margin-top: 2rem;">{current_day}</h3>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="timeline-item">
        <div class="timeline-time">{row['Thời gian']}</div>
        <div class="timeline-content">
            <h4>{row['Icon']} {row['Hoạt động']}</h4>
            <p>📍 {row['Địa điểm']}</p>
            <p>💰 {row['Chi phí (VNĐ)']:,} VNĐ</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Cost Breakdown
st.markdown('<div class="cost-breakdown">', unsafe_allow_html=True)
st.markdown('<h2>💰 Chi tiết chi phí</h2>', unsafe_allow_html=True)

# Create a pie chart for cost breakdown
cost_by_type = df.groupby('Loại')['Chi phí (VNĐ)'].sum()
fig = px.pie(
    values=cost_by_type.values,
    names=cost_by_type.index,
    title='Phân bổ chi phí theo loại hoạt động',
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Detailed cost breakdown table
for category, cost in cost_by_type.items():
    st.markdown(f"""
    <div class="cost-item">
        <div class="cost-category">
            <span style="font-size: 1.5rem;">{schedule_data['Icon'][list(df['Loại']).index(category)]}</span>
            <span>{category}</span>
        </div>
        <div class="cost-value">{cost:,.0f} VNĐ</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Weather Forecast (Sample data - in practice, this would come from a weather API)
st.markdown('<div class="weather-widget">', unsafe_allow_html=True)
st.markdown("""
<h3>Dự báo thời tiết</h3>
<div class="weather-icon">⛅</div>
<div style="font-size: 1.5rem; margin: 0.5rem 0;">25°C</div>
<p>Có mây, khả năng mưa 20%</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interactive Map Preview
st.markdown('<div class="activity-card">', unsafe_allow_html=True)
st.markdown('<h2>🗺️ Bản đồ lịch trình</h2>', unsafe_allow_html=True)

# Sample map data
locations = pd.DataFrame({
    'lat': [21.0285, 21.0359, 21.0288],
    'lon': [105.8542, 105.8471, 105.8433],
    'name': ['Văn Miếu', 'Hoàng thành', 'Chùa Một Cột']
})

fig = px.scatter_mapbox(
    locations,
    lat='lat',
    lon='lon',
    hover_name='name',
    zoom=13
)

fig.update_layout(
    mapbox_style='carto-positron',
    height=400,
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Export Options
st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <button class="custom-button" style="background: var(--primary);">
        📱 Chia sẻ lịch trình
    </button>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <button class="custom-button" style="background: var(--success);">
        📄 Xuất PDF
    </button>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <button class="custom-button" style="background: var(--secondary);">
        📅 Thêm vào lịch
    </button>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with helpful tips
st.markdown("""
<div style="background: white; padding: 2rem; border-radius: 16px; margin-top: 3rem; text-align: center;">
    <h3>💡 Mẹo hữu ích</h3>
    <ul style="list-style: none; padding: 0;">
        <li>👉 Nhấp vào từng hoạt động để xem chi tiết</li>
        <li>👉 Kéo và thả để điều chỉnh thứ tự hoạt động</li>
        <li>👉 Sử dụng nút chia sẻ để gửi lịch trình cho bạn bè</li>
    </ul>
</div>
""", unsafe_allow_html=True) 