import random
# 이 클래스는 주사위를 던지는 동작을 정의합니다.


class Dice:
    def rollDie(self):
        """ 무작위 주사위의 값을 생성 """
        self.roll = random.randint(1, 6)

    def getRoll(self):
        """ 생성된 주사위의 값을 읽음 """
        return  self.roll