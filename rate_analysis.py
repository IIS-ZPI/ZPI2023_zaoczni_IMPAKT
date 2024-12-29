from statistics import median, mode, stdev, mean

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
