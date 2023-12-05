from unittest import TestCase

from my_range import MyRange, MyRangeUnion


class TestMyRange(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #    pass

    # def setUp(self):
    #    pass

    def test_contains(self):
        assert range(11, 12) in MyRange(10, 15)
        assert range(9, 12) not in MyRange(10, 15)

    def test_comparaison(self):
        assert MyRange(10, 15) < MyRange(8, 16)
        assert MyRange(8, 16) > MyRange(10, 15)
        assert MyRange(10, 15) < MyRange(8, 15)
        assert MyRange(8, 15) > MyRange(10, 15)


class TestMyRangeUnion(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #    pass

    def setUp(self):
        self.test = MyRangeUnion(MyRange(9, 15), MyRange(14, 25))

    def test_contains(self):
        assert MyRange(12, 17) in self.test
        assert MyRangeUnion(MyRange(12, 17), MyRange(18, 19)) in self.test
        assert MyRangeUnion(MyRange(12, 17), MyRange(18, 29)) not in self.test

    def test_add(self):
        test = MyRangeUnion(MyRange(9, 15), MyRange(14, 25))
        assert test + MyRangeUnion(MyRange(5, 15), MyRange(28, 35)) == MyRangeUnion(
            MyRange(5, 25), MyRange(28, 35)
        )
