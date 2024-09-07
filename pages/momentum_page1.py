#OVERVIEW PAGE
import streamlit as st
import csv
import pandas as pd
import plotly.express as px

from trading_system.momentum_strategy import MomentumStrategy
from trading_system.momentum_backtesting import MomentumBacktesting

# Path to the CSV file
csv_file_path = 'sp500_symbols.csv'

#creating average scores df
symbols_df = pd.read_csv('sp500_symbols.csv')
df = pd.DataFrame(index=symbols_df['Symbol'], columns=['7_days', '30_days', '90_days'])

def process_time_frame_results(results_df):
    # Group the results by 'Time Frame'
    time_frame_groups = results_df.groupby('Time Frame')
    # Dictionary to store DataFrames and average scores for each time frame
    time_frame_data = {}

    for time_frame, group in time_frame_groups:
        # Store each group as a separate DataFrame for the specific time frame
        time_frame_data[time_frame] = group

        # Calculate and print the average score for the current time frame
        average_score = group['Score'].mean()
        # print(f"Average Score for {time_frame}-day time frame: {average_score:.2f}")

        # Optionally, you could return or store the averages for further use
        time_frame_data[time_frame]['Average Score'] = average_score

    return time_frame_data
count = 0
# Open the CSV file and iterate through each ticker
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        symbol = row['Symbol']
        print(f"Processing ticker: {symbol}")
        count += 1
        results_df = pd.DataFrame()
        # Here, you can add any additional processing for each ticker
        try:
            strategy = MomentumStrategy(symbol, "2010-01-01", "2024-01-01")
            strategy.download_data(symbol, "2010-01-01", "2024-01-01" )
            if strategy.data.empty:
                print("Data download didnt work")
                continue

            strategy.calculate_indicators()
            strategy.generate_signals()
            strategy_backtest = MomentumBacktesting(strategy=strategy, initial_capital=10000)
            strategy_backtest.run_backtest()
            results_df = strategy_backtest.scoring()


            # print("this is results_df")
            # print(results_df)
            if results_df.empty:
                print(f"Results for {symbol} are empty, investigating why...")
                # Optionally, stop skipping and see if there are any unusual values
                continue
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue
        average_score_7_days = results_df.loc[results_df['Time Frame'] == 7, 'Score'].mean()
        average_score_30_days = results_df.loc[results_df['Time Frame'] == 30, 'Score'].mean()
        average_score_90_days = results_df.loc[results_df['Time Frame'] == 90, 'Score'].mean()
        # print(average_score_7_days)
        # print(average_score_30_days)
        # print(average_score_90_days)
        df.loc[symbol] = [average_score_7_days, average_score_30_days, average_score_90_days]
        print(count)
        if count >= 20:
            print(f"Breaking the loop after processing {50} companies.")
            break
        # print(df)
        # Call the function and store the results
        time_frame_results = process_time_frame_results(results_df)
        # print("This is tfr")
        # print(time_frame_results)
        # # Example: Accessing the 7-day time frame DataFrame
        # df_7_day = time_frame_results[7]
        # print(df_7_day.head())  # Display first few rows for the 7-day time frame
        #
        # # Example: Accessing the 30-day time frame DataFrame
        # df_30_day = time_frame_results[30]
        # print(df_30_day.head())  # Display first few rows for the 30-day time frame
        #
        # # Example: Accessing the 90-day time frame DataFrame
        # df_90_day = time_frame_results[90]
        # print(df_90_day.head())  # Display first few rows for the 90-day time frame

        # strategy_backtest.plot_indicators()

# Find the top 10 companies for each time frame

# Fill NaN values with 0
df['7_days'] = df['7_days'].fillna(0).round().astype(int)
df['30_days'] = df['30_days'].fillna(0).round().astype(int)
df['90_days'] = df['90_days'].fillna(0).round().astype(int)


df['7_days'] = df['7_days'].round().astype(int)
df['30_days'] = df['30_days'].round().astype(int)
df['90_days'] = df['90_days'].round().astype(int)

top_3_7_days = df['7_days'].nlargest(10)
top_3_30_days = df['30_days'].nlargest(10)
top_3_90_days = df['90_days'].nlargest(10)

print("Top 3 companies for 7 days:")
print(top_3_7_days)

print("Top 3 companies for 30 days:")
print(top_3_30_days)

print("Top 3 companies for 90 days:")
print(top_3_90_days)

# Create weights based on the 7-day, 30-day, and 90-day scores
df['weight_7_days'] = (df['7_days'] / df['7_days'].sum()).nlargest(10)
df['weight_30_days'] = (df['30_days'] / df['30_days'].sum()).nlargest(10)
df['weight_90_days'] = (df['90_days'] / df['90_days'].sum()).nlargest(10)

top_10_7_days = df['weight_7_days'].nlargest(10)
top_10_30_days = df['weight_30_days'].nlargest(10)
top_10_90_days = df['weight_90_days'].nlargest(10)

print(df['weight_7_days'])
print(top_10_7_days)
# Print the weights for the first few rows
print(df[['weight_7_days', 'weight_30_days', 'weight_90_days']])


st.set_page_config(layout="wide")
st.title("Momentum Strategy Overview")

import streamlit as st
import plotly.express as px

col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    tile1 = col1.container()
    tile1.subheader("Description")
    st.write("Brief description of what is happening")

with col2:
    tile2 = col2.container()
    tile2.subheader("7 Days")
    fig1 = px.pie(values=top_10_7_days.values, names=top_10_7_days.index)
    fig1.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend at the bottom
            y=-0.5,  # Move legend downwards
            xanchor="center",  # Center the legend
            x=0.5  # Align legend horizontally to the center of the chart
        )
    )
    st.plotly_chart(fig1)

with col3:
    tile3 = col3.container()
    tile3.subheader("30 Days")
    fig2 = px.pie(values=top_10_30_days.values, names=top_10_30_days.index)
    fig2.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend at the bottom
            y=-0.5,  # Move legend downwards
            xanchor="center",  # Center the legend
            x=0.5  # Align legend horizontally to the center of the chart
        )
    )
    st.plotly_chart(fig2)

with col4:
    tile4 = col4.container()
    tile4.subheader("90 Days")
    fig3 = px.pie(values=top_10_90_days.values, names=top_10_90_days.index)
    fig3.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend at the bottom
            y=-0.5,  # Move legend downwards
            xanchor="center",  # Center the legend
            x=0.5  # Align legend horizontally to the center of the chart
        )
    )
    st.plotly_chart(fig3)

# Assuming df is your DataFrame with tickers and weights

# Display pie chart in Streamlit
