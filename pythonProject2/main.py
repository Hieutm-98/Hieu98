import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu từ tệp Excel
df_price = pd.read_excel("CCFEI morning_Hieu.xlsx")
df_supply_demand = pd.read_excel("Supply-Demand.xlsx")

# Tiêu đề của ứng dụng và mô tả
st.title("Chào mừng đến với App của Mr. Hiếu")
st.write(
    "Ứng dụng này bao gồm 02 trang, biểu diễn các dữ liệu về giá một số sản phẩm hóa dầu và cung cầu tại một số quốc gia trên thế giới. Nguồn thông tin được tác giả cập nhật từ CCFEI và REUTERS.")

# Sidebar để chọn trang
page = st.sidebar.radio("Chọn một trang để bắt đầu:", ["Giá", "Cung cầu", "Demo Power BI"])

# Trang "Giá"
if page == "Giá":
    st.header("Giá một số sản phẩm hóa dầu năm 2020 theo CCFEI")
    st.write(
        "CCFEI là mạng lưới tin tức về ngành xơ sợi và hóa chất tại Trung Quốc. CCFEI cung cấp thông tin về tình hình thị trường và giá cả các sản phẩm trong ngành xơ sợi và hóa chất tại nhiều thị trường trên thế giới. Dưới đây là một số thông tin về giá các sản phẩm hóa dầu theo một số thị trường và điều khoản vận chuyển cụ thể được cung cấp bởi CCFEI trong năm 2020:")

    # Lọc dữ liệu theo selectbox
    product_options = df_price["Products"].unique()
    selected_product = st.selectbox("Chọn sản phẩm:", product_options)

    available_terms = df_price[df_price["Products"] == selected_product]["Term"].unique()
    selected_terms = st.multiselect("Chọn điều khoản mua bán:", available_terms)

    filtered_df = df_price[(df_price["Products"] == selected_product) & (df_price["Term"].isin(selected_terms))]

    # Vẽ biểu đồ đường
    fig = px.line(filtered_df, x="Time", y="Prices", color="Products", line_shape="linear",
                  title=f"Giá {selected_product} theo CCFEI")
    st.plotly_chart(fig)

# Trang "Cung cầu"
elif page == "Cung cầu":
    st.header("Cung cầu một số sản phẩm hóa dầu tại một số quốc gia trên thế giới")
    st.write(
        "Dưới đây là một số thông tin về thị trường cung cầu các sản phẩm hóa dầu tại một số quốc gia cụ thể được cung cấp bởi REUTERS trong giai đoạn 2000 - 2020 và dự báo đến 2023:")

    # Lọc dữ liệu theo selectbox
    product_options = df_supply_demand["Product"].unique()
    selected_product = st.selectbox("Chọn sản phẩm:", product_options)

    value_options = ["Import", "Production", "Export", "Demand"]
    selected_value = st.selectbox("Chọn giá trị (Nhập khẩu, Sản xuất, Xuất khẩu, Tiêu thụ):", value_options)

    available_countries = df_supply_demand[df_supply_demand["Product"] == selected_product]["Country"].unique()
    selected_countries = st.multiselect("Chọn quốc gia:", available_countries)

    filtered_df = df_supply_demand[
        (df_supply_demand["Product"] == selected_product) & (df_supply_demand["Country"].isin(selected_countries))]

    # Vẽ biểu đồ cột
    fig_bar = px.bar(filtered_df, x="Year", y=selected_value, color="Country",
                     title=f"{selected_value} {selected_product} theo quốc gia")
    st.plotly_chart(fig_bar)

    # Vẽ biểu đồ map
    st.subheader("Biểu đồ Map")

    # Lọc dữ liệu cho biểu đồ Map
    year_options = df_supply_demand["Year"].unique()
    selected_year = st.selectbox("Chọn Năm:", year_options)

    filtered_map_df = filtered_df[filtered_df["Year"] == selected_year]

    # Tạo thông tin cho tooltip trên biểu đồ Map
    tooltip_data = [f"{country}<br>{selected_value}: {value:.2f} (triệu tấn)" for country, value in
                    zip(filtered_map_df['Country'], filtered_map_df[selected_value])]

    # Thêm cột mới "Tooltip" vào DataFrame
    filtered_map_df["Tooltip"] = tooltip_data

    # Vẽ biểu đồ Map
    fig_map = px.choropleth(filtered_map_df, locations="Country", locationmode="country names",
                            color=selected_value,
                            custom_data=["Tooltip"],
                            title=f"{selected_value} {selected_product} theo quốc gia",
                            color_continuous_scale=px.colors.sequential.Plasma,
                            template="plotly")

    # Định dạng tooltip
    fig_map.update_traces(hovertemplate='%{customdata[0]}')

    st.plotly_chart(fig_map)

elif page == "Demo Power BI":

    st.title('Demo Báo cáo Power BI trong ứng dụng Streamlit')

    # Nhúng mã nhúng Power BI vào ứng dụng
    st.markdown('<iframe title="csdl da lng" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiMDhjYzFhNWEtZDNlZC00YTM4LWI1MjItZmZlYzdlN2FhOWZmIiwidCI6ImM1ZWM1YWJlLTc2YzEtNDZjYi1iM2ZlLWMzYjAwNzFmZmRiMyIsImMiOjEwfQ%3D%3D" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)