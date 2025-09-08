import streamlit as st
import pandas as pd

# --------------------
# 模糊比對函數
# --------------------
def fuzzy_match_items(df1, df2, col1, col2, length=4):
    matched_rows = []

    for i, val1 in enumerate(df1[col1]):
        for j, val2 in enumerate(df2[col2]):
            if isinstance(val1, str) and isinstance(val2, str):
                common_chars = set(val1) & set(val2)
                if len(common_chars) >= length:
                    matched_rows.append({
                        "df1_index": i,
                        "df2_index": j,
                        "df1_value": val1,
                        "df2_value": val2,
                        "相同字數": len(common_chars),
                        "共同字元": ''.join(common_chars),
                    })
    return pd.DataFrame(matched_rows)

# --------------------
# Streamlit 主介面
# --------------------
st.title("🔍 商品名稱模糊比對工具")
st.markdown("上傳兩份 Excel 或 CSV 檔案，選擇要比對的欄位，即可找出 **有共同字元** 的品項（最少 X 個字相同）。")

# 檔案上傳
file1 = st.file_uploader("📁 上傳第一份資料", type=["xlsx", "csv"], key="file1")
file2 = st.file_uploader("📁 上傳第二份資料", type=["xlsx", "csv"], key="file2")

if file1 and file2:
    try:
        # 自動偵測格式
        df1 = pd.read_excel(file1, engine="openpyxl") if file1.name.endswith(".xlsx") else pd.read_csv(file1)
        df2 = pd.read_excel(file2, engine="openpyxl") if file2.name.endswith(".xlsx") else pd.read_csv(file2)

        # 顯示欄位供選擇
        st.subheader("🔧 選擇比對欄位")
        column1 = st.selectbox("第一份資料欄位", df1.columns)
        column2 = st.selectbox("第二份資料欄位", df2.columns)

        # 最少共同字數
        length = st.slider("✅ 最少共同字元數", min_value=1, max_value=10, value=4)

        # 執行比對
        if st.button("🚀 開始比對"):
            result = fuzzy_match_items(df1, df2, column1, column2, length)
            st.success(f"✅ 找到 {len(result)} 筆可能重複的品項")
            st.dataframe(result)

            # 下載結果
            csv = result.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ 下載結果 CSV", data=csv, file_name="fuzzy_match_result.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
