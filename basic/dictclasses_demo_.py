class IRLight:
    def __init__(self, IRLuminosity=None, FullSpecLuminosity=None, VisibleLux=None):
        self.IRLuminosity = IRLuminosity
        self.FullSpecLuminosity = FullSpecLuminosity
        self.VisibleLux = VisibleLux


class Box:
    def __init__(self, irlight: IRLight, light=None, irled=None, speaker=None, result=None):
        self.irlight = IRLight(**irlight)
        self.light = light
        self.irled = irled
        self.speaker = speaker
        self.result = result


box_dict = {"light": "on",
            "irled": "off",
            "speaker": "off",
            "result": "True",
            "irlight": {"IRLuminosity": 4,
                        "FullSpecLuminosity": 47,
                        "VisibleLux": 618}}

box = Box(**box_dict)

box.irlight.FullSpecLuminosity


class OnOffDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, on=None, off=None):
        self.on = on
        self.off = off


class LightSensorLogDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # def __getstate__(self):
    #     return self

    # def __setstate__(self, state):
    #     self.update(state)

    def __init__(self, light_board: OnOffDict, light_sensor: OnOffDict):
        self.light_board = light_board
        self.light_sensor = light_sensor


log_dict = LightSensorLogDict(OnOffDict(), OnOffDict())
log_dict.light_board.off = False
log_dict["light_board"]['off']
assert log_dict["light_board"]['off'] == log_dict.light_board.off
temp = log_dict.light_board.pop("off")
temp