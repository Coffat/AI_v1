import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

class ComparisonChart:
    def __init__(self):
        self.data = {}
        self.metrics = ['Thời gian chạy', 'Chi phí', 'Số node mở rộng']
        
    def add_algorithm_data(self, name, execution_time, cost, nodes_expanded):
        """Thêm dữ liệu cho một thuật toán"""
        self.data[name] = {
            'Thời gian chạy': execution_time,
            'Chi phí': cost,
            'Số node mở rộng': nodes_expanded
        }
        
    def create_sample_data(self):
        """Tạo dữ liệu mẫu"""
        sample_data = {
            'A*': {'Thời gian chạy': 0.5, 'Chi phí': 1500000, 'Số node mở rộng': 150},
            'Dijkstra': {'Thời gian chạy': 0.8, 'Chi phí': 1800000, 'Số node mở rộng': 200},
            'Greedy': {'Thời gian chạy': 0.3, 'Chi phí': 2000000, 'Số node mở rộng': 100},
            'Genetic': {'Thời gian chạy': 1.2, 'Chi phí': 1600000, 'Số node mở rộng': 80}
        }
        self.data = sample_data
        
    def render_bar_chart(self, metric):
        """Hiển thị biểu đồ cột cho một chỉ số"""
        if not self.data:
            st.warning("Chưa có dữ liệu so sánh")
            return
            
        # Chuẩn bị dữ liệu
        algorithms = list(self.data.keys())
        values = [self.data[algo][metric] for algo in algorithms]
        
        # Tạo biểu đồ
        fig = go.Figure(data=[
            go.Bar(
                x=algorithms,
                y=values,
                text=values,
                textposition='auto',
                marker_color='#007bff',
                opacity=0.8,
                hovertemplate=f"{metric}: %{{y}}<extra></extra>"
            )
        ])
        
        # Cập nhật layout
        fig.update_layout(
            title=f'So sánh {metric} giữa các thuật toán',
            xaxis_title='Thuật toán',
            yaxis_title=metric,
            showlegend=False,
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            template='plotly_white'
        )
        
        # Thêm animation
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}]
                        )
                    ]
                )
            ]
        )
        
        return fig
        
    def render_radar_chart(self):
        """Hiển thị biểu đồ radar so sánh tất cả các chỉ số"""
        if not self.data:
            st.warning("Chưa có dữ liệu so sánh")
            return
            
        # Chuẩn bị dữ liệu
        algorithms = list(self.data.keys())
        
        # Tạo biểu đồ radar
        fig = go.Figure()
        
        for algo in algorithms:
            values = [self.data[algo][metric] for metric in self.metrics]
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=self.metrics,
                fill='toself',
                name=algo
            ))
            
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max([max([self.data[algo][metric] for algo in algorithms]) 
                                 for metric in self.metrics])]
                )),
            showlegend=True,
            title='So sánh tổng thể giữa các thuật toán'
        )
        
        return fig
        
    def render_comparison(self):
        """Hiển thị tất cả các biểu đồ so sánh"""
        if not self.data:
            self.create_sample_data()
            
        # Tạo tabs cho các loại biểu đồ
        tab1, tab2 = st.tabs(["Biểu đồ cột", "Biểu đồ radar"])
        
        with tab1:
            st.subheader("So sánh chi tiết từng chỉ số")
            for metric in self.metrics:
                fig = self.render_bar_chart(metric)
                st.plotly_chart(fig, use_container_width=True)
                
        with tab2:
            st.subheader("So sánh tổng thể")
            fig = self.render_radar_chart()
            st.plotly_chart(fig, use_container_width=True)
            
        # Hiển thị bảng dữ liệu
        st.subheader("Dữ liệu chi tiết")
        df = pd.DataFrame(self.data).T
        st.dataframe(df.style.format({
            'Thời gian chạy': '{:.2f}s',
            'Chi phí': '{:,.0f}đ',
            'Số node mở rộng': '{:,.0f}'
        }))

def create_comparison_chart(algorithms_data=None):
    """Hàm tiện ích để tạo biểu đồ so sánh"""
    comparison = ComparisonChart()
    
    if algorithms_data:
        for name, data in algorithms_data.items():
            comparison.add_algorithm_data(name, **data)
    else:
        comparison.create_sample_data()
        
    return comparison.render_comparison() 