import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

data = requests.get(
    "https://query1.finance.yahoo.com/v8/finance/chart/JPY=X?interval=1h&range=1d"
).json()

result = data["chart"]["result"][0]

prices = result["indicators"]["quote"][0]["close"]
highs = result["indicators"]["quote"][0]["high"]
lows = result["indicators"]["quote"][0]["low"]

prices = [p for p in prices if p is not None]
highs = [h for h in highs if h is not None]
lows = [l for l in lows if l is not None]

current = prices[-1]
previous = prices[-2]

change = current - previous
percent = (change / previous) * 100

high_day = max(highs)
low_day = min(lows)

ma5 = sum(prices[-5:]) / 5

diff_ma = current - ma5

if diff_ma >= 0.20:
    trend = "強い上昇"
elif diff_ma >= 0.05:
    trend = "上昇"
elif diff_ma <= -0.20:
    trend = "強い下降"
elif diff_ma <= -0.05:
    trend = "下降"
else:
    trend = "横ばい"

emoji = "🟢" if change >= 0 else "🔴"
sign = "+" if change >= 0 else ""

now = datetime.now(ZoneInfo("Asia/Tokyo"))

message = {
    "content":
        f"💱 USD/JPY\n\n"
        f"現在値: {current:.3f}\n\n"
        f"{emoji} 1時間変動: {sign}{change:.3f}円 ({sign}{percent:.2f}%)\n\n"
        f"本日高値: {high_day:.3f}\n"
        f"本日安値: {low_day:.3f}\n\n"
        f"5時間移動平均: {ma5:.3f}\n"
        f"{trend}\n\n"
        f"{now.strftime('%Y-%m-%d %H:%M JST')}"
}

requests.post(
    os.environ["DISCORD_WEBHOOK"],
    json=message
)
