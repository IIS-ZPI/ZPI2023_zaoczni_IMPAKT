import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self):
        pass

    def create_exchange_rates_plot(self, data, base_currency, quote_currency):
        plt.close('all')

        dates = [entry['date'] for entry in data]
        rates = [entry['rate'] for entry in data]

        fig, ax = plt.subplots(figsize=(5, 4))

        ax.plot(dates, rates, label=f'{base_currency}/{quote_currency}')
        ax.set_title(f'{base_currency}/{quote_currency}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Currency exchange rate')
        ax.legend(loc='upper left')
        ax.set_facecolor('#f2f2f2')
        ax.grid(True)

        num_dates = len(dates)
        min_ticks = 7

        step = max(1, num_dates // min_ticks) 
        step = min(step, num_dates - 1) 

        ax.set_xticks(dates[::step])
        ax.set_xticklabels(dates[::step], rotation=45)

        plt.tight_layout()

        return fig
    
    def create_currency_changes_hisogram(self, bins, frequency, base_currency, quote_currency):
        plt.close('all')

        bin_width = bins[1] - bins[0] if len(bins) > 1 else 1
        bin_edges = bins[:-1]
        bin_centers = [edge + bin_width / 2 for edge in bin_edges]

        fig, ax = plt.subplots(figsize=(6, 4))

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
