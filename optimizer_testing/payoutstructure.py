from slate import Slate
from lineup import Lineup



class Payout_Structure():
    def __init__(self, structure: dict):
        #structure will be defined as a key representing the first placing that achieves said payout. It is assumed that all placings between this and the next listed placing receive the same payout. For example if 300th place receives 4x their money, but the next defined payout is listed as 400th place receiving 3x their money, you can assume finishers in placement spots 300-399 received 4x.
        self.structure=structure

class Contest():
    def __init__(self, slate: Slate, lineups: list[Lineup], payout_structure: Payout_Structure):
        self.slate = slate
        self.lineups = lineups
        self.payout_structure = payout_structure

    def simulate_slate(self):
        sim = self.slate.simulate_slate()
        return sim