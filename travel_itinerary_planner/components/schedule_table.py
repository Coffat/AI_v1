import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

class ScheduleTable:
    def __init__(self):
        self.data = []
        self.columns = ['Thời gian', 'Hoạt động', 'Địa điểm', 'Ghi chú', 'Chi phí']
        
    def add_activity(self, time, activity, location, note='', cost=0):
        """Thêm một hoạt động vào lịch trình"""
        self.data.append({
            'Thời gian': time,
            'Hoạt động': activity,
            'Địa điểm': location,
            'Ghi chú': note,
            'Chi phí': cost
        })
        
    def create_sample_data(self):
        """Tạo dữ liệu mẫu"""
        current_time = datetime.now()
        activities = [
            ('08:00', 'Ăn sáng', 'Khách sạn', 'Buffet sáng', 150000),
            ('09:30', 'Tham quan', 'Địa điểm 1', 'Hướng dẫn viên', 200000),
            ('12:00', 'Ăn trưa', 'Nhà hàng', 'Set menu', 250000),
            ('14:00', 'Nghỉ ngơi', 'Khách sạn', 'Check-in', 0),
            ('16:00', 'Tham quan', 'Địa điểm 2', 'Tự do', 100000),
            ('19:00', 'Ăn tối', 'Nhà hàng', 'Đặt trước', 300000)
        ]
        
        for time, activity, location, note, cost in activities:
            self.add_activity(time, activity, location, note, cost)
            
    def render(self, show_total=True):
        """Hiển thị bảng lịch trình"""
        if not self.data:
            st.warning("Chưa có dữ liệu lịch trình")
            return
            
        # Tạo DataFrame
        df = pd.DataFrame(self.data)
        
        # Định dạng chi phí
        df['Chi phí'] = df['Chi phí'].apply(lambda x: f"{x:,.0f}đ" if x > 0 else "Miễn phí")
        
        # Tạo CSS cho bảng
        st.markdown("""
            <style>
                .schedule-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1rem 0;
                    background: white;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
                }
                .schedule-table th {
                    background: #f8f9fa;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                    color: #333;
                    border-bottom: 2px solid #dee2e6;
                }
                .schedule-table td {
                    padding: 12px;
                    border-bottom: 1px solid #dee2e6;
                    transition: background-color 0.3s;
                }
                .schedule-table tr:hover {
                    background-color: #f8f9fa;
                }
                .schedule-table .time-column {
                    font-weight: bold;
                    color: #007bff;
                }
                .schedule-table .activity-column {
                    color: #28a745;
                }
                .schedule-table .location-column {
                    color: #6c757d;
                }
                .schedule-table .cost-column {
                    text-align: right;
                    color: #dc3545;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Hiển thị bảng với định dạng
        st.markdown("""
            <table class="schedule-table">
                <tr>
                    <th>Thời gian</th>
                    <th>Hoạt động</th>
                    <th>Địa điểm</th>
                    <th>Ghi chú</th>
                    <th>Chi phí</th>
                </tr>
        """, unsafe_allow_html=True)
        
        for _, row in df.iterrows():
            st.markdown(f"""
                <tr>
                    <td class="time-column">{row['Thời gian']}</td>
                    <td class="activity-column">{row['Hoạt động']}</td>
                    <td class="location-column">{row['Địa điểm']}</td>
                    <td>{row['Ghi chú']}</td>
                    <td class="cost-column">{row['Chi phí']}</td>
                </tr>
            """, unsafe_allow_html=True)
            
        st.markdown("</table>", unsafe_allow_html=True)
        
        # Hiển thị tổng chi phí nếu được yêu cầu
        if show_total:
            total_cost = sum(float(str(cost).replace('đ', '').replace(',', '')) 
                           for cost in df['Chi phí'] if cost != 'Miễn phí')
            st.markdown(f"""
                <div style="text-align: right; margin-top: 1rem; font-weight: bold;">
                    Tổng chi phí: {total_cost:,.0f}đ
                </div>
            """, unsafe_allow_html=True)

def create_schedule_table(activities=None):
    """Hàm tiện ích để tạo bảng lịch trình"""
    schedule = ScheduleTable()
    
    if activities:
        for activity in activities:
            schedule.add_activity(*activity)
    else:
        schedule.create_sample_data()
        
    return schedule.render() 