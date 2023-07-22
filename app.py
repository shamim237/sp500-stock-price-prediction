import os
import yfinance as yf
import pandas as pd
import streamlit as st

def download_and_save_data():
    # Load ticker_list from csv file
    ticker_data = pd.read_csv("s&p500_tickers_list.csv")

    ticker_list = ticker_data['Ticker'].tolist()

    ticker_lists = []
    for i in ticker_list:
        tickers = i.replace(".", "-")
        ticker_lists.append(tickers)

    data = yf.download(tickers=" ".join(ticker_lists), period="2y", interval="1h")

    data.index = pd.to_datetime(data.index)
    # Get the last date in the DataFrame
    last_date = data.index[-1].date()

    # Check if the last date has all seven hourly data points
    if len(data.loc[data.index.date == last_date]) == 7:
        # If it has all seven data points, keep the data
        pass
    else:
        # If it doesn't have all seven data points, remove the data for that date
        data = data.loc[data.index.date < last_date]

    # Separate data for each ticker
    ticker_columns = data.columns.get_level_values(1).unique()

    ticker_data = {}

    for ticker in ticker_columns:
        ticker_data[ticker] = data.loc[:, (slice(None), ticker)]

    # Reset column index for each ticker's DataFrame
    for ticker in ticker_data:
        ticker_data[ticker].columns = ticker_data[ticker].columns.droplevel(1)
        ticker_data[ticker].rename_axis('datetime', axis='index', inplace=True)

        # Save data for each ticker as a CSV file
        folder_path = 'stock-data'  # Replace 'stock-data' with the desired folder path
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f'{ticker}_stock_train_data.csv')
        ticker_data[ticker].to_csv(file_path)

    return folder_path

def main():
    st.title("Stock Data Downloader")

    if st.button("Download Data"):
        folder_path = download_and_save_data()
        st.success("Data downloaded successfully.")

if __name__ == "__main__":
    main()
