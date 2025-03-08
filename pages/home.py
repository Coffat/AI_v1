import streamlit as st
import os
import base64

def show_home():
    # Cấu hình trang
    st.set_page_config(
        page_title="Home - Travel Planner",
        page_icon="🏠",
        layout="wide"
    )

    # Custom CSS
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Lấy thư mục hiện tại (pages)
    css_path = os.path.join(current_dir, 'assets', 'css', 'style.css')  # Tạo đường dẫn tuyệt đối
    video_path = os.path.join(current_dir, 'assets', 'images', 'home_vd.mp4')
    
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Không tìm thấy file CSS tại: {css_path}")

    # Video Section with autoplay
    with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()

    # Video section HTML
    st.markdown("""
        <div class="video-section">
            <video autoplay muted loop playsinline style="width:100%; height:100%; object-fit:cover; filter: brightness(0.7);">
                <source src="data:video/mp4;base64,{}" type="video/mp4">
            </video>
            <div class="overlay-content">
                <h1>Travel Planner</h1>
                <p>Khám phá Việt Nam một cách tối ưu với công cụ lập lịch trình thông minh</p>
                <div class="hero-buttons">
                    <a href="./input_form" class="btn btn-primary">BẮT ĐẦU NGAY</a>
                    <a href="#features" class="btn btn-outline">TÌM HIỂU THÊM</a>
                </div>
            </div>
        </div>
    """.format(base64.b64encode(video_bytes).decode()), unsafe_allow_html=True)

    # Add custom CSS for video section
    st.markdown("""
        <style>
            .video-section {
                position: relative;
                width: 100%;
                height: 100vh;
                margin-top: -80px;
                z-index: 2;
                overflow: hidden;
            }
            
            .overlay-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: white;
                width: 100%;
                max-width: 800px;
                padding: 2rem;
                z-index: 3;
            }
            
            .overlay-content h1 {
                font-size: 4.5rem;
                font-weight: 800;
                margin-bottom: 1.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                letter-spacing: -1px;
                line-height: 1.2;
            }
            
            .overlay-content p {
                font-size: 1.8rem;
                margin-bottom: 3rem;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                line-height: 1.5;
                font-weight: 400;
            }
            
            .hero-buttons {
                display: flex;
                gap: 2rem;
                justify-content: center;
            }
            
            .btn {
                padding: 1.2rem 3rem;
                font-size: 1.1rem;
                border-radius: 50px;
                text-decoration: none;
                transition: all 0.3s ease;
                font-weight: 700;
                letter-spacing: 1px;
            }
            
            .btn-primary {
                background: var(--primary-color);
                color: white;
                border: none;
            }
            
            .btn-primary:hover {
                background: var(--secondary-color);
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            }
            
            .btn-outline {
                background: transparent;
                color: white;
                border: 2px solid white;
            }
            
            .btn-outline:hover {
                background: white;
                color: var(--primary-color);
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            }

            @media (max-width: 768px) {
                .overlay-content {
                    top: 50%;
                    padding: 1rem;
                }
                
                .overlay-content h1 {
                    font-size: 3rem;
                }
                
                .overlay-content p {
                    font-size: 1.4rem;
                    margin-bottom: 2rem;
                }
                
                .hero-buttons {
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .btn {
                    width: 100%;
                    text-align: center;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <div id="features" class="features-section">
            <div class="section-header">
                <h2>Tại sao chọn Travel Planner?</h2>
                <p>Khám phá những lợi ích độc đáo của chúng tôi</p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3>Lộ trình tối ưu</h3>
                    <p>Tự động tạo lộ trình tối ưu dựa trên thời gian và chi phí</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⏰</div>
                    <h3>Tiết kiệm thời gian</h3>
                    <p>Không cần mất nhiều thời gian lên kế hoạch</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💰</div>
                    <h3>Tiết kiệm chi phí</h3>
                    <p>Dự toán chi phí chính xác và tối ưu</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎨</div>
                    <h3>Trải nghiệm cá nhân</h3>
                    <p>Lộ trình được tùy chỉnh theo sở thích</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add custom CSS for features section
    st.markdown("""
        <style>
            .features-section {
                padding: 6rem 2rem;
                background-color: var(--white);
            }
            
            .section-header {
                text-align: center;
                margin-bottom: 4rem;
            }
            
            .section-header h2 {
                font-size: 2.8rem;
                color: var(--primary-color);
                margin-bottom: 1rem;
                font-weight: 700;
            }
            
            .section-header p {
                font-size: 1.3rem;
                color: var(--text-color);
                opacity: 0.8;
            }
            
            .features-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 2.5rem;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .feature-card {
                background: white;
                padding: 2.5rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 5px 20px rgba(0,0,0,0.05);
                transition: all 0.3s ease;
                border: 1px solid rgba(0,0,0,0.05);
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                border-color: var(--primary-color);
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 1.5rem;
            }
            
            .feature-card h3 {
                font-size: 1.5rem;
                color: var(--primary-color);
                margin-bottom: 1rem;
                font-weight: 600;
            }
            
            .feature-card p {
                color: var(--text-color);
                line-height: 1.6;
                font-size: 1rem;
            }
            
            @media (max-width: 1200px) {
                .features-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
            
            @media (max-width: 768px) {
                .features-section {
                    padding: 4rem 1rem;
                }
                
                .section-header h2 {
                    font-size: 2.2rem;
                }
                
                .features-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # Popular Destinations Section
    st.markdown("""
        <div class="destinations-section">
            <div class="section-header">
                <h2>Điểm đến phổ biến</h2>
                <p>Khám phá những địa điểm du lịch nổi tiếng nhất Việt Nam</p>
            </div>
            <div class="destinations-grid">
    """, unsafe_allow_html=True)

    # Create three columns for destinations
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")

    with col1:
        st.markdown("""
            <div class="destination-card">
                <div class="image-container">
        """, unsafe_allow_html=True)
        st.image("pages/assets/images/hanoi.jpg", use_container_width=True)
        st.markdown("""
                </div>
                <div class="destination-content">
                    <h3>Hà Nội</h3>
                    <p>Thủ đô nghìn năm văn hiến</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="destination-card">
                <div class="image-container">
        """, unsafe_allow_html=True)
        st.image("pages/assets/images/hcmc.jpg", use_container_width=True)
        st.markdown("""
                </div>
                <div class="destination-content">
                    <h3>Hồ Chí Minh</h3>
                    <p>Thành phố không ngủ</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="destination-card">
                <div class="image-container">
        """, unsafe_allow_html=True)
        st.image("pages/assets/images/danang.jpg", use_container_width=True)
        st.markdown("""
                </div>
                <div class="destination-content">
                    <h3>Đà Nẵng</h3>
                    <p>Thành phố đáng sống</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add custom CSS for destinations section
    st.markdown("""
        <style>
            .destinations-section {
                padding: 0;
                background-color: #f8f9fa;
                margin: 0;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .section-header {
                text-align: center;
                padding: 0;
                margin-bottom: 2rem;
            }
            
            .section-header h2 {
                font-size: 2.5rem;
                color: var(--primary-color);
                margin: 0;
                padding: 0;
                font-weight: 700;
                line-height: 1.2;
            }
            
            .section-header p {
                font-size: 1.1rem;
                color: var(--text-color);
                opacity: 0.8;
                margin: 0.3rem 0 0 0;
                padding: 0;
                line-height: 1.2;
            }

            .destinations-grid {
                margin: 0;
                padding: 0 1rem;
            }

            .destination-card {
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                height: 250px;
                position: relative;
                margin: 0;
            }

            [data-testid="block-container"] {
                padding-top: 2rem !important;
                padding-bottom: 1rem !important;
                max-width: 100% !important;
            }

            [data-testid="stVerticalBlock"] {
                gap: 0 !important;
                padding: 0 !important;
            }

            [data-testid="stHorizontalBlock"] {
                gap: 1rem !important;
                padding: 0 1rem !important;
            }

            .destination-content {
                text-align: center;
                padding: 1rem;
                background: linear-gradient(transparent, rgba(0,0,0,0.8));
                color: white;
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                z-index: 1;
            }
            
            .destination-content h3 {
                font-size: 1.4rem;
                margin-bottom: 0.2rem;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                font-weight: 600;
            }
            
            .destination-content p {
                font-size: 0.95rem;
                opacity: 0.9;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                margin-bottom: 0;
            }
            
            @media (max-width: 768px) {
                .destinations-section {
                    padding: 1rem;
                }

                .section-header {
                    margin-bottom: 1.5rem;
                }

                .section-header h2 {
                    font-size: 2rem;
                }

                .section-header p {
                    font-size: 1rem;
                }

                .destination-card {
                    height: 200px;
                }

                .destination-content {
                    padding: 0.8rem;
                }

                .destination-content h3 {
                    font-size: 1.2rem;
                }

                .destination-content p {
                    font-size: 0.85rem;
                }

                [data-testid="stHorizontalBlock"] {
                    gap: 0.5rem !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_home()