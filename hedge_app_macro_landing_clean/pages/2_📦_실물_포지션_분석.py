import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="📦 실물 거래 헷지 분석", layout="wide")
st.header("📦 실물 거래 파일 업로드 및 헷지 분석")

uploaded_file = st.file_uploader("실물 거래 데이터를 업로드하세요 (xlsx)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    lot_size = 25

    st.subheader("🔹 공급선 기준 (Sell 포지션)")
    purchase_grouped = df[['Purchase\nReference', 'Lot NW']].dropna().groupby('Purchase\nReference').sum()
    purchase_grouped = purchase_grouped.rename(columns={'Lot NW': 'Physical Quantity (MT)'})
    purchase_grouped['Underhedge Lot'] = (purchase_grouped['Physical Quantity (MT)'] // lot_size).astype(int)
    purchase_grouped['Overhedge Lot'] = (purchase_grouped['Physical Quantity (MT)'] / lot_size).apply(math.ceil)
    purchase_grouped['Underhedge Exposure (MT)'] = (
        purchase_grouped['Physical Quantity (MT)'] - (purchase_grouped['Underhedge Lot'] * lot_size)).round(3)
    purchase_grouped['Overhedge Exposure (MT)'] = (
        (purchase_grouped['Overhedge Lot'] * lot_size) - purchase_grouped['Physical Quantity (MT)']).round(3)
    purchase_grouped.reset_index(inplace=True)
    purchase_grouped['Position Type'] = 'Sell (Supplier)'
    st.dataframe(purchase_grouped)

    st.subheader("🔸 판매선 기준 (Buy 포지션)")
    sales_grouped = df[['Sales\nReference', 'Lot NW']].dropna().groupby('Sales\nReference').sum()
    sales_grouped = sales_grouped.rename(columns={'Lot NW': 'Physical Quantity (MT)'})
    sales_grouped['Underhedge Lot'] = (sales_grouped['Physical Quantity (MT)'] // lot_size).astype(int)
    sales_grouped['Overhedge Lot'] = (sales_grouped['Physical Quantity (MT)'] / lot_size).apply(math.ceil)
    sales_grouped['Underhedge Exposure (MT)'] = (
        sales_grouped['Physical Quantity (MT)'] - (sales_grouped['Underhedge Lot'] * lot_size)).round(3)
    sales_grouped['Overhedge Exposure (MT)'] = (
        (sales_grouped['Overhedge Lot'] * lot_size) - sales_grouped['Physical Quantity (MT)']).round(3)
    sales_grouped.reset_index(inplace=True)
    sales_grouped['Position Type'] = 'Buy (Customer)'
    st.dataframe(sales_grouped)