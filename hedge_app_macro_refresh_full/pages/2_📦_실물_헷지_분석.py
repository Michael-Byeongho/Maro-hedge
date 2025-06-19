
import streamlit as st
import pandas as pd

st.set_page_config(page_title="📦 실물 헷지 분석", layout="wide")

st.title("📦 실물 거래 파일 업로드 및 헷지 분석")

st.markdown("샘플 파일이 필요한 경우 👉 [샘플 다운로드](../sample_files/sample_hedge_input.xlsx)")

uploaded_file = st.file_uploader("실물 거래 엑셀 파일을 업로드하세요", type=["xlsx"])

required_columns = [
    "Trade Date", "Type", "Supplier", "Customer",
    "Lot NW (MT)", "QP Start", "QP End", "Pricing Currency"
]

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            st.error(f"❌ 다음 필수 컬럼이 누락되었습니다: {', '.join(missing_cols)}")
        else:
            for date_col in ["Trade Date", "QP Start", "QP End"]:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

            if df[["Trade Date", "QP Start", "QP End"]].isnull().values.any():
                st.warning("⚠️ 날짜 형식 오류가 있는 셀이 있어요. 날짜는 YYYY-MM-DD 형식으로 입력해주세요.")

            st.success("✅ 파일이 정상적으로 업로드 및 분석되었습니다.")
            st.dataframe(df)
            st.markdown("📌 *이후 여기서 Buy/Sell Matching, Under/Over Hedge 분석 로직이 추가됩니다.*")

    except Exception as e:
        st.error(f"❌ 파일을 읽는 중 오류 발생: {e}")
else:
    st.info("왼쪽 사이드바에서 샘플 파일을 다운로드하거나 엑셀 파일을 업로드하세요.")
