import streamlit as st
import requests
import xml.etree.ElementTree as ET

# RSS feed URL
RSS_URL = "https://style-threadz.myspreadshop.net/1482874/products.rss?pushState=false&targetPlatform=google"

@st.cache_data(ttl=600)
def fetch_products_from_rss():
    """Fetch products from Spreadshop RSS feed"""
    resp = requests.get(RSS_URL, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)

    products = []
    for item in root.findall('.//item'):
        title = item.findtext('title') or ''
        price = item.findtext('{http://base.google.com/ns/1.0}price') or ''
        image = item.findtext('{http://base.google.com/ns/1.0}image_link') or ''

        products.append({
            "title": title.strip(),
            "price": price.strip(),
            "image": image.strip()
        })
    return products


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Style Threadz Products", layout="wide")
st.title("🛍️ Style Threadz Products")

try:
    products = fetch_products_from_rss()
    if not products:
        st.warning("No products found.")
    else:
        cols_per_row = 4
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, prod in zip(cols, products[i:i+cols_per_row]):
                with col:
                    # Product card
                    st.image(prod["image"], use_column_width=True)
                    st.subheader(prod["title"])
                    st.write(f"**Price:** {prod['price']}")
                    # ✅ Fixed redirect link (always goes to stylethreadz.com)
                    st.markdown(
                        '[👉 View on StyleThreadz](https://stylethreadz.com/)', 
                        unsafe_allow_html=True
                    )
except Exception as e:
    st.error(f"Error loading products: {e}")
        
