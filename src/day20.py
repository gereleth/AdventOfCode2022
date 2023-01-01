# Day 20: Grove Positioning System
# Problem statement: https://adventofcode.com/2022/day/20

day_title = "Grove Positioning System"


class Node:
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.right = None
        self.left = None
        self.original_right = None


class MixingList:
    def __init__(self, ls):
        nodes = [Node(value, index) for index, value in enumerate(ls)]
        self.length = len(ls)
        for i, node in enumerate(nodes):
            node.right = nodes[(i + 1) % self.length]
            node.left = nodes[(i - 1) % self.length]
            node.original_right = node.right
            if node.value == 0:
                self.zero = node
        self.head = nodes[0]

    def mix(self):
        node = self.head
        while True:
            move = node.value % (self.length - 1)
            if move >= self.length // 2:
                move -= self.length - 1
            # remove node and connect its neighbours
            node.left.right = node.right
            node.right.left = node.left
            # insert node at new place
            insert_left_of = node.left
            if move > 0:
                for _ in range(move):
                    insert_left_of = insert_left_of.right
            elif move < 0:
                for _ in range(-move):
                    insert_left_of = insert_left_of.left
            insert_right_of = insert_left_of.right
            insert_left_of.right = node
            insert_right_of.left = node
            node.left = insert_left_of
            node.right = insert_right_of
            # go on with the original right neighbour
            node = node.original_right
            if node == self.head:
                break

    def answer(self):
        total = 0
        node = self.zero
        for i in range(3):
            for _ in range(1000 % self.length):
                node = node.right
            total += node.value
        return total


def part1(text_input):
    ls = [int(i) for i in text_input.split()]
    mixer = MixingList(ls)
    mixer.mix()
    return mixer.answer()


def part2(text_input):
    key = 811589153
    ls = [int(i) * key for i in text_input.split()]
    mixer = MixingList(ls)
    for _ in range(10):
        mixer.mix()
    return mixer.answer()
