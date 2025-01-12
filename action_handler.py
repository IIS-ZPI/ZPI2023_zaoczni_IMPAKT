from nbp_api_caller import NBPApiCaller
from datetime import datetime, timedelta
from rate_analysis import RateAnalysis
from distribution_analysis import DistributionAnalysis
import common

class ActionHandler:
    def __init__(self, plotter):
        self.plotter = plotter
        self.interface = None
        self.NBPApiCaller = NBPApiCaller()

    def set_interface(self, interface):
        self.interface = interface

    def handle_create_market_analysis(self, base_currency, quote_currency, data_range):
        """
        This function is called on "SUBMIT" button click on "Market Analysis" widget.
        """

        end_date = datetime.now()
        start_date = end_date - timedelta(days=common.DATA_RANGES[data_range])

        try:
            raw_data = self.NBPApiCaller.fetch_exchange_rate(base_currency, quote_currency, start_date, end_date)
        except Exception as e:
            self.interface.show_error_message("Invalid input", str(e))
            return
        

        # TODO: preprocess raw_data if needed, get statistical data and pass them to plotter

        plot_data = self.plotter.create_exchange_rates_plot(raw_data, base_currency, quote_currency)

        self.interface.update_plot(plot_data)


    def handle_create_currency_changes_histogram(self, base_currency, quote_currency, start_date, report_type):
        """
        This function is called on "SUBMIT" button click on "Currency Changes Histogram" widget.
        """
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = start_date + timedelta(days=common.CURRENCY_CHANGES_HISTOGRAM_REPORT_TYPES[report_type])

        try:
            raw_data = self.NBPApiCaller.fetch_exchange_rate(base_currency, quote_currency, start_date, end_date)
        except Exception as e:
            self.interface.show_error_message("Invalid input", str(e))
            return
        
        distribution_analysis = DistributionAnalysis(raw_data)
        distribution = distribution_analysis.calculate_changes_distribution(report_type)

        plot_data = self.plotter.create_currency_changes_histogram_plot(distribution['bins'], distribution['frequency'], base_currency, quote_currency)

        self.interface.update_plot(plot_data)

        