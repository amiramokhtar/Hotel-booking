
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the data
data = pd.read_csv('Hotel Bookings.csv')  

# Streamlit app title and description
st.title("🌴 Hotel Booking Dashboard")
st.markdown("Explore hotel reservations between 2015 and 2017 in detail.")

# Sidebar filters
st.sidebar.subheader('Filters')
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
# Use .loc to avoid SettingWithCopyWarning
family_data.loc[:, 'family'] = family_data['family']
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
