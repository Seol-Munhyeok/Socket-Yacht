# 이 클래스는 플레이어에 관한 정보와 동작을 정의합니다.

class Player:
    # 사용자가 지정할 수 있는 카테고리의 개수를 나타내는 상수
    UPPER = 6
    LOWER = 7

    def __init__(self, name):
        self.name = name
        self.scores = [0 for i in range(self.UPPER + self.LOWER)]  # 13개의 카테고리 점수를 나타냄
        self.used = [False for i in range(self.UPPER + self.LOWER)]  # 각 카테고리의 사용 여부
        self.bonus = 0  # 보너스 점수 유무


    def setScore(self, score, index):
        """ 각 카테고리 별로 점수를 scores 리스트에 작성하는 함수 """
        self.scores[index] = score

    def setAtUsed(self, index):
        """ 13개 카테고리에 대해서 사용한 카테고리를 True로 변경하는 함수 """
        self.used[index] = True

    def getUpperScore(self):
        """ 상단의 카테고리가 모두 기입되면 그 합을 구하는 함수 """
        sum = 0
        for i in range(self.UPPER):
            sum += self.scores[i]
        self.upperScore = sum
        return self.upperScore

    def getLowerScore(self):
        """ 하단의 카테고리가 모두 기입되면 그 합을 구하는 함수 """
        sum = 0
        for i in range(self.LOWER):
            sum += self.scores[self.UPPER + i]
        self.lowerScore = sum
        return self.lowerScore

    def getUsed(self, index):
        """ used 카테고리 리스트를 가져오는 getter 함수 """
        return self.used[index]

    def getTotalScore(self):
        """ 13개 카테고리가 모두 사용되었을 때 총점을 가져오는 getter 함수 """
        sum = 0
        for i in range(self.LOWER + self.UPPER):
            sum += self.scores[i]
        self.totalScore = sum
        return self.totalScore

    def toString(self):
        """ 이름을 반환하는 함수 """
        return self.name

    def allLowerUsed(self):
        """ 하위 카테고리 7개가 모두 사용되었는지를 반환하는 함수 """
        for i in range(6, 13):
            if not self.used[i]:
                return False
        return True

    def allUpperUsed(self):
        """ 상위 카테고리 6개가 모두 사용되었는지를 반환하는 함수 """
        for i in range(self.UPPER):
            if not self.used[i]:
                return False
        return True
