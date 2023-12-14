from app import app
import yfinance as yf
def test_graph():
    ticker = "AAPL"
    symbol = yf.Ticker(ticker)
    df = symbol.history(period='1d', interval='1m')

    assert df['Open'].item
    assert df['High'].item
    assert df['Low'].item
    assert df['Close'].item
    assert df['Volume'].item
    assert df['Dividends'].item
    assert df['Stock Splits'].item