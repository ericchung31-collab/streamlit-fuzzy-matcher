import streamlit as st
import pandas as pd

def fuzzy_match_items(df1, df2, column, length=3):
    matched_items = []

    def has_common_substring(a, b, length):
        a, b = str(a), str(b)
        for i in range(len(a) - length + 1):
            substring = a[i:i+length]
            if substring in b:
                return substring
        return None

    for val1 in df1[column].astype(str):
        for val2 in df2[column].astype(str):
            match = has_common_substring(val1, val2, length)
            if match:
                matched_items.append({
                    f"df1_{column}": val1,
                    f"df2_{column}": val2,
                    "連續相同片段": match
                })

    return pd.DataFrame(matched_items)


# Streamlit App
st.set_page_config(page_title="模糊比對工具", layout="wide")
st.title("🔍 兩份資料欄位模糊比對工具")

file1 = st.file_uploader("上傳第一份 Excel 或 CSV 檔案", type=["xlsx", "csv"], key="file1")
file2 = st.file_uploader("上傳第二份 Excel 或 CSV 檔案", type=["xlsx", "csv"], key="file2")

if file1 and file2:
    def load_file(file):
        if file.name.endswith(".xlsx"):
            return pd.read_excel(file)
        elif file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            return None

    df1 = load_file(file1)
    df2 = load_file(file2)

    common_cols = list(set(df1.columns) & set(df2.columns))
    if not common_cols:
        st.error("❌ 兩份資料中沒有共同欄位，請確認資料格式一致")
    else:
        column = st.selectbox("選擇要比對的欄位", common_cols)
        length = st.slider("設定比對成功所需的相同字元數", 1, 10, 3)

        if st.button("開始比對"):
            with st.spinner("比對中，請稍候..."):
                result = fuzzy_match_items(df1, df2, column, length=length)

            st.success(f"✅ 比對完成，共有 {len(result)} 筆相似品項")
            st.dataframe(result)

            # 提供下載
            csv = result.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 下載比對結果（CSV）",
                data=csv,
                file_name="fuzzy_match_result.csv",
                mime="text/csv"
            )
