# A ship object is our way of defining a set of lineups generated by a user after submitting to optimization. I couldnt think of a better thing to call it. ShipIt is too hard to type (try it)

from slate import Slate



class Ship():
    def __init__(self, slate: Slate, n=10, *args, **kwargs):
        pass