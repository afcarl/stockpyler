import GlobalManager

class Stockpyler:

    def __init__(self, live=False):
        self.gm = GlobalManager.GlobalManager(live)