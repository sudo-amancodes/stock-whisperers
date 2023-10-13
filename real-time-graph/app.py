import yfinance as yf
import matplotlib.pyplot as plt

# Set the start and end dates
start_date = "2023-10-13 10:00:00"
end_date = "2023-10-13 10:10:00"

# Get the ticker symbol for the stock you want to track
ticker = "AAPL"

# Get the historical data for the stock
df = yf.download(ticker, start_date, end_date, interval="10m")

# Plot the data
plt.plot(df["Close"])

# Add a legend to the graph
plt.legend([ticker], loc="upper left")

# Change the line color to blue
plt.plot(df["Close"], color="blue")

# Add a grid to the graph
plt.grid(True)

# Change the axis labels
plt.xlabel("Time (PST)")
plt.ylabel("Price (USD)")

# Change the title of the graph
plt.title("Current Market for {} on 2023-10-13".format(ticker))

# Show the graph
plt.show()