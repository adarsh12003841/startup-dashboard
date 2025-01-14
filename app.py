import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Page configuration
st.set_page_config(layout='wide',page_title = 'Startup Analysis')

# Function to call for overall analysis
def load_over_analysis():
    st.title('Overall Analysis')

    # Total invested amount
    total = round(df['amount'].sum())
    # Max amount invest on a startup
    max = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]
    # Average Funding on companies
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # Total funded startup
    total_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total Amount',str(total) + 'Cr')
    with col2:
        st.metric('Max Amount',str(max) + 'Cr')
    with col3:
        st.metric('Avg Amount',str(round(avg_funding)) + 'Cr')
    with col4:
        st.metric('Total Startups',str(total_startups))
    # Month on month graph
    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] =  temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig4,ax4 = plt.subplots()
    ax4.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig4)

def load_investor_details(investor):
    st.title(investor)

    # load the recent 5 investment of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','City  Location','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2= st.columns(2)

    with col1:
        # biggest Investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Invested Sectors')
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct = '%0.01f%%')
        st.pyplot(fig1)




    # Make a year column and groupby year to find the total amount invested by investor every year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY Investment')
    fig3, ax3 = plt.subplots()
    ax3.plot(year_series.index,year_series.values)
    st.pyplot(fig3)

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select one', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
        load_over_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)













































