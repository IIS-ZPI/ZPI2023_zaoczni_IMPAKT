from datetime import datetime
import numpy as np
import common

class DistributionAnalysis:
    def __init__(self, data):
      self.data = data

    def calculate_periodic_changes(self, report_type):
        """
        Calculates currency value changes over monthly or quarterly periods.

        Args:
            report_type (str): "monthly" or "quarterly".

        Returns:
            list: A list of value changes for the selected periods.
        """
        if report_type not in common.CURRENCY_CHANGES_HISTOGRAM_REPORT_TYPES:
            raise ValueError("Invalid report type. Use 'monthly' or 'quarterly'.")

        changes = []
        rates_by_date = {entry["date"]: entry["rate"] for entry in self.data}
        dates = sorted(rates_by_date.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))

        for i in range(0, len(dates)):
            start_date = dates[i]
            end_date = dates[len(dates) - 1]
            change = rates_by_date[end_date] - rates_by_date[start_date]
            changes.append(change)
        print(changes)
        return changes

    def calculate_changes_distribution(self, report_type):
        """
        Calculates the histogram distribution of currency value changes for monthly/quarterly periods.

        Args:
            report_type (str): "monthly" or "quarterly".
            intervals (int): Number of histogram intervals.

        Returns:
            dict: A dictionary with bins and their respective frequencies.
        """

        changes = self.calculate_periodic_changes(report_type=report_type)
        intervals = int(np.ceil(np.log2(len(changes)) + 1))  # Sturges' rule
        min_change, max_change = min(changes), max(changes)
        bins = np.linspace(min_change, max_change, intervals + 1)

        histogram, _ = np.histogram(changes, bins=bins)

        return {
            "bins": bins.tolist(),
            "frequency": histogram.tolist()
        }