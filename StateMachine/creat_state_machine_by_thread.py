import threading

from transitions.extensions import GraphMachine as Machine


class Model:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def on_enter_load(self):
        print(f"{self.name}_{self.id} {self.state} state ...")
        import time
        if self.id % 2 == 0:
            print(f"{self.name}_{self.id} {self.state} sleep ...")
            time.sleep(1)
        self.trigger("next")

    def on_enter_write_plc(self):
        print(f"{self.name}_{self.id} {self.state} state ...")
        self.trigger("next")

    def on_enter_wait_plc(self):
        print(f"{self.name}_{self.id} {self.state} state ...")
        self.trigger("next")

    def on_enter_end(self):
        print(f"{self.name}_{self.id} {self.state} state ...")
        # self.trigger("next") 接回去會無窮迴圈


class ModelThreading(threading.Thread):

    def __init__(self, station_id):
        threading.Thread.__init__(self)
        self.station_id = station_id
        self.model = Model(self.name, station_id)
        self.machine = Machine(model=self.model,
                               states=[
                                   'start',
                                   'load',
                                   'write_plc',
                                   'wait_plc',
                                   'end',
                               ],
                               transitions=[
                                   {'trigger': 'next', 'source': 'start', 'dest': 'load'},
                                   {'trigger': 'next', 'source': 'load', 'dest': 'write_plc'},
                                   {'trigger': 'next', 'source': 'write_plc', 'dest': 'wait_plc'},
                                   {'trigger': 'next', 'source': 'wait_plc', 'dest': 'end'}
                               ],
                               initial='start',
                               show_conditions=True)

    def run(self):
        print(f"{self.name}_{self.station_id} run ...")
        self.model.trigger("next")


if __name__ == "__main__":
    machines = []
    for i in range(5):
        machines.append(ModelThreading(i))
        machines[i].start()

'''
Thread-1_0 run ...
Thread-1_0 load state ...
Thread-1_0 load sleep ...
Thread-2_1 run ...
Thread-2_1 load state ...
Thread-2_1 write_plc state ...
Thread-2_1 wait_plc state ...
Thread-2_1 end state ...
Thread-3_2 run ...
Thread-3_2 load state ...
Thread-3_2 load sleep ...
Thread-4_3 run ...
Thread-4_3 load state ...
Thread-4_3 write_plc state ...
Thread-4_3 wait_plc state ...
Thread-4_3 end state ...
Thread-5_4 run ...
Thread-5_4 load state ...
Thread-5_4 load sleep ...
Thread-1_0 write_plc state ...
Thread-1_0 wait_plc state ...
Thread-1_0 end state ...
Thread-3_2 write_plc state ...
Thread-3_2 wait_plc state ...
Thread-3_2 end state ...
Thread-5_4 write_plc state ...
Thread-5_4 wait_plc state ...
Thread-5_4 end state ...
'''
