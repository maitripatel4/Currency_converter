import streamlit as st
from datetime import datetime
import pandas as pd

df = pd.read_csv('data/Currency_Data_All_Years.csv')

# Retrieving currency codes
currency_code = []
for val in df.columns:
    start = val.find('(')
    end = val.find(')')

    if start != -1:
        ans = val[start + 1:end]
        currency_code.append(ans)

st.set_page_config(layout="wide")
st.title("NORTHERN TRUST CURRENCY CONVERTOR")

col1, col2 = st.columns(2)

with col1:
    # Selecting first currency
    curr1 = st.selectbox('Currency 1', currency_code)
    st.write('You selected:', curr1)

    # Finding the index of the currency code
    i = 0
    curr1_index = -1
    for item in currency_code:
        if curr1 == item:
            curr1_index = i
        i = i + 1

    # Selecting second currency
    curr2 = st.selectbox('Currency 2', currency_code)
    st.write('You selected:', curr2)

    # Finding the index of the currency code
    i = 0
    curr2_index = -1
    for item in currency_code:
        if curr2 == item:
            curr2_index = i
        i = i + 1

    # Converting the streamlit date format to the csv file format for comparison
    d = st.date_input("Rate for the given date: ")
    d = str(d)
    d = datetime.strptime(d, '%Y-%m-%d').strftime('%d-%b-%y')

    # Finding the Date index
    i = 0
    date_index = -1
    for item in df.Date:
        if d == item:
            date_index = i
        i = i + 1

    # Finding the cell corresponding to the currency code projected against the date entered
    fx_rate = df.iloc[date_index, curr2_index + 1]  # For Currency 1
    fx_rate1 = df.iloc[date_index, curr1_index + 1] # For Currency 2

    # When Conversion is made with respect to USD
    if curr1 == 'USD':
        if fx_rate == '?':                              # Handling NaN Data
            st.warning("Data Not Found!")
        elif pd.isnull(fx_rate):                        # Handling NaN Data
            st.warning("Data Not Found!")
        else:
            st.write("Price: ", float(fx_rate))

    # When two different Currencies are selected
    else:
        if fx_rate == '?' or fx_rate1 == '?':            # Handling NaN Data
            st.warning("Data Not Found!")
        elif pd.isnull(fx_rate) or pd.isnull(fx_rate1):  # Handling NaN Data
            st.warning("Data Not Found!")
        else:
            fx_rate = float(fx_rate) / float(fx_rate1)   # Formula for conversion from one Currency to other
            st.write("Price: ", fx_rate)

    if not (pd.isnull(fx_rate) or fx_rate == '?' or pd.isnull(fx_rate1) or fx_rate1 == '?'):
        st.title("Convertor:")
        amt = st.number_input("Enter the amount to convert: ")
        con_amt = float(fx_rate) * float(amt)
        st.text(str(amt) + " " + str(curr1) + " is equivalent to " + str(con_amt) + " " + curr2 + ".")

# Graphs are made for currency 2 with respect to USD
with col2:
    option = st.selectbox('Enter the trend that you want to see for Currency 2: ',
                          ('Specific Period', 'Weekly', 'Monthly', 'Quarterly', 'Yearly'))

    if option == "Specific Period":

        start_date = st.date_input("Starting Date: ")
        start_date = str(start_date)
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%b-%y')

        # Finding the Date index
        i = 0
        st_date_index = -1
        for item in df.Date:
            if start_date == item:
                st_date_index = i
            i = i + 1

        end_date = st.date_input("Ending Date: ")
        end_date = str(end_date)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%b-%y')

        i = 0
        en_date_index = -1
        for item in df.Date:
            if end_date == item:
                en_date_index = i
            i = i + 1

        # Retrieving data from csv file and backfilling the data to avoid unevenness in graphs
        dfwo = pd.read_csv('data/Currency_Data_All_YearsWO.csv')
        edit_df = dfwo.fillna(method="backfill")

        # Retrieving the column corresponding to the country code
        plotdata = edit_df.iloc[:, curr2_index + 1]

        # Retrieving the data as per the start and end date as given by the user
        plotdata = plotdata[st_date_index:en_date_index + 1]

        # Creating a list to store the currency values
        temp_list = []
        temp_list = edit_df.iloc[st_date_index:en_date_index +
                                               1, curr2_index + 1].tolist()

        # Initializing the max and min variables to handle the condition when no input is given
        mx = -1
        mn = -1

        # Finding the max and min values of the list
        if temp_list.__len__() != 0:
            mx = max(temp_list)
            mn = min(temp_list)

        st.line_chart(plotdata)

    else:

        stri = "data/Exchange_Rate_Report_"

        if option == "Weekly":
            year = st.selectbox('Select Year: ', (
                '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'))

            # Select box for selecting the week
            week = st.selectbox(
                'Select Week: ', [f"Week {i}" for i in range(1, 53)])
            stri += str(year)
            stri += ".csv"
            df1 = pd.read_csv(stri)

            # Backfilling and frontfilling the data to make the graph more uniform 
            df1 = df1.fillna(method="backfill")
            df1 = df1.fillna(method="ffill")

            # Locating the column corresponding to the currency code
            plotdata = df1.iloc[:, curr2_index + 1]
            tp = df1.__len__() // 52

            # Extracting the week number from the selected week
            week_no = int(week[5:])

            # Getting the plot data as per the selected week
            plotdata = plotdata[(week_no - 1) * tp:week_no * tp]

            temp_list = []
            temp_list = df1.iloc[(week_no - 1) * tp:week_no *
                                                    tp, curr2_index + 1].tolist()
            mx = max(temp_list)
            mn = min(temp_list)

            st.line_chart(plotdata)

        elif option == "Monthly":
            year = st.selectbox('Select Year: ', (
                '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'))
            stri += str(year)
            df1 = pd.read_csv(stri + ".csv")
            df1 = df1.fillna(method="backfill")
            df1 = df1.fillna(method="ffill")
            plotdata = df1.iloc[:, curr2_index + 1]

            # Making 12 equal partitions in the data
            tp = df1.__len__() // 12

            # Dividing the yearly data into 12 parts
            plotdata = plotdata[::tp]
            mx = max(plotdata.tolist())
            mn = min(plotdata.tolist())
            st.line_chart(plotdata)

        elif option == "Quarterly":
            year = st.selectbox('Select Year: ', (
                '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'))
            stri += str(year)
            stri += ".csv"
            df1 = pd.read_csv(stri)

            # Backfilling and frontfilling the data to make the graph more uniform 
            df1 = df1.fillna(method="backfill")
            df1 = df1.fillna(method="ffill")

            # Select box for selecting the quarter
            qtr = st.selectbox(
                'Select Quarter: ', ('Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4'))
            print(df1.__len__())

            # Finding the partition in the data to divide it into 4 parts
            tp = df1.__len__() // 4

            # Appropriate data is shown in graphs as per the quarter selected by the user
            if qtr == "Quarter 1":
                plotdata = df1.iloc[:, curr2_index + 1]
                plotdata = plotdata[0:tp]
            elif qtr == "Quarter 2":
                plotdata = df1.iloc[:, curr2_index + 1]
                plotdata = plotdata[tp:2 * tp]
            elif qtr == "Quarter 3":
                plotdata = df1.iloc[:, curr2_index + 1]
                plotdata = plotdata[2 * tp:3 * tp]
            elif qtr == "Quarter 4":
                plotdata = df1.iloc[:, curr2_index + 1]
                plotdata = plotdata[3 * tp:4 * tp]
            mx = max(plotdata.tolist())
            mn = min(plotdata.tolist())
            print(plotdata)
            st.line_chart(plotdata)

        elif option == "Yearly":
            dataset = []

            # Last value of the each year is taken into consideration while plotting the yearly trends on the second currency
            for i in range(2012, 2023):
                stri += str(i)
                df1 = pd.read_csv(stri + ".csv")
                df1 = df1.fillna(method="backfill")
                df1 = df1.fillna(method="ffill")
                dataset.append(df1.iloc[-1, curr2_index + 1])
                stri = "data/Exchange_Rate_Report_"
            print(dataset)
            mx = max(dataset)
            mn = min(dataset)
            st.line_chart(dataset)

    # Handling the condition when no input is given
    if mx != -1:
        st.write("Maximum rate: ", mx)
    if mn != -1:
        st.write("Minimum rate: ", mn)

st.subheader(
    "Designed by Amaan Mansuri, Bhavik Harkhani, Maitri Patel, Mokshil Shah and Vedant Mehta")
