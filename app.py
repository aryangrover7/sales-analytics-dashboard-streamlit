import pandas as pd
import streamlit as st

st.title("Sales Analytics Dashboard")


# -----------------------------
# LOAD DEMO DATA
# -----------------------------

df = pd.read_csv("sales.csv")


# Store data in session
if "sales_data" not in st.session_state:

    st.session_state.sales_data = df.copy()

df = st.session_state.sales_data


# -----------------------------
# FILTERS
# -----------------------------

st.sidebar.header("Filters")

categories = [
    "All"
] + list(df["Category"].unique())

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

if selected_category == "All":

    filtered_df = df

else:

    filtered_df = df[
        df["Category"] == selected_category
    ]


# -----------------------------
# ADD NEW SALE
# -----------------------------

st.sidebar.subheader("Add New Sale")

product = st.sidebar.text_input(
    "Product"
)

category_new = st.sidebar.text_input(
    "Category"
)

sales = st.sidebar.number_input(
    "Sales",
    min_value=0
)

units = st.sidebar.number_input(
    "Units",
    min_value=0
)

add_button = st.sidebar.button(
    "Add Sale"
)


if add_button:

    new_sale = {
        "Product": product,
        "Category": category_new,
        "Sales": sales,
        "Units": units
    }

    st.session_state.sales_data = pd.concat(
        [
            st.session_state.sales_data,
            pd.DataFrame([new_sale])
        ],
        ignore_index=True
    )

    st.success(
        "Sale added successfully!"
    )

    # Update dataframe

    df = st.session_state.sales_data

    # Update filtered data

    if selected_category == "All":

        filtered_df = df

    else:

        filtered_df = df[
            df["Category"] == selected_category
        ]


# -----------------------------
# OVERALL PERFORMANCE
# -----------------------------

st.subheader(
    "Overall Performance"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Sales",
        df["Sales"].sum()
    )

with col2:

    st.metric(
        "Total Units",
        df["Units"].sum()
    )

with col3:

    st.metric(
        "Total Products",
        len(df)
    )


# -----------------------------
# DATA TABLE
# -----------------------------

st.subheader(
    "Sales Data"
)

st.dataframe(
    filtered_df
)


# -----------------------------
# FILTERED PERFORMANCE
# -----------------------------

st.subheader(
    "Filtered Performance"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Filtered Sales",
        filtered_df["Sales"].sum()
    )

with col2:

    st.metric(
        "Filtered Units",
        filtered_df["Units"].sum()
    )

with col3:

    st.metric(
        "Filtered Products",
        len(filtered_df)
    )


# -----------------------------
# SALES BY PRODUCT
# -----------------------------

st.subheader(
    "Sales by Product"
)

product_sales = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_sales)


# -----------------------------
# SALES BY CATEGORY
# -----------------------------

st.subheader(
    "Sales by Category"
)

category_data = df.groupby(
    "Category"
)["Sales"].sum()

st.bar_chart(
    category_data
)



st.subheader("Top 3 Products by Sales")

top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .reset_index()
)

st.bar_chart(
    top_products,
    x="Product",
    y="Sales",
    horizontal=True,
    sort="-Sales"
)

st.subheader("Top 3 Products by Units Sold")

top_units = (
    filtered_df
    .groupby("Product")["Units"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .reset_index()
)

st.bar_chart(
    top_units,
    x="Product",
    y="Units",
    horizontal=True,
    sort="-Units"
)
