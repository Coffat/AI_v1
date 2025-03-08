import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import os
import json
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Tạo lịch trình - Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define common data
interests_data = {
    "Văn hóa": {
        "icon": "🏛️",
        "description": "Khám phá di sản văn hóa, bảo tàng, và nghệ thuật truyền thống",
        "related_destinations": ["Hà Nội", "Huế", "Hội An"]
    },
    "Ẩm thực": {
        "icon": "🍜",
        "description": "Thưởng thức các món ăn đặc sản và khám phá văn hóa ẩm thực",
        "related_destinations": ["Hà Nội", "Huế", "Đà Nẵng", "Hội An"]
    },
    "Thiên nhiên": {
        "icon": "🌳",
        "description": "Tham quan công viên, vườn quốc gia và cảnh quan thiên nhiên",
        "related_destinations": ["Sapa", "Hạ Long", "Đà Lạt"]
    },
    "Lịch sử": {
        "icon": "🏺",
        "description": "Tìm hiểu về lịch sử địa phương qua các di tích và bảo tàng",
        "related_destinations": ["Hà Nội", "Huế", "Hội An"]
    },
    "Mua sắm": {
        "icon": "🛍️",
        "description": "Khám phá các khu mua sắm, chợ truyền thống và cửa hàng đặc sản",
        "related_destinations": ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng"]
    },
    "Biển": {
        "icon": "🏖️",
        "description": "Tắm biển, thư giãn trên bãi cát và các hoạt động dưới nước",
        "related_destinations": ["Hạ Long", "Đà Nẵng", "Nha Trang", "Phú Quốc"]
    }
}

# Enhanced destinations data
destinations_data = {
    "Hà Nội": {
        "image": "https://i.imgur.com/8DZuLtU.jpg",
        "description": "Thủ đô nghìn năm văn hiến",
        "region": "Miền Bắc",
        "highlights": ["Phố cổ", "Văn Miếu", "Hồ Gươm"],
        "min_days": 2,
        "suggested_days": 3,
        "base_cost_per_day": 1000000
    },
    "Hạ Long": {
        "image": "https://i.imgur.com/3R2Qj5K.jpg",
        "description": "Di sản thiên nhiên thế giới",
        "region": "Miền Bắc",
        "highlights": ["Vịnh Hạ Long", "Hang Sửng Sốt", "Đảo Titop"],
        "min_days": 2,
        "suggested_days": 3,
        "base_cost_per_day": 1500000
    },
    "Sapa": {
        "image": "https://i.imgur.com/6mTTNmP.jpg",
        "description": "Thị trấn trong mây",
        "region": "Miền Bắc",
        "highlights": ["Bản Cát Cát", "Fansipan", "Ruộng bậc thang"],
        "min_days": 2,
        "suggested_days": 3,
        "base_cost_per_day": 1200000
    },
    "Huế": {
        "image": "https://i.imgur.com/0XtHYh3.jpg",
        "description": "Cố đô di sản",
        "region": "Miền Trung",
        "highlights": ["Đại Nội", "Chùa Thiên Mụ", "Lăng Tự Đức"],
        "min_days": 2,
        "suggested_days": 2,
        "base_cost_per_day": 1000000
    },
    "Đà Nẵng": {
        "image": "https://i.imgur.com/8KZyaLV.jpg",
        "description": "Thành phố đáng sống",
        "region": "Miền Trung",
        "highlights": ["Bà Nà Hills", "Cầu Rồng", "Bãi biển Mỹ Khê"],
        "min_days": 3,
        "suggested_days": 4,
        "base_cost_per_day": 1300000
    }
}

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
    /* Modern Travel Theme Color Scheme */
    :root {
        --primary: #00b4d8;
        --primary-light: #90e0ef;
        --primary-dark: #0077b6;
        --primary-gradient: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%);
        
        --secondary: #ff9e00;
        --secondary-light: #ffb700;
        --secondary-dark: #ff7b00;
        --secondary-gradient: linear-gradient(135deg, #ff9e00 0%, #ff7b00 100%);
        
        --accent: #ff006e;
        --accent-light: #ff4d8d;
        --accent-dark: #cc0058;
        --accent-gradient: linear-gradient(135deg, #ff006e 0%, #cc0058 100%);
        
        --success: #06d6a0;
        --success-light: #29e7b6;
        --success-dark: #05a37a;
        
        --background: #f8f9fa;
        --surface: #ffffff;
        --text: #2b2d42;
        --text-light: #6c757d;
        
        --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    /* Enhanced Animations */
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #f0f7ff 0%, #ffffff 100%);
    }

    /* Travel-themed Header */
    .travel-header {
        text-align: center;
        padding: 4rem 2rem;
        background: url('https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=2000&q=80') center/cover;
        position: relative;
        border-radius: 24px;
        overflow: hidden;
        margin-bottom: 3rem;
    }

    .travel-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.7) 100%);
        z-index: 1;
    }

    .travel-header-content {
        position: relative;
        z-index: 2;
        color: white;
    }

    .travel-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: float 6s ease-in-out infinite;
    }

    .travel-subtitle {
        font-size: 1.25rem;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    /* Step Navigation */
    .step-nav {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: var(--surface);
        border-radius: 16px;
        box-shadow: var(--shadow-lg);
    }

    .step-indicator {
        display: flex;
        align-items: center;
        font-size: 1.1rem;
        color: var(--text);
        margin-right: auto;
    }

    .step-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }

    /* Form Card */
    .form-card {
        background: var(--surface);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: var(--shadow-lg);
        margin-bottom: 2rem;
        animation: slideUp 0.5s ease-out;
    }

    /* Enhanced Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background: var(--background);
        border: 2px solid transparent;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 4px rgba(0, 180, 216, 0.1);
        transform: translateY(-2px);
    }

    /* Interest Cards */
    .interest-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        box-shadow: var(--shadow-sm);
    }

    .interest-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-md);
    }

    .interest-card.selected {
        border-color: var(--primary);
        background: linear-gradient(to right, rgba(0, 180, 216, 0.1), transparent);
    }

    .interest-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    /* Destination Cards */
    .destination-card {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        background: var(--surface);
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
        height: 100%;
    }

    .destination-card:hover {
        transform: translateY(-10px);
        box-shadow: var(--shadow-xl);
    }

    .destination-image {
        height: 240px;
        position: relative;
    }

    .destination-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }

    .destination-card:hover .destination-image img {
        transform: scale(1.1);
    }

    .destination-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 2rem;
        background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
        color: white;
    }

    .destination-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .destination-info {
        padding: 1.5rem;
    }

    .destination-highlights {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .highlight-tag {
        background: var(--primary-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 999px;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    /* Summary Card */
    .summary-card {
        background: var(--surface);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: var(--shadow-lg);
    }

    .summary-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .summary-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 1rem;
    }

    .summary-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.25rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .summary-item:hover {
        background: var(--background);
        transform: translateX(10px);
        border-radius: 12px;
    }

    .summary-label {
        color: var(--text-light);
        font-weight: 500;
    }

    .summary-value {
        color: var(--text);
        font-weight: 600;
    }

    /* Enhanced Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Alert Styles */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: var(--shadow-md) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.form_data = {
        'start_location': '',
        'end_location': '',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=7)).date(),
        'num_travelers': 1,
        'budget': 5000000,
        'destinations': [],
        'interests': [],
        'suggested_destinations': []
    }

# Header
st.markdown("""
<div class="travel-header">
    <div class="travel-header-content">
        <h1 class="travel-title">✈️ Khám phá Việt Nam</h1>
        <p class="travel-subtitle">Tạo lịch trình du lịch độc đáo và phù hợp với sở thích của bạn</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Step Navigation
step_icons = ["📝", "💫", "🗺️", "✨"]
step_names = ["Thông tin cơ bản", "Sở thích", "Điểm đến", "Xác nhận"]
current_step = step_names[st.session_state.step - 1]
current_icon = step_icons[st.session_state.step - 1]

st.markdown(f"""
<div class="step-nav">
    <div class="step-indicator">
        <span class="step-icon">{current_icon}</span>
        <span>Bước {st.session_state.step}: {current_step}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Step 1: Basic Information
if st.session_state.step == 1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        start_location = st.text_input("Điểm xuất phát", 
                                     value=st.session_state.form_data['start_location'],
                                     placeholder="Ví dụ: Hà Nội")
        
        start_date = st.date_input("Ngày bắt đầu", 
                                 value=st.session_state.form_data['start_date'],
                                 min_value=datetime.now().date())
        
        num_travelers = st.number_input("Số người", 
                                      min_value=1, 
                                      value=st.session_state.form_data['num_travelers'])
    
    with col2:
        end_location = st.text_input("Điểm kết thúc", 
                                   value=st.session_state.form_data['end_location'],
                                   placeholder="Ví dụ: Hồ Chí Minh")
        
        end_date = st.date_input("Ngày kết thúc", 
                               value=st.session_state.form_data['end_date'],
                               min_value=start_date)
        
        budget = st.number_input("Ngân sách (VNĐ)", 
                               min_value=1000000, 
                               value=st.session_state.form_data['budget'],
                               step=1000000,
                               format="%d")

    # Validation
    is_valid = all([
        start_location,
        end_location,
        start_date <= end_date,
        num_travelers > 0,
        budget >= 1000000
    ])

    if not is_valid:
        st.warning("Vui lòng điền đầy đủ thông tin để tiếp tục")

    if st.button("Tiếp tục", disabled=not is_valid, type="primary", use_container_width=True):
        st.session_state.form_data.update({
            'start_location': start_location,
            'end_location': end_location,
            'start_date': start_date,
            'end_date': end_date,
            'num_travelers': num_travelers,
            'budget': budget
        })
        st.session_state.step = 2
        st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Interests
elif st.session_state.step == 2:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    selected_interests = []
    for interest, data in interests_data.items():
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            selected = st.checkbox("", value=interest in st.session_state.form_data['interests'])
            if selected:
                selected_interests.append(interest)
        with col2:
            st.markdown(f"""
            <div class="interest-card {'selected' if selected else ''}">
                <span class="interest-icon">{data['icon']}</span>
                <div>
                    <div style="font-weight: 600;">{interest}</div>
                    <div style="color: var(--text-light); font-size: 0.9rem;">{data['description']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Update suggested destinations based on interests
    suggested_destinations = set()
    for interest in selected_interests:
        suggested_destinations.update(interests_data[interest]['related_destinations'])
    st.session_state.form_data['suggested_destinations'] = list(suggested_destinations)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Quay lại", use_container_width=True):
            st.session_state.step = 1
            st.experimental_rerun()
    
    with col2:
        if st.button("Tiếp tục ➡️", disabled=len(selected_interests) == 0, use_container_width=True):
            st.session_state.form_data['interests'] = selected_interests
            st.session_state.step = 3
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Destinations
elif st.session_state.step == 3:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    # Filter destinations by region
    regions = ["Tất cả", "Miền Bắc", "Miền Trung", "Miền Nam"]
    selected_region = st.selectbox("Chọn khu vực", regions)
    
    filtered_destinations = destinations_data
    if selected_region != "Tất cả":
        filtered_destinations = {k: v for k, v in destinations_data.items() 
                              if v["region"] == selected_region}
    
    # Show suggested destinations first
    suggested = st.session_state.form_data['suggested_destinations']
    if suggested:
        st.markdown("""
        <div style="margin: 1rem 0;">
            <h3>🎯 Gợi ý điểm đến phù hợp với sở thích của bạn:</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
        """, unsafe_allow_html=True)
        
        for dest in suggested:
            if dest in filtered_destinations:
                st.markdown(f"""
                <span class="highlight-tag">{dest}</span>
                """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Display destinations as cards
    cols = st.columns(3)
    selected_destinations = []
    
    for i, (dest, data) in enumerate(filtered_destinations.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="destination-card">
                <div class="destination-image">
                    <img src="{data['image']}" alt="{dest}">
                </div>
                <div class="destination-overlay">
                    <h3 class="destination-title">{dest}</h3>
                    <p class="destination-description">{data['description']}</p>
                    <div class="destination-highlights">
                        {' '.join(f'<span class="highlight-tag">{highlight}</span>' for highlight in data['highlights'])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.checkbox(f"Chọn {dest}", value=dest in st.session_state.form_data['destinations']):
                selected_destinations.append(dest)
    
    # Calculate estimated duration and cost
    if selected_destinations:
        total_min_days = sum(destinations_data[d]['min_days'] for d in selected_destinations)
        total_suggested_days = sum(destinations_data[d]['suggested_days'] for d in selected_destinations)
        total_cost = sum(destinations_data[d]['base_cost_per_day'] for d in selected_destinations)
        
        st.info(f"""
        ⏱️ Thời gian đề xuất: {total_min_days}-{total_suggested_days} ngày
        💰 Chi phí ước tính: {total_cost:,} VNĐ/ngày/người
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Quay lại", use_container_width=True):
            st.session_state.step = 2
            st.experimental_rerun()
    
    with col2:
        if st.button("Tiếp tục ➡️", disabled=len(selected_destinations) == 0, use_container_width=True):
            st.session_state.form_data['destinations'] = selected_destinations
            st.session_state.step = 4
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Step 4: Confirmation
elif st.session_state.step == 4:
    st.markdown("""
    <div class="summary-card">
        <div class="summary-header">
            <h2 class="summary-title">✨ Xác nhận thông tin chuyến đi</h2>
            <p>Hãy kiểm tra lại thông tin trước khi tạo lịch trình</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate trip duration and total cost
    trip_days = (st.session_state.form_data['end_date'] - st.session_state.form_data['start_date']).days + 1
    total_cost = sum(destinations_data[d]['base_cost_per_day'] for d in st.session_state.form_data['destinations'])
    total_cost *= trip_days * st.session_state.form_data['num_travelers']
    
    # Display summary
    summary_items = [
        ("Điểm xuất phát", st.session_state.form_data['start_location']),
        ("Điểm kết thúc", st.session_state.form_data['end_location']),
        ("Thời gian", f"{trip_days} ngày ({st.session_state.form_data['start_date'].strftime('%d/%m/%Y')} - {st.session_state.form_data['end_date'].strftime('%d/%m/%Y')})"),
        ("Số người", f"{st.session_state.form_data['num_travelers']} người"),
        ("Ngân sách", f"{st.session_state.form_data['budget']:,} VNĐ"),
        ("Chi phí ước tính", f"{total_cost:,} VNĐ"),
        ("Điểm đến", ", ".join(st.session_state.form_data['destinations'])),
        ("Sở thích", ", ".join(f"{interests_data[i]['icon']} {i}" for i in st.session_state.form_data['interests']))
    ]
    
    for label, value in summary_items:
        st.markdown(f"""
        <div class="summary-item">
            <span class="summary-label">{label}</span>
            <span class="summary-value">{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Budget warning
    if total_cost > st.session_state.form_data['budget']:
        st.warning(f"""
        ⚠️ Chi phí ước tính ({total_cost:,} VNĐ) vượt quá ngân sách của bạn ({st.session_state.form_data['budget']:,} VNĐ).
        Bạn có thể cân nhắc:
        - Giảm số ngày du lịch
        - Chọn ít điểm đến hơn
        - Tăng ngân sách
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Quay lại", use_container_width=True):
            st.session_state.step = 3
            st.experimental_rerun()
    
    with col2:
        if st.button("✨ Tạo lịch trình", type="primary", use_container_width=True):
            with st.spinner("Đang tạo lịch trình..."):
                # Save data for next page
                st.session_state.itinerary_data = st.session_state.form_data
                st.success("Đã tạo lịch trình thành công!")
                st.switch_page("pages/schedule_view.py")

    st.markdown('</div>', unsafe_allow_html=True)
