import streamlit as st
st.image("logo.jpg")
import pandas as pd

# Cấu hình giao diện trang
st.set_page_config(
    page_title="Tính Lãi Suất Tiết Kiệm Đa Ngân Hàng",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Ứng dụng Tính Lãi Gửi Tiết Kiệm & Biểu Lãi Suất Ngân Hàng")
st.write("Chọn ngân hàng ngay từ lúc đầu để xem biểu lãi suất tương ứng, sau đó nhập thông tin khoản gửi để tính toán chi tiết.")

# Dữ liệu biểu lãi suất của các ngân hàng mẫu
banks_data = {
    "Vietcombank": {
        "Kỳ hạn": ["1 tháng", "3 tháng", "6 tháng", "9 tháng", "12 tháng", "24 tháng", "36 tháng"],
        "Số tháng": [1, 3, 6, 9, 12, 24, 36],
        "Lãi suất (%/năm)": [3.0, 3.3, 4.5, 4.5, 5.5, 5.5, 5.5]
    },
    "BIDV": {
        "Kỳ hạn": ["1 tháng", "3 tháng", "6 tháng", "9 tháng", "12 tháng", "24 tháng", "36 tháng"],
        "Số tháng": [1, 3, 6, 9, 12, 24, 36],
        "Lãi suất (%/năm)": [3.1, 3.4, 4.6, 4.6, 5.6, 5.6, 5.6]
    },
    "Techcombank": {
        "Kỳ hạn": ["1 tháng", "3 tháng", "6 tháng", "9 tháng", "12 tháng", "24 tháng", "36 tháng"],
        "Số tháng": [1, 3, 6, 9, 12, 24, 36],
        "Lãi suất (%/năm)": [3.2, 3.6, 4.8, 5.0, 5.8, 6.0, 6.0]
    },
    "MB Bank": {
        "Kỳ hạn": ["1 tháng", "3 tháng", "6 tháng", "9 tháng", "12 tháng", "24 tháng", "36 tháng"],
        "Số tháng": [1, 3, 6, 9, 12, 24, 36],
        "Lãi suất (%/năm)": [3.1, 3.5, 4.7, 4.9, 5.9, 6.1, 6.1]
    }
}

# --- PHẦN 1: CHỌN NGÂN HÀNG Ở LÚC ĐẦU ---
st.markdown("### 🏢 Bước 1: Chọn Ngân Hàng & Xem Biểu Lãi Suất")
selected_bank = st.selectbox("Chọn ngân hàng bạn muốn tham khảo:", list(banks_data.keys()))

# Lấy dữ liệu biểu lãi suất của ngân hàng được chọn
current_bank_dict = banks_data[selected_bank]
df_bank_rates = pd.DataFrame(current_bank_dict)

# Hiển thị bảng lãi suất của ngân hàng đó
st.dataframe(
    df_bank_rates[["Kỳ hạn", "Lãi suất (%/năm)"]], 
    use_container_width=True, 
    hide_index=True
)

st.markdown("---")

# --- PHẦN 2: NHẬP THÔNG TIN VÀ TÍNH TOÁN ---
st.markdown("### 🧮 Bước 2: Nhập Thông Tin Khoản Gửi & Tính Toán")

col_form, col_info = st.columns([1.2, 0.8])

with col_form:
    with st.form("savings_form"):
        principal = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=0,
            value=50000000,
            step=1000000,
            format="%d"
        )
        
        use_bank_rate = st.checkbox(f"Sử dụng lãi suất theo biểu của {selected_bank}", value=True)
        
        if use_bank_rate:
            term_options = dict(zip(df_bank_rates["Kỳ hạn"], df_bank_rates["Số tháng"]))
            selected_term_str = st.selectbox("Chọn kỳ hạn gửi", list(term_options.keys()))
            term_months = term_options[selected_term_str]
            annual_rate = float(df_bank_rates.loc[df_bank_rates["Kỳ hạn"] == selected_term_str, "Lãi suất (%/năm)"].values[0])
            st.success(f"👉 Lãi suất áp dụng: **{annual_rate}%/năm** cho kỳ hạn **{selected_term_str}**")
        else:
            term_months = st.number_input(
                "Kỳ hạn gửi (tháng)",
                min_value=1,
                max_value=360,
                value=12,
                step=1
            )
            annual_rate = st.number_input(
                "Lãi suất (%/năm)",
                min_value=0.0,
                max_value=50.0,
                value=5.5,
                step=0.1
            )
        
        payment_method = st.selectbox(
            "Hình thức nhận lãi",
            ["Cuối kỳ", "Hàng tháng", "Hàng quý"]
        )
        
        submitted = st.form_submit_button("🧮 Tính toán ngay", use_container_width=True)

with col_info:
    st.info(f"""
    📌 **Hướng dẫn:**
    - Ngân hàng đang chọn: **{selected_bank}**
    - Bạn có thể thay đổi ngân hàng ở phía trên bất cứ lúc nào để xem và so sánh mức lãi suất.
    - Hình thức nhận lãi hàng tháng hoặc hàng quý giúp bạn nhận dòng tiền đều đặn, trong khi cuối kỳ nhận trọn gói khi đáo hạn.
    """)

# Xử lý khi người dùng bấm nút tính toán
if submitted:
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

    st.markdown("---")
    st.subheader("📊 Kết quả tính toán chi tiết")
    
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

    st.markdown("---")
    st.subheader("📅 Lịch chi tiết nhận lãi")
    
    if payment_method == "Hàng tháng":
        data = []
        for i in range(1, term_months + 1):
            data.append({
                "Kỳ hạn": f"Tháng {i}",
                "Tiền lãi nhận được (VNĐ)": f"{periodic_interest:,.0f}",
                "Số dư gốc (VNĐ)": f"{principal:,.0f}"
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    elif payment_method == "Hàng quý":
        data = []
        num_quarters = int(term_months // 3)
        remainder_months = term_months % 3
        for i in range(1, num_quarters + 1):
            data.append({
                "Kỳ hạn": f"Quý {i}",
                "Tiền lãi nhận được (VNĐ)": f"{periodic_interest:,.0f}",
                "Số dư gốc (VNĐ)": f"{principal:,.0f}"
            })
        if remainder_months > 0:
            rem_interest = principal * (annual_rate / 100) * (remainder_months / 12)
            data.append({
                "Kỳ hạn": f"Tháng lẻ cuối ({remainder_months} tháng)",
                "Tiền lãi nhận được (VNĐ)": f"{rem_interest:,.0f}",
                "Số dư gốc (VNĐ)": f"{principal:,.0f}"
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    else:
        st.info(f"💡 Với hình thức nhận lãi **Cuối kỳ**, bạn sẽ nhận toàn bộ số tiền lãi **{total_interest:,.0f} VNĐ** cộng với tiền gốc **{principal:,.0f} VNĐ** một lần duy nhất vào cuối kỳ hạn ({term_months} tháng) tại ngân hàng **{selected_bank}**.")
