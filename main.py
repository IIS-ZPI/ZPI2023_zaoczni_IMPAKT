from nbp_api_caller import NBPApiCaller
from datetime import datetime, timedelta
from rate_analysis import RateAnalysis
from distribution_analysis import DistributionAnalysis
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

start_date_distribution = datetime(2023, 2, 6)
data_range_distribution = "1 quarter"

if data_range_distribution == "1 quarter":
    report_type = common.DEFAULT_CURRENCY_CHANGES_HISTOGRAM_REPORT_TYPE 
else:
    report_type = common.CURRENCY_CHANGES_HISTOGRAM_REPORT_TYPES[1]


end_date_distribution = start_date_distribution + timedelta(days=common.DATA_RANGES[data_range_distribution])

if end_date_distribution > datetime.now():
    raise ValueError("End date cannot be in the future.")
else:
    raw_data_distribution = caller.fetch_exchange_rate("USD", "PLN", start_date_distribution, end_date_distribution)

    distribution_analysis = DistributionAnalysis(raw_data_distribution)
    distribution = distribution_analysis.calculate_changes_distribution(report_type)

    print("\nDistribution of currency value changes:")
    for key, value in distribution.items():
        print(f"  {key}: {value}")