import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os
import os
print("Current working directory:", os.getcwd())
# Construct the file path
file_path = os.path.join('D:', 'data sicece 2', '44', 'MID-project', 'Hotel Bookings.csv')
# Load your data here
data = pd.read_csv('D:/data sicece 2/44/MID-project/Hotel Bookings.csv')  

st.set_page_config(
    layout='wide',
    page_title='DashBoard',
    page_icon='📊'
)

tab1, tab2 = st.tabs(['🏨 Hotel Booking Dashboard', '📊 Additional Visualizations'])

# Tab 1: Hotel Booking Dashboard
with tab1:
    col1, col2, col3 = st.columns([6, 0.5, 6])
    
    with col1:
        st.sidebar.subheader('Numerical Descriptive Statistics')
            
    with col3:
        st.subheader('Categorical Descriptive Statistics')
        cat = data.select_dtypes(include=['object'])  # Example for categorical data
        st.dataframe(cat, 500, 200)

    # Sidebar filters
    selected_category = st.sidebar.selectbox('Hotel', data['hotel'].unique())
    selected_years = st.sidebar.multiselect('Year', data['arrival_date_year'].unique(), default=data['arrival_date_year'].unique())
    selected_countries = st.sidebar.multiselect('Country', data['country'].unique(), default=['TUR', 'ITA', 'RUS'])
    type_of_customer = st.sidebar.multiselect('Customer Type', data['customer_type'].unique(), default=['Transient', 'Contract', 'Transient-Party', 'Group'])

    # Filter the data based on user selections
    filtered_data = data[
        (data['hotel'] == selected_category) &
        (data['arrival_date_year'].isin(selected_years)) &
        (data['country'].isin(selected_countries)) &
        (data['customer_type'].isin(type_of_customer))
    ]

    # Display total reservations
    st.write(f"Total reservations: {len(filtered_data)}")

    # Set figure size
    figure_size = (900, 600)

    # Custom month order for plotting
    custom_month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthly_data = filtered_data.groupby('arrival_date_month')['arrival_date_month'].count().reindex(custom_month_order)
    monthly_data.index = pd.Categorical(monthly_data.index, categories=custom_month_order, ordered=True)

    # Figure 1: Reservations by Month
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data.values, mode='lines+markers', line=dict(color='#3A98B9')))
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(showgrid=False)
    fig1.update_layout(title='Reservations by Month', width=figure_size[0], height=figure_size[1])
    st.plotly_chart(fig1)

    # Figure 2: Cancellation Distribution
    fig2 = px.pie(
        filtered_data.replace({'is_canceled': {0: 'No', 1: 'Yes'}}),
        names='is_canceled',
        title='Cancellation Distribution',
        width=figure_size[0],
        height=figure_size[1],
        color_discrete_sequence=['#3A98B9', '#C51605']
    )
    st.plotly_chart(fig2)

    # Figure 3: Guests by Country
    country_data = filtered_data.groupby('country')['country'].count().reset_index(name='count')
    country_data = country_data.sort_values(by='count', ascending=False)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=country_data['country'], y=country_data['count'], marker_color='#3A98B9'))
    fig3.update_xaxes(categoryorder='total descending')
    fig3.update_layout(title='Guests by Country', width=figure_size[0], height=figure_size[1])
    fig3.update_xaxes(showgrid=False)
    fig3.update_yaxes(showgrid=False)
    st.plotly_chart(fig3)

    # Figure 4: ADR by Family Size
    family_data = filtered_data[['adults', 'children', 'babies', 'adr']]
    family_data['family'] = family_data['adults'] + family_data['children'] + family_data['babies']
    fig4 = px.box(family_data, x='family', y='adr', title='ADR by Family Size')
    fig4.update_xaxes(title='Family Size')
    fig4.update_yaxes(title='Average Daily Rate (ADR)')
    fig4.update_traces(marker_color='#3A98B9')
    fig4.update_layout(width=figure_size[0], height=figure_size[1])
    fig4.update_xaxes(showgrid=False)
    fig4.update_yaxes(showgrid=False)
    st.plotly_chart(fig4)

    # Figure 5: Weekend and Week Night Stays Distribution
    weekend_stays = filtered_data['stays_in_weekend_nights'].sum()
    weeknight_stays = filtered_data['stays_in_week_nights'].sum()
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=['Weekend Stays', 'Week Night Stays'], y=[weekend_stays, weeknight_stays], marker_color='#3A98B9'))
    fig5.update_layout(title='Weekend and Week Night Stays Distribution', width=figure_size[0], height=figure_size[1])
    fig5.update_xaxes(title='Stay Type')
    fig5.update_yaxes(title='Stay Count')
    fig5.update_xaxes(showgrid=False)
    fig5.update_yaxes(showgrid=False)
    st.plotly_chart(fig5)

# Tab 2: Additional Visualizations
with tab2:
    st.title("📊 Additional Visualizations")

    # Chart - 1 visualization code
    st.subheader("Hotel Booking Percentage")
    hotel_name = data['hotel'].unique()
    unique_booking = data.hotel.value_counts().sort_values(ascending=True)
    fig1 = px.pie(names=hotel_name, values=unique_booking, hole=0.5, color=hotel_name,
                   color_discrete_map={'Resort Hotel': 'teal', 'City Hotel': 'nude'})
    fig1.update_traces(textinfo='percent + value')
    fig1.update_layout(title_text='Hotel Booking Percentage', title_x=0.5)
    fig1.update_layout(legend=dict(orientation='h', yanchor='bottom', xanchor='center'))
    st.plotly_chart(fig1, use_container_width=True)

    # Chart - 2 visualization code
    st.subheader("Hotel Booking Count")
    hotel_count = data.hotel.value_counts()
    fig2 = plt.figure(figsize=(9, 7))
    hotel_count.plot.pie(autopct='%1.2f%%', shadow=True, fontsize=15, startangle=50)
    plt.title('Hotel Booking Percentage')
    plt.axis('equal')
    st.pyplot(fig2)  

    # Chart - 3 visualization code
    st.subheader("Hotel Cancellation Percentage")
    cancelled_hotel = data.is_canceled.value_counts()
    fig3 = plt.figure(figsize=(9, 7))
    cancelled_hotel.plot.pie(explode=(0.05, 0.05), autopct='%1.2f%%', shadow=True, fontsize=15, startangle=50)
    plt.title('Percentage of Hotel Cancellation and Non-Cancellation')
    plt.axis('equal')
    st.pyplot(fig3)  

    # Chart - 4 visualization code
    st.subheader("Bookings Across Years")
    fig4 = plt.figure(figsize=(10, 4))
    sns.countplot(x=data['arrival_date_year'], hue=data['hotel'])
    plt.title("Number of bookings across year", fontsize=25)
    st.pyplot(fig4)  

    # Chart - 5 visualization code
    st.subheader("Bookings Across Months")
    fig5 = plt.figure(figsize=(15, 5))
    sns.countplot(x=data['arrival_date_month'], hue=data['hotel'])
    plt.title("Number of booking across months", fontsize=25)
    st.pyplot(fig5)  

    # Chart - 6 visualization code
    st.subheader("Preferred Room Type by Guests")
    fig6 = plt.figure(figsize=(15, 5))
    sns.countplot(x=data['reserved_room_type'], order=data['reserved_room_type'].value_counts().index)
    plt.title('Preferred Room Type by Guests', fontsize=20)
    st.pyplot(fig6)  

    # Chart - 7 visualization code
    st.subheader("Assigned Room Type to Guests")
    fig7 = plt.figure(figsize=(15, 5))
    sns.countplot(x=data['assigned_room_type'], order=data['assigned_room_type'].value_counts().index)
    plt.title('Assigned Room Type to Guests', fontsize=20)
    st.pyplot(fig7)  

    # Chart - 8 visualization code
    st.subheader("Percentage of Repeated Guests")
    rep_guests = data['is_repeated_guest'].value_counts()
    fig8 = plt.figure(figsize=(15, 6))
    rep_guests.plot.pie(autopct='%1.2f%%', explode=(0.00, 0.09), shadow=False)
    plt.title('Percentage of Repeated Guests', fontsize=20)
    plt.axis('equal')
    st.pyplot(fig8)  

    # Chart - 9 visualization code
    st.subheader("Customer Type Booking Count")
    cust_type = data['customer_type'].value_counts()
    fig9 = plt.figure(figsize=(15, 5))
    cust_type.plot()
    plt.xlabel('Count', fontsize=8)
    plt.ylabel('Customer Type', fontsize=10)
    plt.title('Customer Type and their booking count', fontsize=20)
    st.pyplot(fig9)  

    # Chart - 10 visualization code
    st.subheader("Most Repeated Guests for Each Hotel")
    rep_guest = data[data['is_repeated_guest'] == 1].groupby('hotel').size().reset_index()
    rep_guest = rep_guest.rename(columns={0: 'number_of_repeated_guests'})
    fig10 = plt.figure(figsize=(8, 4))
    sns.barplot(x=rep_guest['hotel'], y=rep_guest['number_of_repeated_guests'])
    plt.xlabel('Hotel type', fontsize=12)
    plt.ylabel('Count of repeated guests', fontsize=12)
    plt.title('Most Repeated Guests for Each Hotel', fontsize=20)
    st.pyplot(fig10)  

    # Chart - 11 visualization code
    st.subheader("ADR Across Each Distribution Channel")
    dist_channel_adr = data.groupby(['distribution_channel', 'hotel'])['adr'].mean().reset_index()
    fig11 = plt.figure(figsize=(15, 5))
    sns.barplot(x='adr', y='distribution_channel', data=dist_channel_adr, hue='hotel')
    plt.title('ADR Across Each Distribution Channel', fontsize=20)
    st.pyplot(fig11) 

    # Chart - 12 visualization code
    st.subheader("Daily Revenue by Each Hotel Type")
    most_rev = data.groupby('hotel')['adr'].count()
    fig12 = plt.figure(figsize=(15, 5))
    most_rev.plot.pie(autopct='%1.2f%%')
    plt.title('Percentage of Daily Revenue by Each Hotel Type', fontsize=20)
    plt.axis('equal')
    st.pyplot(fig12) 
