import streamlit as st
import pandas as pd

# Cấu hình giao diện trang
st.set_page_config(
    page_title="Tính Lãi Suất Tiết Kiệm",
    page_icon="🏦",
    layout="centered"
)

st.title("💰 Ứng dụng Tính Lãi Gửi Tiết Kiệm _ ĐỖ THỊ TÂM ANH 🐥🦅🦉🐝")
st.write("Nhập thông tin khoản tiền gửi bên dưới để tính toán chi tiết tiền lãi định kỳ, tổng tiền lãi và tổng số tiền nhận được💗🚓🤼‍♂️.")

# Form nhập liệu
with st.form("savings_form"):
    st.subheader("📝 Thông tin khoản gửi")
    
    col1, col2 = st.columns(2)
    with col1:
        principal = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=0,
            value=50000000,
            step=1000000,
            format="%d"
        )
        term_months = st.number_input(
            "Kỳ hạn gửi (tháng)",
            min_value=1,
            max_value=360,
            value=12,
            step=1
        )
    
    with col2:
        annual_rate = st.number_input(
            "Lãi suất (%/năm)",
            min_value=0.0,
            max_value=50.0,
            value=6.5,
            step=0.1
        )
        payment_method = st.selectbox(
            "Hình thức nhận lãi",
            ["Cuối kỳ", "Hàng tháng", "Hàng quý"]
        )
    
    submitted = st.form_submit_button("🧮 Tính toán ngay", use_container_width=True)

# Xử lý khi người dùng bấm nút tính toán
if submitted:
    # Tính toán cơ bản
    rate_monthly = (annual_rate / 100) / 12
    total_interest = 0
    periodic_interest = 0
    
    if payment_method == "Cuối kỳ":
        total_interest = principal * (annual_rate / 100) * (term_months / 12)
        periodic_interest = total_interest
    elif payment_method == "Hàng tháng":
        periodic_interest = principal * rate_monthly
        total_interest = periodic_interest * term_months
    elif payment_method == "Hàng quý":
        periodic_interest = principal * (annual_rate / 100) * (3 / 12)
        num_quarters = term_months / 3
        total_interest = periodic_interest * num_quarters

    total_amount = principal + total_interest

    # Hiển thị kết quả tổng quan
    st.markdown("---")
    st.subheader("📊 Kết quả tính toán")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        if payment_method == "Cuối kỳ":
            st.metric("Tiền lãi (Cuối kỳ)", f"{total_interest:,.0f} VNĐ")
        elif payment_method == "Hàng tháng":
            st.metric("Tiền lãi định kỳ (Tháng)", f"{periodic_interest:,.0f} VNĐ")
        else:
            st.metric("Tiền lãi định kỳ (Quý)", f"{periodic_interest:,.0f} VNĐ")
            
    with res_col2:
        st.metric("Tổng tiền lãi", f"{total_interest:,.0f} VNĐ")
        
    with res_col3:
        st.metric("Tổng gốc & lãi", f"{total_amount:,.0f} VNĐ")

    # Hiển thị chi tiết lịch nhận lãi
    st.markdown("---")
    st.subheader("📅 Chi tiết lịch nhận lãi")
    
    if payment_method == "Hàng tháng":
        data = []
        for i in range(1, term_months + 1):
            data.append({
                "Kỳ hạn": f"Tháng {i}",
                "Tiền lãi nhận được 💥 (VNĐ)": f"{periodic_interest:,.0f}",
                "Số dư gốc (VNĐ)": f"{principal:,.0f}"
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
    elif payment_method == "Hàng quý":
        data = []
        num_quarters = int(term_months // 3)
        remainder_months = term_months % 3
        for i in range(1, num_quarters + 1):
            data.append({
                "Kỳ hạn": f"Quý {i}",
                "Tiền lãi nhận được 🌻 (VNĐ)": f"{periodic_interest:,.0f}",
                "Số dư gốc (VNĐ)": f"{principal:,.0f}"
            })
        if remainder_months > 0:
            rem_interest = principal * (annual_rate / 100) * (remainder_months / 12)
            data.append({
                "Kỳ hạn": f"Tháng lẻ cuối ({remainder_months} tháng)",
                "Tiền lãi nhận được ❤️‍🩹 (VNĐ)": f"{rem_interest:,.0f}",
                "Số dư gốc (VNĐ)": f"{principal:,.0f}"
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info(f"💡 Với hình thức nhận lãi **Cuối kỳ**, bạn sẽ nhận toàn bộ số tiền lãi **{total_interest:,.0f} VNĐ** cộng với tiền gốc **{principal:,.0f} VNĐ** một lần duy nhất vào cuối kỳ hạn ({term_months} tháng).")
