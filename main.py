class Position:
    def __init__(self, who_wins=-1, when_wins=-1, winning_score=0):
        self.who_wins = who_wins  # 2 - это ничья
        self.when_wins = when_wins
        self.winning_score = winning_score
        self.good_moves = []
        self.catching_the_take = -1
        self.catching_the_transmission = -1
        self.opponents_moves = {}


class OdnomastkaDurak:
    def __init__(self, cards, player):  # cards - текущие карты в формате массива
        self.moves_tree = {}  # уже просчитанные позиции
        self.pole = -1  # карта лежащая на столе
        self.cards = 0  # текущие карты в формате числа
        self.size = len(cards)
        self.reverse = 0
        self.now_player = player
        self.names_of_cards = [i for i in range(1, self.size + 1)]
        for i in range(self.size):
            self.cards += cards[i] * (2 ** i)
        self.cards += 2 ** self.size  # обозначает начало
        if player == 1:
            self.change_player()  # теперь считаем, что первый ходит игрок 0
        self.build_moves_tree()

    def who_wins(self):
        return (self.moves_tree[self.cards].who_wins + self.reverse) % 2

    def when_wins(self):
        return self.moves_tree[self.cards].when_wins

    def winning_score(self):
        return self.moves_tree[self.cards].winning_score

    def has_player_position(self, pos, player):
        return (2 ** pos) & self.cards == player * (2 ** pos)

    def change_player(self):
        self.cards = (2 ** self.size - 1) ^ self.cards
        self.reverse = (self.reverse + 1) % 2

    def remove(self, pos1, pos2):
        if pos1 < pos2:
            pos1, pos2 = pos2, pos1
        self.cards = self.cards % (2 ** pos1) + ((self.cards // (2 ** (pos1 + 1))) << pos1)
        self.cards = self.cards % (2 ** pos2) + ((self.cards // (2 ** (pos2 + 1))) << pos2)
        self.size -= 2

    def add(self, pos, player):
        self.cards = self.cards % (2 ** pos) + player * (2 ** pos) + ((self.cards // (2 ** pos)) << (pos + 1))
        self.size += 1

    def change_position(self, pos):
        if (2 ** pos) & self.cards == 0:
            self.cards += 2 ** pos
        else:
            self.cards -= 2 ** pos

    def is_end(self):
        return (self.cards == 2 ** self.size or self.cards == (2 ** (self.size + 1) - 1))

    def move_by_computer(self):
        if self.moves_tree.get(self.cards) is None:
            self.build_moves_tree()
        if self.is_end():
            return -1  # игра окончена
        if self.pole == -1:
            self.now_player = (self.now_player + 1) % 2
            if self.moves_tree[self.cards].catching_the_take != -1:
                self.pole = self.moves_tree[self.cards].catching_the_take
                return self.moves_tree[self.cards].catching_the_take + 1
            elif self.moves_tree[self.cards].catching_the_transmission != -1:
                self.pole = self.moves_tree[self.cards].catching_the_transmission
                return self.moves_tree[self.cards].catching_the_transmission + 1
            else:
                self.pole = self.moves_tree[self.cards].good_moves[0]
                return self.moves_tree[self.cards].good_moves[0] + 1
        else:
            t = self.pole
            self.pole = -1
            res = self.moves_tree[self.cards].opponents_moves[t]
            if res == t:
                self.now_player = (self.now_player + 1) % 2
                self.change_position(res)
                return res + 1
            self.remove(res, t)
            self.names_of_cards.remove(self.names_of_cards[res])
            self.names_of_cards.remove(self.names_of_cards[t])
            self.change_player()
            return res + 1

    def move_by_player(self, pos):  # код ошибки -1, pos=-1 значит принять карту
        if self.is_end():
            return -1  # игра окончена
        if pos == -1:
            if self.pole == -1:
                return -1
            else:
                self.now_player = (self.now_player+1)%2
                self.change_position(self.pole)
                self.pole = -1
        else:
            pos -= 1
            if self.pole == -1:
                if not self.has_player_position(pos, 0):
                    return -1
                self.pole = pos
                self.now_player = (self.now_player+1)%2
            else:
                if (not self.has_player_position(pos, 1)) or pos <= self.pole:
                    return -1
                self.remove(self.pole, pos)
                self.names_of_cards.remove(self.names_of_cards[pos])
                self.names_of_cards.remove(self.names_of_cards[self.pole])
                self.pole = -1
                self.change_player()
        return 0

    def write_position(self, p, pole, is_catching, protection):
        self.moves_tree[self.cards].who_wins = p.who_wins
        self.moves_tree[self.cards].when_wins = p.when_wins
        self.moves_tree[self.cards].winning_score = p.winning_score
        self.moves_tree[self.cards].catching_the_transmission = -1
        self.moves_tree[self.cards].catching_the_take = -1
        self.moves_tree[self.cards].good_moves = [pole]
        if is_catching and self.moves_tree[self.cards].opponents_moves[pole] == protection:
            self.moves_tree[self.cards].catching_the_transmission = pole
        elif is_catching and self.moves_tree[self.cards].opponents_moves[pole] == pole:
            self.moves_tree[self.cards].catching_the_take = pole

    def build_moves_tree_opponent(self):
        pole = self.pole
        self.change_position(pole)
        self.pole = -1
        self.build_moves_tree()
        take = self.cards
        transmission = take
        who_wins_take = self.moves_tree[take].who_wins
        who_wins_transmission = who_wins_take
        self.change_position(pole)
        protection = pole  # карта защиты
        while protection < self.size and self.has_player_position(protection, 0):
            protection += 1
        if protection != self.size:
            self.remove(pole, protection)
            self.change_player()  # из-за этого ответ кто выиграл для этого случая будет обратный
            transmission = self.cards
            self.build_moves_tree()
            self.change_player()
            self.add(pole, 0)
            self.add(protection, 1)
            who_wins_transmission = (self.moves_tree[transmission].who_wins + 1) % 2
        p = Position()  # что получится после этого хода
        is_catching = True
        if who_wins_take == 0 and who_wins_transmission == 1:
            p = Position(1, self.moves_tree[transmission].when_wins + 1, self.moves_tree[transmission].winning_score)
            self.moves_tree[self.cards].opponents_moves[pole] = protection
        elif who_wins_take == 1 and who_wins_transmission == 0:
            p = Position(1, self.moves_tree[take].when_wins + 1, self.moves_tree[take].winning_score)
            self.moves_tree[self.cards].opponents_moves[pole] = pole
        elif who_wins_take == 1 and who_wins_transmission == 1:
            p.who_wins = 1
            if self.moves_tree[take].winning_score > self.moves_tree[transmission].winning_score:
                p.winning_score = self.moves_tree[take].winning_score
                p.when_wins = self.moves_tree[take].when_wins + 1
                self.moves_tree[self.cards].opponents_moves[pole] = pole
            elif self.moves_tree[take].winning_score < self.moves_tree[transmission].winning_score:
                p.when_wins = self.moves_tree[transmission].when_wins + 1
                p.winning_score = self.moves_tree[transmission].winning_score
                self.moves_tree[self.cards].opponents_moves[pole] = protection
            else:
                p.winning_score = self.moves_tree[transmission].winning_score
                if self.moves_tree[transmission].when_wins < self.moves_tree[take].when_wins:
                    p.when_wins = self.moves_tree[transmission].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = protection
                else:
                    p.when_wins = self.moves_tree[take].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = pole
                if self.moves_tree[transmission].when_wins == self.moves_tree[take].when_wins:
                    is_catching = False
        elif who_wins_take == 0 and who_wins_transmission == 0:
            p.who_wins = 0
            if self.moves_tree[take].winning_score < self.moves_tree[transmission].winning_score:
                p.winning_score = self.moves_tree[take].winning_score
                p.when_wins = self.moves_tree[take].when_wins + 1
                self.moves_tree[self.cards].opponents_moves[pole] = pole
            elif self.moves_tree[take].winning_score > self.moves_tree[transmission].winning_score:
                p.when_wins = self.moves_tree[transmission].when_wins + 1
                p.winning_score = self.moves_tree[transmission].winning_score
                self.moves_tree[self.cards].opponents_moves[pole] = protection
            else:
                p.winning_score = self.moves_tree[transmission].winning_score
                if self.moves_tree[transmission].when_wins > self.moves_tree[take].when_wins:
                    p.when_wins = self.moves_tree[transmission].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = protection
                else:
                    p.when_wins = self.moves_tree[take].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = pole
                if self.moves_tree[transmission].when_wins == self.moves_tree[take].when_wins:
                    is_catching = False
        if self.moves_tree[self.cards].who_wins == -1 or (
                self.moves_tree[self.cards].who_wins == 1 and p.who_wins == 0):
            self.write_position(p, pole, is_catching, protection)
        elif self.moves_tree[self.cards].who_wins == 0 and p.who_wins == 0:
            if self.moves_tree[self.cards].winning_score < p.winning_score:
                self.write_position(p, pole, is_catching, protection)
            elif self.moves_tree[self.cards].winning_score == p.winning_score:
                if self.moves_tree[self.cards].when_wins > p.when_wins:
                    self.write_position(p, pole, is_catching, protection)
                elif self.moves_tree[self.cards].when_wins == p.when_wins:
                    self.moves_tree[self.cards].good_moves.append(pole)
                    if is_catching and self.moves_tree[self.cards].opponents_moves[pole] == protection:
                        self.moves_tree[self.cards].catching_the_transmission = pole
                    elif is_catching and self.moves_tree[self.cards].opponents_moves[pole] == pole and \
                            self.moves_tree[self.cards].catching_the_take == -1:
                        self.moves_tree[self.cards].catching_the_take = pole
        elif self.moves_tree[self.cards].who_wins == 1 and p.who_wins == 1:
            if self.moves_tree[self.cards].winning_score > p.winning_score:
                self.write_position(p, pole, is_catching, protection)
            elif self.moves_tree[self.cards].winning_score == p.winning_score:
                if self.moves_tree[self.cards].when_wins < p.when_wins:
                    self.write_position(p, pole, is_catching, protection)
                elif self.moves_tree[self.cards].when_wins == p.when_wins:
                    self.moves_tree[self.cards].good_moves.append(pole)
                    if is_catching and self.moves_tree[self.cards].opponents_moves[pole] == protection:
                        self.moves_tree[self.cards].catching_the_transmission = pole
                    elif is_catching and self.moves_tree[self.cards].opponents_moves[pole] == pole and \
                            self.moves_tree[self.cards].catching_the_take == -1:
                        self.moves_tree[self.cards].catching_the_take = pole

    def build_moves_tree(self):
        if not self.moves_tree.get(self.cards) is None:
            return
        if self.cards == 2 ** self.size:  # проверить случай ничьи 01
            self.moves_tree[self.cards] = Position(1, 0, self.size)
            return
        if self.cards == (2 ** (self.size + 1) - 1):
            self.moves_tree[self.cards] = Position(0, 0, self.size)
            return
        self.moves_tree[self.cards] = Position()
        for i in range(self.size):
            if self.has_player_position(i, 0):
                self.pole = i
                self.build_moves_tree_opponent()
        self.pole = -1

    def print(self):
        copy_cards = self.cards
        cards = [0] * self.size
        i = 0
        while copy_cards != 0 and i < self.size:
            cards[i] = (copy_cards % 2 + self.reverse) % 2
            copy_cards //= 2
            i += 1
        if self.pole == -1:
            print(cards)
        else:
            print(self.pole + 1, cards)


class OdnomastkaD_Durak(OdnomastkaDurak):
    def who_wins(self):
        if self.moves_tree[self.cards].who_wins == 2:
            return 2
        return (self.moves_tree[self.cards].who_wins + self.reverse) % 2

    def build_moves_tree_opponent(self):
        pole = self.pole
        self.change_position(pole)
        self.pole = -1
        self.build_moves_tree()
        take = self.cards
        transmission = take
        who_wins_take = self.moves_tree[take].who_wins
        who_wins_transmission = who_wins_take
        self.change_position(pole)
        protection = pole  # карта защиты
        while protection < self.size and self.has_player_position(protection, 0):
            protection += 1
        if protection != self.size:
            self.remove(pole, protection)
            self.change_player()  # из-за этого ответ кто выиграл для этого случая будет обратный
            transmission = self.cards
            self.build_moves_tree()
            self.change_player()
            self.add(pole, 0)
            self.add(protection, 1)
            who_wins_transmission = (self.moves_tree[transmission].who_wins + 1) % 2
            if self.moves_tree[transmission].who_wins == 2:
                who_wins_transmission = 2
        p = Position()  # что получится после этого хода
        is_catching = True
        if (who_wins_take == 0 or who_wins_take == 2) and who_wins_transmission == 1:
            p = Position(1, self.moves_tree[transmission].when_wins + 1, self.moves_tree[transmission].winning_score)
            self.moves_tree[self.cards].opponents_moves[pole] = protection
        elif who_wins_take == 0 and who_wins_transmission == 2:
            p = Position(2, -1, 0)
            self.moves_tree[self.cards].opponents_moves[pole] = protection
        elif who_wins_take == 1 and (who_wins_transmission == 0 or who_wins_transmission == 2):
            p = Position(1, self.moves_tree[take].when_wins + 1, self.moves_tree[take].winning_score)
            self.moves_tree[self.cards].opponents_moves[pole] = pole
        elif who_wins_take == 2 and who_wins_transmission == 0:
            p = Position(2, -1, 0)
            self.moves_tree[self.cards].opponents_moves[pole] = pole
        elif who_wins_take == 1 and who_wins_transmission == 1:
            p.who_wins = 1
            if self.moves_tree[take].winning_score > self.moves_tree[transmission].winning_score:
                p.winning_score = self.moves_tree[take].winning_score
                p.when_wins = self.moves_tree[take].when_wins + 1
                self.moves_tree[self.cards].opponents_moves[pole] = pole
            elif self.moves_tree[take].winning_score < self.moves_tree[transmission].winning_score:
                p.when_wins = self.moves_tree[transmission].when_wins + 1
                p.winning_score = self.moves_tree[transmission].winning_score
                self.moves_tree[self.cards].opponents_moves[pole] = protection
            else:
                p.winning_score = self.moves_tree[transmission].winning_score
                if self.moves_tree[transmission].when_wins < self.moves_tree[take].when_wins:
                    p.when_wins = self.moves_tree[transmission].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = protection
                else:
                    p.when_wins = self.moves_tree[take].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = pole
                if self.moves_tree[transmission].when_wins == self.moves_tree[take].when_wins:
                    is_catching = False
        elif who_wins_take == 0 and who_wins_transmission == 0:
            p.who_wins = 0
            if self.moves_tree[take].winning_score < self.moves_tree[transmission].winning_score:
                p.winning_score = self.moves_tree[take].winning_score
                p.when_wins = self.moves_tree[take].when_wins + 1
                self.moves_tree[self.cards].opponents_moves[pole] = pole
            elif self.moves_tree[take].winning_score > self.moves_tree[transmission].winning_score:
                p.when_wins = self.moves_tree[transmission].when_wins + 1
                p.winning_score = self.moves_tree[transmission].winning_score
                self.moves_tree[self.cards].opponents_moves[pole] = protection
            else:
                p.winning_score = self.moves_tree[transmission].winning_score
                if self.moves_tree[transmission].when_wins > self.moves_tree[take].when_wins:
                    p.when_wins = self.moves_tree[transmission].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = protection
                else:
                    p.when_wins = self.moves_tree[take].when_wins + 1
                    self.moves_tree[self.cards].opponents_moves[pole] = pole
                if self.moves_tree[transmission].when_wins == self.moves_tree[take].when_wins:
                    is_catching = False
        elif who_wins_take == 2 and who_wins_transmission == 2:
            p = Position(2, -1, 0)
            self.moves_tree[self.cards].opponents_moves[pole] = pole
            is_catching = False
        if self.moves_tree[self.cards].who_wins == -1 or (
                self.moves_tree[self.cards].who_wins == 1 and (p.who_wins == 0 or p.who_wins == 2)) or (
                self.moves_tree[self.cards].who_wins == 2 and p.who_wins == 0):
            self.write_position(p, pole, is_catching, protection)
        elif self.moves_tree[self.cards].who_wins == 0 and p.who_wins == 0:
            if self.moves_tree[self.cards].winning_score < p.winning_score:
                self.write_position(p, pole, is_catching, protection)
            elif self.moves_tree[self.cards].winning_score == p.winning_score:
                if self.moves_tree[self.cards].when_wins > p.when_wins:
                    self.write_position(p, pole, is_catching, protection)
                elif self.moves_tree[self.cards].when_wins == p.when_wins:
                    self.moves_tree[self.cards].good_moves.append(pole)
                    if is_catching and self.moves_tree[self.cards].opponents_moves[pole] == protection:
                        self.moves_tree[self.cards].catching_the_transmission = pole
                    elif is_catching and self.moves_tree[self.cards].opponents_moves[pole] == pole and \
                            self.moves_tree[self.cards].catching_the_take == -1:
                        self.moves_tree[self.cards].catching_the_take = pole
        elif self.moves_tree[self.cards].who_wins == 1 and p.who_wins == 1:
            if self.moves_tree[self.cards].winning_score > p.winning_score:
                self.write_position(p, pole, is_catching, protection)
            elif self.moves_tree[self.cards].winning_score == p.winning_score:
                if self.moves_tree[self.cards].when_wins < p.when_wins:
                    self.write_position(p, pole, is_catching, protection)
                elif self.moves_tree[self.cards].when_wins == p.when_wins:
                    self.moves_tree[self.cards].good_moves.append(pole)
                    if is_catching and self.moves_tree[self.cards].opponents_moves[pole] == protection:
                        self.moves_tree[self.cards].catching_the_transmission = pole
                    elif is_catching and self.moves_tree[self.cards].opponents_moves[pole] == pole and \
                            self.moves_tree[self.cards].catching_the_take == -1:
                        self.moves_tree[self.cards].catching_the_take = pole
        elif self.moves_tree[self.cards].who_wins == 2 and p.who_wins == 2:
            self.moves_tree[self.cards].good_moves.append(pole)
            if is_catching and self.moves_tree[self.cards].opponents_moves[pole] == protection:
                self.moves_tree[self.cards].catching_the_transmission = pole
            elif is_catching and self.moves_tree[self.cards].opponents_moves[pole] == pole and \
                    self.moves_tree[self.cards].catching_the_take == -1:
                self.moves_tree[self.cards].catching_the_take = pole

    def build_moves_tree(self):
        if not self.moves_tree.get(self.cards) is None:
            return
        if self.size == 0:
            self.moves_tree[self.cards] = Position(2, -1, 0)
            return
        if self.cards == 2 ** self.size:  # проверить случай ничьи 01
            self.moves_tree[self.cards] = Position(1, 0, self.size)
            return
        if self.cards == (2 ** (self.size + 1) - 1):
            self.moves_tree[self.cards] = Position(0, 0, self.size)
            return
        self.moves_tree[self.cards] = Position()
        for i in range(self.size):
            if self.has_player_position(i, 0):
                self.pole = i
                self.build_moves_tree_opponent()
        self.pole = -1


def main():
    vector = list(map(int, input("Вектор карт: ").split()))
    player = int(input("Первый игрок: "))
    type = int(input("Дурак - 0 или Д-Дурак - 1: "))
    #type2 = int(input("Компъютер/Компъютер - 0 или Игрок/Компъютер - 1: "))
    type2=0
    if type == 1:
        d = OdnomastkaD_Durak(vector, player)
    else:
        d = OdnomastkaDurak(vector, player)
    # d = OdnomastkaDurak([0, 1, 0, 1, 1, 0, 0], 0)
    print('Кто выиграет:', d.who_wins())
    print('Через сколько ходов', d.when_wins())
    print('С счетом', d.winning_score())
    if type2 == 0:
        print("Оптимальные ходы: ", end='')
        for i in d.moves_tree[d.cards].good_moves:
            print(i+1, end=' ')
        print()
        print("Ловля взятие", d.moves_tree[d.cards].catching_the_take+1)
        print("Ловля пропускание", d.moves_tree[d.cards].catching_the_transmission+1)
        pole = d.move_by_computer()
        while pole != -1:
            print("карта:", pole)
            d.print()
            pole = d.move_by_computer()
    else:
        print("-1 значит принять карту, компьютер играет за 0, -2 значит сходить компьютеру")
        d.print()
        while not d.is_end():
            if d.now_player==0:
                pole = d.move_by_computer()
                print("карта:", pole)
                d.print()
            else:
                t = int(input())
                if t == -2:
                    pole = d.move_by_computer()
                    print("карта:", pole)
                else:
                    d.move_by_player(t)
                d.print()



if __name__ == '__main__':
    main()
# 0 1 0 1  0 1 0 1  0 1 0 1  0 1 0 1  0 1
# 0 1 0 1  0 1 0 1  0 1 0 1  0 1 0 1  0 1 0 1

# 0 1 0 1  0 1 0 1  0 1 0 1  0 1 0 1  0 1 0 1  0 1 0 1  0 1

