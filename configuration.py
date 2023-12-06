from collections import Counter

# 이 클래스는 주사위 눈에 따라 족보에 맞는 점수를 계산합니다. 생성자가 없는 클래스입니다.


class Configuration:
    configs = ["Category","Ones", "Twos","Threes","Fours","Fives","Sixes",
    "Upper Scores","Upper Bonus(35)","Three of a kind", "Four of a kind", "Full House(25)",
    "Small Straight(30)", "Large Straight(40)", "Yahtzee(50)","Chance","Lower Scores", "Total"]

    def score(row, d):
        """ row에 따라 주사위 점수를 계산하여 반환한다. 예를 들어 row가 0이면 "Ones"가 row가 2이면 "Threes"가 채점되어야 함을 의미한다.
        row가 주사위 점수와 관련 없는 버튼 (UpperScore, UpperBouns, LowerScore, Total 등)을 나타내면 -1을 반환한다.

        d는 주사위 5개의 눈을 담는 배열을 의미한다.
        """

        if 0 <= row < 6:
            return Configuration.scoreUpper(d, row + 1)
        elif row == 8:
            return Configuration.scoreThreeOfAKind(d)
        elif row == 9:
            return Configuration.scoreFourOfAKind(d)
        elif row == 10:
            return Configuration.scoreFullhouse(d)
        elif row == 11:
            return Configuration.scoreSmallStraight(d)
        elif row == 12:
            return Configuration.scoreLargeStraight(d)
        elif row == 13:
            return Configuration.scoreYahtzee(d)
        elif row == 14:
            return Configuration.sumDie(d)
        else:
            return -1

    def scoreUpper(d, num):
        """ num이 나온 주사위 눈의 총합을 계산한다. """
        sum = 0
        for i in range(5):
            if d[i].getRoll() == num:
                sum += num
        return sum

    def scoreThreeOfAKind(d):
        """ 동일한 주사위의 눈이 3개 이상일 때, 주사위 눈 5개의 합을 계산한다. """
        roll_counts = Counter([die.getRoll() for die in d])
        for roll, count in roll_counts.items():
            if count >= 3:
                return Configuration.sumDie(d)
        return 0

    def scoreFourOfAKind(d):
        """ 동일한 주사위의 눈이 4개 이상일 때, 주사위 눈 5개의 합을 계산한다. """
        roll_counts = Counter([die.getRoll() for die in d])
        for count in roll_counts.values():
            if count >= 4:
                return Configuration.sumDie(d)
        return 0

    def scoreFullhouse(d):
        """ 동일한 주사위 눈 한 종류가 3개, 다른 종류가 2개일 때, 주사위 눈 5개의 총합을 계산한다. """
        roll_counts = Counter([die.getRoll() for die in d])
        if 3 in roll_counts.values() and 2 in roll_counts.values():
            return 25
        return 0

    def scoreSmallStraight(d):
        """ 주사위 4개 이상의 눈이 이어지는 수일 때, 고정 30점 """
        tmp = [0 for _ in range(7)]
        for i in range(5):
            tmp[d[i].getRoll()] += 1
        for i in range(3):
            if tmp[i + 1] >= 1 and tmp[i + 2] >= 1 and tmp[i + 3] >= 1 and tmp[i + 4] >= 1:
                return 30
        return 0

    def scoreLargeStraight(d):
        """ 주사위 4개 이상의 눈이 이어지는 수일 때, 고정 40점 """
        tmp = [0 for _ in range(7)]
        for i in range(5):
            tmp[d[i].getRoll()] += 1
        for i in range(2):
            if tmp[i + 1] == 1 and tmp[i + 2] == 1 and tmp[i + 3] == 1 and tmp[i + 4] == 1 and tmp[i + 5] == 1:
                return 40
        return 0

    def scoreYahtzee(d):
        """ 주사위 5개의 눈이 모두 같을 때, 고정 50점 """
        if d[0].getRoll() == d[1].getRoll() == d[2].getRoll() == d[3].getRoll() == d[4].getRoll():
            return 50
        return 0

    def sumDie(d):
        """ 주사위 5개의 눈의 합을 구한다. """
        sum = 0
        for i in range(5):
            sum += d[i].getRoll()
        return sum

