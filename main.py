from nbp_api_caller import NBPApiCaller
from datetime import datetime, timedelta
from rate_analysis import RateAnalysis
import common

caller = NBPApiCaller()


data_range = "1 year"

end_date = datetime.now()
start_date = end_date - timedelta(days=common.DATA_RANGES[data_range])

raw_data = caller.fetch_exchange_rate("USD", "PLN", start_date, end_date)

print(raw_data)

analysis = RateAnalysis(raw_data)
statistics = analysis.calculate_statistics()
sessions = analysis.calculate_sessions()

print("Statistical Indicators:")
for key, value in statistics.items():
    print(f"  {key}: {value}")

print("\nSession Counts:")
for key, value in sessions.items():
    print(f"  {key}: {value}")
