

class Measure:
    def __init__(self, data):
        self.session = data[0]
        self.measure_point = data[1]

        self.load_data(data[2])

    def load_data(self, data):
        self.timings = data[1:-2]

        if data[-1] is not None:
            self.sub_calls = list()
            for d in data[-1]:
                self.sub_calls.append(Measure(d))

