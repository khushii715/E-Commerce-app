import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")
st.set_page_config(page_title="Analysis", page_icon="📊", layout="wide")

df = pd.read_csv("STREAM/E_commerce_sales_data.csv")

with st.sidebar:
    selected=option_menu(menu_title="Main Menu",options=["Home","Data-set","Data Cleaning","Data Visualization","📦 Sales Overview", "👥 Customer Analysis", "🚚 Shipping Analysis", "📈 Time Trends","About"],icons=["house","table","bar-chart","graph-up-arrow","","","","","person"],default_index=0)


if selected=="Home":
    st.title("📊 E-Commerce Sales Dashboard")
    st.caption("Business Performance Analysis")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Sales", "₹2,35,000", "+22%")
 
    with col2:
        st.metric("📦 Orders", "1000", "+38%")

    with col3:
        st.metric("👥 Customers", "810", "+25%")

    with col4:
        st.metric("📈 Avg Sale", "₹920", "+33%")

    left, right = st.columns (2)
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("📌 Business Insights")

    st.info("""
✔ Electronics generated the highest revenue.

✔ North Region has the maximum sales.

✔ COD is the most preferred payment method.

✔ November is the highest selling month.

✔ Average order value is ₹599.
""")

elif selected=="Data-set":
    t1,t2,t3=st.tabs(["Data","Info","Summary"])
    with t1:
        st.title("Data-set")
        df["Order Date"]=pd.to_datetime(df["Order Date"],dayfirst=True,errors="coerce")
        df["Month"]=df["Order Date"].dt.month_name() 
        Month_order=["January","February","March","April","May","June","July","August","September","October","November","December"]
        df["Month"]=pd.Categorical(df["Month"],categories=Month_order,ordered=True)
        df["Week"]=df["Order Date"].dt.day_name()
        day_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        df["Week"]=pd.Categorical(df["Week"],categories=day_order,ordered=True)
        st.dataframe(df)
    with t2:
        st.title("Info")
        df.info()
        st.write(df.columns)
    with t3:
        st.title("Summary")
        st.write(df.describe())

elif selected=="Data Cleaning":
    st.title("Preprocessing")
    t1,t2=st.tabs(["Before Processing","After Processing"])
    with t1:
        st.write(df.isna().sum())
        
    with t2:
        df["Order Date"]=pd.to_datetime(df["Order Date"],dayfirst=True,errors="coerce")
        df["Month"]=df["Order Date"].dt.month_name() 
        Month_order=["January","February","March","April","May","June","July","August","September","October","November","December"]
        df["Month"]=pd.Categorical(df["Month"],categories=Month_order,ordered=True)
        df["Week"]=df["Order Date"].dt.day_name()
        day_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        df["Week"]=pd.Categorical(df["Week"],categories=day_order,ordered=True)
        
        df["Age"].median()
        df["Age"]=df["Age"].fillna(df["Age"].median())
        df["Region"]=df["Region"].fillna("Unknown")
        df["Shipping Status"]=df["Shipping Status"].fillna("Pending")
        st.write(df.isna().sum())
        st.write(df) #

elif selected=="Data Visualization": 
    st.title("📊 Data Visualization Hub")
    st.markdown("""📊 Welcome to the Visualization Hub! 
    Select an analysis from the sidebar to view detailed insights on Sales, Customers, Shipping, and Trends""")
    st.markdown("---")

    # 1. KPI CARDS - Sabse upar
    st.subheader("📌 Quick Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"₹{df['Total Price'].sum():,.0f}", "12% ↑")
    col2.metric("📦 Total Orders", f"{len(df):,}", "5% ↑")
    col3.metric("👥 Total Customers", f"{df['Customer ID'].nunique():,}", "8% ↑")
    col4.metric("⭐ Avg Order Value", f"₹{df['Total Price'].mean():,.0f}", "3% ↑")
    st.markdown("---")

    # 2. MINI PREVIEW GRAPHS - 2 chote graph
    st.subheader("📈 Quick Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("*Top Categories by Sales*")
        cat_sales = df.groupby('Category')['Total Price'].sum().nlargest(5).reset_index()
        fig1 = px.bar(cat_sales, x='Category', y='Total Price', template="plotly_dark", color='Category')
        fig1.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        df["Order Date"]=pd.to_datetime(df["Order Date"],dayfirst=True,errors="coerce")
        st.write("*Monthly Sales Trend*")
        monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Total Price'].sum().reset_index()
        monthly['Order Date'] = monthly['Order Date'].astype(str)
        fig2 = px.line(monthly, x='Order Date', y='Total Price', template="plotly_dark", markers=True)
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    st.info("👈 *Tip*: Select an analysis from the left sidebar to view detailed insights on Sales, Customers, Shipping, and Trends")
    
elif selected=="📦 Sales Overview":
    st.subheader("📦 Sales Overview")
    # t1, t2, t3, t4 = st.tabs(["📦 Sales Overview", "👥 Customer Analysis", "🚚 Shipping Analysis", "📈 Time Trends"])
    df['Order Date'] = pd.to_datetime(df['Order Date'],dayfirst=True, errors='coerce')
    df['Month'] = df['Order Date'].dt.strftime('%B')
    df['Week'] = df['Order Date'].dt.strftime('Week %U')
    
    # TAB 1: Sales Overview
    # with t1:
            # 1. Bar Chart: Sales by Category
    cat_sales = df.groupby('Category')['Total Price'].sum().reset_index().sort_values('Total Price', ascending=False)
    fig1 = px.bar(cat_sales, x='Category', y='Total Price', 
                         title='💰 Total Sales by Category',
                         color='Category', text_auto='.2s')
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)
    
    category_sales = df.groupby('Category')['Total Price'].sum().reset_index()
    top_cat = category_sales.loc[category_sales['Total Price'].idxmax()]
    total_sales = category_sales['Total Price'].sum()
    percentage = (top_cat['Total Price'] / total_sales) * 100

    st.success(
    f"💡 * Insight*: '{top_cat['Category']}' contributes {percentage:.1f}% of total sales - ₹{top_cat['Total Price']/1000000:.1f}M. "
    f"Consider running bundle offers and promotions for 'Wearables' and 'Accessories' to boost their performance.")

            # 2. Pie Chart: Sales by Region
    st.markdown("----")
    region_sales = df.groupby('Region')['Total Price'].sum().reset_index()
    fig2 = px.pie(region_sales, names='Region', values='Total Price',
             title='🌍 Sales Distribution by Region', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    region_sales = df.groupby('Region')['Total Price'].sum().reset_index()
    top_region = region_sales.loc[region_sales['Total Price'].idxmax()]
    bottom_region = region_sales.loc[region_sales['Total Price'].idxmin()]
    total_sales = region_sales['Total Price'].sum()

    top_perc = (top_region['Total Price'] / total_sales) * 100
    bottom_perc = (bottom_region['Total Price'] / total_sales) * 100

# Insight Box
    st.info(
    f"💡 *Insight*: '{top_region['Region']}' region leads with {top_perc:.1f}% of sales. "
    f"'{bottom_region['Region']}' is at {bottom_perc:.1f}%. The sales team should focus on growth strategies for '{bottom_region['Region']}' region.")

    fig2.update_layout(template="plotly_dark", title_font_size=20, title_font_color="cyan")    
    

        # 3. Top 10 Products
    st.markdown("---")
    
    top_products = df.groupby('Product Name')['Total Price'].sum().reset_index().sort_values('Total Price', ascending=False).head(10)
    fig3 = px.bar(top_products, x='Total Price', y='Product Name', orientation='h',
                     title='🏆 Top 10 Products by Sales', color='Total Price')
    


    st.success(f"💡 * Insight* : Laptop is the top-selling product. "f"Focus on bundling low-performing accessories like Mouse and Keyboard with top products to increase revenue.")
    

    # 4 Heatmap 
   
    st.plotly_chart(fig3, use_container_width=True)
    heat_data = df.pivot_table(values='Total Price', index='Region', columns='Category', aggfunc='sum').reset_index()
    st.markdown("---")
    fig10 = px.imshow(heat_data.set_index('Region'), 
             title='🔥 Sales Heatmap: Region vs Category', aspect='auto', color_continuous_scale='Blues')
    st.plotly_chart(fig10, use_container_width=True)
    
  
    heatmap_data = df.pivot_table(index='Region', columns='Category', values='Total Price', aggfunc='sum')
    max_region = heatmap_data.sum(axis=1).idxmax()
    min_category = heatmap_data.sum(axis=0).idxmin()

    st.warning(
    f"💡 * Insight*: '{max_region}' region performs best overall. "f"'{min_category}' category has the lowest sales across all regions. Run targeted promotions to improve it.")
     
    

elif selected=="👥 Customer Analysis":
        st.subheader("👥 Customer Analysis")
    # TAB 2: Customer Analysis
    
            # 4. Bar Chart: Sales by Gender
        df["Age"].median()
        df["Age"]=df["Age"].fillna(df["Age"].median())
        gender_sales = df.groupby('Gender')['Total Price'].sum().reset_index()
        fig4 = px.bar(gender_sales, x='Gender', y='Total Price',
        title='📈 Sales by Gender', color='Gender')
        st.plotly_chart(fig4, use_container_width=True)
        gender_orders = df.groupby('Gender')['Order Date'].nunique()
        top_gender = gender_orders.idxmax()
        st.success(f"💡 *Insight*: '{top_gender}' customers drive the most orders. Focus marketing to balance gender engagement.")

    
            # 5. Histogram: Age Distribution
        st.markdown("---")
        df["Age"].median()
        df["Age"]=df["Age"].fillna(df["Age"].median())
        fig5 = px.histogram(df, x='Age', nbins=20,
                               title='🎂 Customer Age Distribution',
                               color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig5, use_container_width=True)
        avg_age = df['Age'].mean()
        st.info(f"💡 * Insight*: The core customer segment is around {avg_age:.0f} years old. Tailor products and campaigns for the 25-40 age group.")
        
        # 6. Scatter: Price vs Quantity
        st.markdown("---")
        fig6 = px.scatter(df, x='Unit Price', y='Quantity', size='Total Price',
                         color='Category', hover_data=['Product Name'],
                         title='📦 Unit Price vs Quantity')
        st.plotly_chart(fig6, use_container_width=True)
        top_category_bubble =df.groupby('Category')['Order Date'].count().idxmax()
        st.warning(f"💡 * Insight*: '{top_category_bubble}' has the highest order volume. Low-to-mid price products with quantity 1-3 are most popular.")
    

elif selected=="🚚 Shipping Analysis" :
        st.subheader("🚚 Shipping Analysis") 
    
        
# 9
        df["Shipping Status"]=df["Shipping Status"].fillna("Pending")
        ship_mode = df.groupby('Shipping Status')['Total Price'].sum().reset_index()
        fig2 = px.pie(ship_mode, values='Total Price', names='Shipping Status', 
              title="Revenue by Shipping Status", hole=0.4)
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
        mode_rev = df.groupby('Shipping Status')['Total Price'].sum().reset_index()
        
        top_mode = mode_rev.loc[mode_rev['Total Price'].idxmax()]
        st.success(
        f"💡 *Insight*: '{top_mode['Shipping Status']}' mode generates the highest revenue. "f"Focus on reducing 'Returned' and 'Pending' orders to improve efficiency.")


        # 8. Box Plot: Shipping Fee by Region
        st.markdown("----")
        df["Shipping Status"]=df["Shipping Status"].fillna("Pending")
        df["Region"]=df["Region"].fillna("Unknown")
        fig8 = px.box(df, x='Region', y='Shipping Fee', color='Region',
             title='📮 Shipping Fee Distribution by Region')
        st.plotly_chart(fig8, use_container_width=True) 
        

        high_fee_region = df.groupby('Region')['Shipping Fee'].median().idxmax()
        st.warning(
        f"💡 * Insight*: '{high_fee_region}' region has the highest median shipping fee. " f"Review logistics for this region to reduce costs and improve margins.")



elif selected=="📈 Time Trends":
    st.subheader("📊 Time Trends")
     # TAB 4: Time Trends
   
        # 9. Line Chart: Monthly Sales Trend
    df["Order Date"]=pd.to_datetime(df["Order Date"],dayfirst=True,errors="coerce")
    df["Month"]=df["Order Date"].dt.month_name() 
    Month_order=["January","February","March","April","May","June","July","August","September","October","November","December"]
    df["Month"]=pd.Categorical(df["Month"],categories=Month_order,ordered=True)
    df["Week"]=df["Order Date"].dt.day_name()
    day_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    df["Week"]=pd.Categorical(df["Week"],categories=day_order,ordered=True)
    

    Month_order=["January","February","March","April","May","June","July","August","September","October","November","December"]
    df["month"]=pd.Categorical(df["Month"],categories=Month_order,ordered=True)
    st.subheader("📈 Revenue Trend Over Time")
    monthly = df.groupby("Month", as_index=False)["Total Price"].sum().sort_values("Month")
    fig = px.area(monthly, x="Month", y="Total Price", markers=True)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f5f7fa", height=380, margin=dict(t=20, b=0, l=0, r=0),
        yaxis_title="Revenue", xaxis_title="Month"
    )
    fig.update_traces(fill="tozeroy", fillgradient=dict(type="vertical", colorscale=[[0, "rgba(45,212,191,0.35)"],[1,"rgba(45,212,191,0)"]]))
    st.plotly_chart(fig, use_container_width=True)

    st.success(
    f"💡 Insight*: Sales peak in Januaryand are lowest in March. "
    f"Stock up and run ads 1 month before January. Use discounts in March to boost sales."
)
        



# 10 . Line Chart: Orders by Day of Week
    
    st.markdown("----")
    df["Week"]=df["Order Date"].dt.day_name()
    day_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    df["Week"]=pd.Categorical(df["Week"],categories=day_order,ordered=True)

    st.subheader("📅 Orders by Day of Week")
    order_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    wd = df["Week"].value_counts().reindex(order_days).fillna(0).reset_index()
    wd.columns = ["Week", "Orders"]
    fig = px.line(wd, x="Week", y="Orders", markers=True)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f5f7fa", height=360, margin=dict(t=20, b=0, l=0, r=0),
        yaxis_title="Orders", xaxis_title="Days"
    )
    fig.update_traces(fill="tozeroy", fillgradient=dict(type="vertical", colorscale=[[0, "rgba(45,212,191,0.35)"],[1,"rgba(45,212,191,0)"]]))
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"💡*Insight * :Most orders happen on Tuesday. Fewest on Friday. "
    f"Launch weekend deals on Tuesday and run email campaigns to lift Friday sales.")



# 11 Sales Trend by Category
    st.markdown("----")
    st.subheader("📊 Sales Trend by Category")
    
    monthly_cat = df.copy()
    monthly_cat['Month'] = monthly_cat['Order Date'].dt.to_period('M').astype(str)
    trend_data = monthly_cat.groupby(['Month', 'Category'])['Total Price'].sum().reset_index()
    
    # Line chart with multiple lines - har category ki 1 line
    fig_category_trend = px.line(
        trend_data, 
        x='Month', 
        y='Total Price', 
        color='Category',  # Har category ka alag color
        title="Monthly Sales Trend by Category",
        markers=True
    )
    fig_category_trend.update_layout(
        template="plotly_dark",
        xaxis_title="Month",
        yaxis_title="Total Sales ",
        legend_title="Category",
        xaxis_tickangle=-45
    )
    fig.update_traces(fill="tozeroy", fillgradient=dict(type="vertical", colorscale=[[0, "rgba(45,212,191,0.35)"],[1,"rgba(45,212,191,0)"]]))
    st.plotly_chart(fig_category_trend, use_container_width=True)
    
    top_cat = df.groupby('Category')['Total Price'].sum().idxmax()
    st.warning(
    f"💡 *Insight*: '{top_cat}' is the best-performing category all year. "
    f"Give it more stock and ad budget. All categories dip in Feb - use offers then to balance revenue."
)

  


elif selected=="About":
    st.title("ℹ️ About This Dashboard")
    
    st.markdown("---")
    
    # 1. Project Intro
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📊 E-Commerce Sales Dashboard")
        st.write("""
        This dashboard is designed to analyze the sales data of an E-Commerce Company. It provide a centralized view of key metrics including sales performance,customer insights,shipping analytics and time based trends.
                  
        *Main Goal:* Data se insights nikalna aur business decisions ko easy karna.
        """)
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1019/1019607.png", width=150) # dashboard icon

        st.markdown("---")

    # 2. Features
    st.subheader("✨ Key Features")
    features = {
        "📈 Sales Overview": "Category aur Product wise sales analysis",
        "👥 Customer Analysis": "Top customers aur Gender distribution", 
        "🚚 Shipping Analysis": "Delivery time, Shipping fee aur Status",
        "⏰ Time Trends": "Monthly sales aur Category growth"
    }
    for title, desc in features.items():
        st.write(f"*{title}*: {desc}")

    st.markdown("---")
# 3
    st.subheader("📁 Dataset Information")
    st.write(f"*Rows: {len(df):,}  |  **Columns*: {len(df.columns)}")
    st.write("*Columns Include*: Order ID, Product, Category,Age, Price, Quantity,Unit Price, Customer, Region,Shipping Status,Month,Week")

    st.markdown("---")

    # 4. Tech Stack
    st.subheader("🛠️ Tech Stack Used")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Python", "3.12")
    col2.metric("Library", "Streamlit")
    col3.metric("Charts", "Plotly")
    col4.metric("Data", "Pandas")

    st.markdown("---")

    # 4. Creator Info
    st.subheader("👩‍💻 Created By")
    st.write("*Name*: Khushi Kumari")
   
    st.success("Thanks for visiting! ")




