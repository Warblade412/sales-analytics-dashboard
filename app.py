import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide",
)


@st.cache_data
def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """Load the sales CSV and apply practical cleaning steps."""
    df = pd.read_csv(file_path)

    # Convert dates before filtering or resampling.
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # Remove repeated rows that can appear during data exports.
    df = df.drop_duplicates()

    # Keep missing categories visible instead of silently dropping them.
    categorical_columns = ["Product_Category", "Product", "Region", "Customer_Type"]
    for column in categorical_columns:
        df[column] = df[column].fillna("Unknown")

    # Median imputation is simple, explainable, and resistant to outliers.
    numeric_columns = ["Units_Sold", "Unit_Price", "Revenue", "Profit"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        df[column] = df[column].fillna(df[column].median())

    return df.sort_values("Date").reset_index(drop=True)


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_percent(value: float) -> str:
    return f"{value:+.1f}%"


df = load_and_clean_data("data.csv")

st.title("Sales Analytics Dashboard")
st.caption("Interactive revenue, profitability, product, and regional performance analysis.")

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        overflow: visible;
        white-space: nowrap;
    }

    [data-testid="stMetricValue"] div {
        overflow: visible;
        text-overflow: clip;
        font-size: clamp(1.35rem, 2.4vw, 2rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Filters")

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    selected_categories = st.multiselect(
        "Product category",
        options=sorted(df["Product_Category"].unique()),
        default=sorted(df["Product_Category"].unique()),
    )

    selected_regions = st.multiselect(
        "Region",
        options=sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique()),
    )

    selected_customer_types = st.multiselect(
        "Customer type",
        options=sorted(df["Customer_Type"].unique()),
        default=sorted(df["Customer_Type"].unique()),
    )


if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered_df = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
    & (df["Product_Category"].isin(selected_categories))
    & (df["Region"].isin(selected_regions))
    & (df["Customer_Type"].isin(selected_customer_types))
].copy()

if filtered_df.empty:
    st.warning("No sales records match the selected filters.")
    st.stop()

total_revenue = filtered_df["Revenue"].sum()
average_revenue = filtered_df["Revenue"].mean()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0

monthly_revenue = (
    filtered_df.set_index("Date")
    .resample("ME")["Revenue"]
    .sum()
    .reset_index()
)
monthly_revenue["Month"] = monthly_revenue["Date"].dt.strftime("%b %Y")
growth_rate = (
    monthly_revenue["Revenue"].pct_change().iloc[-1] * 100
    if len(monthly_revenue) > 1
    else 0
)

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Total Revenue", format_currency(total_revenue))
metric_2.metric("Average Order", format_currency(average_revenue))
metric_3.metric("Total Profit", format_currency(total_profit))

metric_4, metric_5 = st.columns(2)
metric_4.metric("Profit Margin", f"{profit_margin:.1f}%")
metric_5.metric("Monthly Growth", format_percent(growth_rate))

st.divider()

left_column, right_column = st.columns((2, 1))

with left_column:
    st.subheader("Revenue Over Time")
    revenue_line = px.line(
        monthly_revenue,
        x="Date",
        y="Revenue",
        markers=True,
        labels={"Date": "Month", "Revenue": "Revenue"},
    )
    revenue_line.update_traces(line_color="#2563eb", line_width=3)
    revenue_line.update_layout(yaxis_tickprefix="$", hovermode="x unified")
    st.plotly_chart(revenue_line, use_container_width=True)

with right_column:
    st.subheader("Category Distribution")
    category_share = (
        filtered_df.groupby("Product_Category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )
    category_pie = px.pie(
        category_share,
        names="Product_Category",
        values="Revenue",
        hole=0.45,
    )
    category_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(category_pie, use_container_width=True)

st.subheader("Top Product Categories")
top_categories = (
    filtered_df.groupby("Product_Category", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Units_Sold", "sum"),
    )
    .sort_values("Revenue", ascending=False)
)
category_bar = px.bar(
    top_categories,
    x="Product_Category",
    y="Revenue",
    color="Profit",
    text_auto=".2s",
    labels={"Product_Category": "Product Category", "Revenue": "Revenue"},
    color_continuous_scale="Blues",
)
category_bar.update_layout(yaxis_tickprefix="$", coloraxis_colorbar_title="Profit")
st.plotly_chart(category_bar, use_container_width=True)

st.subheader("Regional Performance")
region_summary = (
    filtered_df.groupby("Region", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Average_Order_Revenue=("Revenue", "mean"),
        Orders=("Revenue", "count"),
    )
    .sort_values("Revenue", ascending=False)
)
region_chart = px.bar(
    region_summary,
    x="Region",
    y="Revenue",
    color="Region",
    text_auto=".2s",
    labels={"Revenue": "Revenue"},
)
region_chart.update_layout(showlegend=False, yaxis_tickprefix="$")
st.plotly_chart(region_chart, use_container_width=True)

st.subheader("Top Products")
top_products = (
    filtered_df.groupby(["Product", "Product_Category"], as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Units_Sold", "sum"),
    )
    .sort_values("Revenue", ascending=False)
    .head(10)
)
st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Revenue": st.column_config.NumberColumn("Revenue", format="$%.2f"),
        "Profit": st.column_config.NumberColumn("Profit", format="$%.2f"),
        "Units_Sold": st.column_config.NumberColumn("Units Sold", format="%d"),
    },
)

with st.expander("View cleaned dataset sample"):
    st.dataframe(filtered_df.head(100), use_container_width=True, hide_index=True)
