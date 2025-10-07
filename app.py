import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from io import BytesIO

# -------------------------
# 🤖 Offline (Hardcoded) Dataset Type Detection
# -------------------------
def detect_dataset_type_offline(df):
    cols = [c.lower() for c in df.columns]

    if any(k in cols for k in ["employee", "salary", "age", "department", "job", "position", "hr"]):
        return "👨‍💼 Employee / HR Data"

    elif any(k in cols for k in ["car", "model", "engine", "speed", "mileage", "vehicle", "fuel"]):
        return "🚗 Car / Vehicle Data"

    elif any(k in cols for k in ["product", "item", "price", "category", "stock", "sales"]):
        return "🛍️ Product / Sales Data"

    elif any(k in cols for k in ["student", "class", "grade", "marks", "school", "university", "course"]):
        return "🎓 Student / Education Data"

    elif any(k in cols for k in ["date", "temperature", "humidity", "weather", "rainfall", "climate"]):
        return "🌦️ Weather / Climate Data"

    elif any(k in cols for k in ["country", "city", "region", "population", "area", "continent"]):
        return "🌍 Geographic / Demographic Data"

    else:
        return "❓ Unknown / Miscellaneous Data"


# -------------------------
# 🌐 Streamlit UI
# -------------------------
st.set_page_config(page_title="Offline Data Normalizer", page_icon="🤖", layout="wide")

st.title("🤖 Offline Smart Data Normalizer Web App")
st.write("Upload a CSV or Excel file — App will detect dataset type and normalize numeric columns automatically (no AI key needed).")

# File upload
uploaded_file = st.file_uploader("📤 Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Detect file type and read
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Show dataset preview
    st.subheader("📊 Original Data Preview")
    st.dataframe(df.head())

    # Detect dataset type (Offline)
    dataset_type = detect_dataset_type_offline(df)
    st.success(f"**Detected Dataset Type:** {dataset_type}")

    # Normalization method selection
    method = st.selectbox("🔧 Choose normalization method", ["Min-Max", "Standard"])
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    st.write(f"Detected numeric columns: `{numeric_cols}`")

    # Normalize button
    if st.button("🚀 Normalize Data"):
        if not numeric_cols:
            st.warning("No numeric columns found to normalize.")
        else:
            scaler = MinMaxScaler() if method == "Min-Max" else StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

            st.success("✅ Data normalized successfully!")
            st.subheader("📈 Normalized Data Preview")
            st.dataframe(df.head())

            # Export normalized data
            if uploaded_file.name.endswith(".csv"):
                output_file = "normalized_data.csv"
                data_bytes = df.to_csv(index=False).encode("utf-8")
                mime_type = "text/csv"
            else:
                output_file = "normalized_data.xlsx"
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                data_bytes = buffer.getvalue()
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            st.download_button("📥 Download Normalized File", data_bytes, output_file, mime_type)

else:
    st.info("Please upload a CSV or Excel file to get started.")
