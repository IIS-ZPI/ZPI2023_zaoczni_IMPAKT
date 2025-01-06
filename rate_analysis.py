from statistics import median, mode, stdev, mean
from datetime import datetime
import numpy as np

class RateAnalysis:
    def __init__(self, data):
        self.data = data

    def calculate_statistics(self):
        rates = [entry['rate'] for entry in self.data]

        statistics = {
            'median': median(rates),
            'mode': mode(rates),
            'standard_deviation': stdev(rates),
            'coefficient_of_variation': (stdev(rates) / mean(rates)) * 100
        }
        return statistics

    def calculate_sessions(self):
        upward = 0
        downward = 0

        for i in range(1, len(self.data)):
            if self.data[i]['rate'] > self.data[i - 1]['rate']:
                upward += 1
            elif self.data[i]['rate'] < self.data[i - 1]['rate']:
                downward += 1

        sessions = {
            'session_upward': upward,
            'session_downward': downward
        }
        return sessions

    def calculate_periodic_changes(self, report_type):
        """
        Calculates currency value changes over monthly or quarterly periods.

        Args:
            report_type (str): "monthly" or "quarterly".

        Returns:
            list: A list of value changes for the selected periods.
        """
        if report_type not in ["monthly", "quarterly"]:
            raise ValueError("Invalid report type. Use 'monthly' or 'quarterly'.")

        changes = []
        rates_by_date = {entry["date"]: entry["rate"] for entry in self.data}
        dates = sorted(rates_by_date.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))

        step = 30 if report_type == "monthly" else 91

        for i in range(0, len(dates) - step, step):
            start_date = dates[i]
            end_date = dates[i + step]
            change = rates_by_date[end_date] - rates_by_date[start_date]
            changes.append(change)

        return changes

    def calculate_changes_distribution(self, report_type, intervals):
        """
        Calculates the histogram distribution of currency value changes for monthly/quarterly periods.

        Args:
            report_type (str): "monthly" or "quarterly".
            intervals (int): Number of histogram intervals.

        Returns:
            dict: A dictionary with bins and their respective frequencies.
        """
        changes = self.calculate_periodic_changes(report_type=report_type)
        min_change, max_change = min(changes), max(changes)
        bins = np.linspace(min_change, max_change, intervals + 1)

        histogram, _ = np.histogram(changes, bins=bins)

        return {
            "bins": bins.tolist(),
            "frequency": histogram.tolist()
        }