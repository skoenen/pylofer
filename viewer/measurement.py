

class Measure:
    def __init__(self, data):
        self.id = data['measure_id']
        self.session = data['measure_session']
        self.point = data['measure_point']
        self.code = data['code']
        self.call_count = data['call_count']
        self.recursive_call_count = data['recursive_call_count']
        self.time_total = data['time_total']
        self.time_function = data['time_function']

        self.time_per_call = data['time_function'] / data['call_count']
        self.time_other = data['time_total'] - data['time_function']

        self.subcalls = []
        self.categories = []

    def add_subcalls(self, data):
        for sc in data:
            self.subcalls.append(Measure(sc))

