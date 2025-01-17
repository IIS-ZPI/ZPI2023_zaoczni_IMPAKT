import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

class Plotter:
    def __init__(self):
        pass

    def create_exchange_rates_plot(self, data, base_currency, quote_currency, statistics, sessions):
        plt.close('all')

        dates = [entry['date'] for entry in data]
        rates = [entry['rate'] for entry in data]

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(dates, rates)
        ax.set_title(f'{base_currency}/{quote_currency}')
        ax.set_xlabel('Date')
        ax.set_ylabel(f'{base_currency} price in {quote_currency}')
        ax.set_facecolor('#f2f2f2')
        ax.grid(True)

        self.display_text_boxes(ax, quote_currency, statistics, sessions)

        num_dates = len(dates)
        min_ticks = 7

        step = max(1, num_dates // min_ticks) 
        step = min(step, num_dates - 1) 

        ax.set_xticks(dates[::step])
        ax.set_xticklabels(dates[::step], rotation=45)
        ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        ax.ticklabel_format(style='plain', axis='y')

        # Stretch y axis by stretch_pct to get some area for textboxes
        stretch_pct = 0.25
        y_min, y_max = ax.get_ylim()
        margin = (y_max - y_min) * stretch_pct
        ax.set_ylim(y_min - margin, y_max + margin)
        
        plt.tight_layout()

        return fig
    
    def display_text_boxes(self, ax, quote_currency, statistics, sessions):
        # Add text box with statistics
        stats_text = f"Median: {statistics.get('median'):.6f} {quote_currency}\n" +\
            f"Mode: {statistics.get('mode'):.6f} {quote_currency}\n" +\
            f"Standard deviation: {statistics.get('standard_deviation'):.6f} {quote_currency}\n" +\
            f"Coefficient of variation: {statistics.get('coefficient_of_variation'):.6f} {quote_currency}"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="#f9f9f9"))
        
        
        # Add text box with sessions
        sessions_text = f"Sessions\n" +\
            f"Upward: {sessions.get('session_upward')}\n" +\
            f"Downward: {sessions.get('session_downward')}"
        ax.text(0.29, 0.98, sessions_text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="#f9f9f9"))
    
    def create_currency_changes_histogram_plot(self, bins, frequency, base_currency, quote_currency):
        plt.close('all')

        bin_width = bins[1] - bins[0] if len(bins) > 1 else 1
        bin_edges = bins[:-1]
        bin_centers = [edge + bin_width / 2 for edge in bin_edges]

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(bin_centers, frequency, width=bin_width, align='center', edgecolor='black')

        ax.set_ylabel('Changes frequency')
        ax.set_title(f'{base_currency}/{quote_currency} currency changes histogram')
        ax.set_facecolor('#f2f2f2')

        ax.grid(True)

        ax.set_xticks(bins)
        ax.set_xticklabels([f'{tick:.4f}' for tick in bins])
        ax.tick_params(axis='x', rotation=45)

        max_freq = max(frequency)
        y_max = int(np.ceil(max_freq / 2) * 2) + 2
        ax.set_ylim(0, y_max)
        ax.set_yticks(range(0, y_max + 1, 2))

        plt.tight_layout()

        return fig
