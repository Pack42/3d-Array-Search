class KeyManager:

    def __init__(self, major, step, leap, instrument):
        self.major = major
        self.steps = [0, 2, 4, 5, 7, 9, 11]
        self.step = step
        self.leap = leap
        self.instrument = instrument
        if not self.major:
            self.steps[2] = 3
            self.steps[5] = 8
            self.steps[6] = 10

    def key_from_position(self,x,y,z):
        key = (self.leap * y + self.steps[((x * self.step) % 7)] + z * 12) % 47
        return "Key Samples/" + self.instrument + "/" + str(key) + ".wav"