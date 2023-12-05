class MyRange:
    def __init__(self, start: int, stop: int = None) -> None:
        if start is not None and stop is None:
            self._range = range(start, start)
        else:
            if start > stop:
                self._range = None
            self._range = range(start, stop)

    @property
    def start(self):
        return self._range.start

    @property
    def stop(self):
        return self._range.stop

    def offset(self, offset: int):
        return MyRange(self.start + offset, self.stop + offset)

    def __bool__(self):
        return self._range is not None

    def __str__(self) -> str:
        return range.__str__(self._range)

    def __repr__(self) -> str:
        return self.__str__()

    def __contains__(self, value: int):
        if value == self.start or value == self.stop:
            return True
        return value in self._range

    def __eq__(self, other: object) -> bool:
        return other.start == self.start and other.stop == self.stop

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object):
        self._assert_other_type(other)
        if self.stop == other.stop:
            return self.start > other.start
        return self.stop < other.stop

    def __gt__(self, other: object):
        self._assert_other_type(other)
        if other.stop == self.stop:
            return other.start > self.start
        return other.stop < self.stop

    def _assert_other_type(self, other: object):
        if isinstance(other, (range, MyRange)):
            pass
        else:
            raise ValueError(f"Unknown type '{other.__class__.__name__}'")

    def mask(self, other: object) -> (list, list):
        if other.start >= self.start and other.stop <= self.stop:
            return (self, None)
        elif self.start <= other.start and self.stop >= other.start:
            return (
                MyRange(other.start, self.stop),
                MyRange(self.start, other.start - 1),
            )
        elif self.start <= other.stop and self.stop >= other.stop:
            return (MyRange(self.start, other.stop), MyRange(other.stop + 1, self.stop))
        else:
            return (None, self)

    def strict_left(self, value: int):
        if value in self:
            if value == self.start:
                return []
            else:
                return [MyRange(self.start, value - 1)]
        else:
            raise ValueError("test")

    def strict_right(self, value: int):
        if value in self:
            if value == self.stop:
                return []
            else:
                return [MyRange(value + 1, self.stop)]
        else:
            raise ValueError("test")

    def mask(self, other: object) -> (list, list):
        if other.start in self and other.stop in self:
            return (
                [other],
                self.strict_left(other.start) + self.strict_right(other.stop),
            )
        elif self.start in other and self.stop in other:
            return ([self], [])
        elif other.start not in self and other.stop in self:
            return (self.strict_left(other.stop), self.strict_right(other.stop))
        elif other.start in self and other.stop not in self:
            return (self.strict_right(other.start), self.strict_left(other.start))
        else:
            return ([], [self])


class MyRangeUnion:
    def __init__(self, *items) -> None:
        self._ranges = []
        for item in items:
            if not isinstance(item, MyRange):
                raise ValueError("item type must be MyRange")
            self._ranges += [item]
        self._factorize()

    def _factorize(self):
        self._ranges.sort()
        done = False
        while not done:
            new, done = self._factorization_step()
            self._ranges = new

    def _factorization_step(self) -> (list[MyRange], bool):
        done = True
        if len(self._ranges) <= 1:
            return (self._ranges, done)
        new = []
        for index, _range in enumerate(self._ranges):
            if index > 0:
                if self._ranges[index - 1] in _range:
                    new.pop()
                    new += [_range]  # Only the containing
                    done = False
                elif self._ranges[index - 1].stop >= _range.start:
                    new += [
                        MyRange(self._ranges[index - 1].start, _range.stop)
                    ]  # Union
                    done = False
                else:
                    new += [_range]
            else:
                new += [_range]
        return (new, done)

    def __add__(self, other: object):
        if isinstance(other, MyRangeUnion):
            new = MyRangeUnion(*(self._ranges + other._ranges))
            new._factorize()
            return new
        else:
            raise ValueError(f"Unknown type '{other.__class__.__name__}'")

    def __str__(self) -> str:
        return list.__str__(self._ranges)

    def __contains__(self, other: object):
        if isinstance(other, (range, MyRange)):
            for _r2 in self._ranges:
                if other in _r2:
                    return True
            return False

        elif isinstance(other, MyRangeUnion):
            for _r1 in other._ranges:
                for _r2 in self._ranges:
                    if _r1 not in _r2:
                        return False
            return True
        else:
            raise ValueError(f"Unknown type '{other.__class__.__name__}'")

    def __eq__(self, other: object) -> bool:
        for r1, r2 in zip(self._ranges, other._ranges):
            if r1.start != r2.start or r1.stop != r2.stop:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
