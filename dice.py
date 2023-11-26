import random
class Dice:
    def rollDie(self):
        """ 무작위 주사위의 값을 생성 """
        self.roll = random.randint(1, 6)

    def getRoll(self):
        """ 생성된 주사위의 값을 읽음 """
        return  self.roll