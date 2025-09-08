import streamlit as st
import pandas as pd

def has_common_substring(str1, str2, length=4):
    if not isinstance(str1, str) or not isinstance(str2, str):
        return False
    for i in range(len(str1) - length + 1):
        if str1[i:i+length] in str2:
            return True
    return False

def fuzzy_match_items(df1, df2, column, length=4):
    matches = []
    for i, val1 in enumerate(df1[column]):
        for j, val2 in enumerate(df2[column]):
            if has_common_substring(val1, val2, length):
                matches.append({
                    "資料表1索引": i,
                    "資料表1品項": val1,
                    "資料表2索引": j,
                    "資料表2品項": val2
                })
    return pd.DataFrame(matches)

st.title("🧠 商品資料模糊比對工具")
st.markdown("上傳兩份 Excel 或 CSV，系統會比對指定欄位中『連續四字』以上相同的品項。")

file1 = st.file_uploader("📄 上傳資料表1", type=["xlsx", "csv"])
file2 = st.file_uploader("📄 上傳資料表2", type=["xlsx", "csv"])

if file1 and file2:
    df1 = pd.read_excel(file1) if file1.name.endswith(".xlsx") else pd.read_csv(file1)
    df2 = pd.read_excel(file2) if file2.name.endswith(".xlsx") else pd.read_csv(file2)

    column = st.selectbox("🧩 選擇要比對的欄位", options=df1.columns.intersection(df2.columns))
    length = st.slider("🔍 比對幾個字視為重複？", 2, 10, 4)

    if st.button("🚀 開始比對"):
        result = fuzzy_match_items(df1, df2, column=column, length=length)
        st.success(f"比對完成，共找到 {len(result)} 組可能重複品項")
        st.dataframe(result)

        csv = result.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載比對結果 CSV", data=csv, file_name="fuzzy_match_result.csv", mime="text/csv")
