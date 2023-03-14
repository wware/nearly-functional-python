from dataclasses import dataclass
from typing import List, Union

@dataclass
class Student:
    first_name: str
    last_name: str


@dataclass
class Lecturer:
    first_name: str
    last_name: str
    subject: str


class IterHelper(object):
    def __iter__(self):
        return self

    def filter(self, f):
        for i in self:
            if f(i):
                yield i

    def map(self, f):
        for i in self:
            yield f(i)

    def reset(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


@dataclass
class UniversityClass(IterHelper):
    lecturers: List[Lecturer]
    students: List[Student]
    _current_index: int = 0

    def reset(self):
        self._current_index=0

    def __next__(self):
        try:
            this = (self.lecturers + self.students)[self._current_index]
            self._current_index += 1
            return this
        except IndexError:
            raise StopIteration


if __name__ == '__main__':
    s1 = Student('Andrew', 'Brown')
    s2 = Student('Helen', 'White')
    s3 = Student('George', 'Johnson')

    l1 = Lecturer('Maria', 'Richardson', 'Algorithms')
    l2 = Lecturer('Bob', 'Johanson', 'Programming')

    uni_cl = UniversityClass(
        lecturers=[l1 ,l2],
        students=[s1, s2, s3]
    )

    for member in uni_cl:
        print(member)

    print("")
    uni_cl.reset()
    for member in uni_cl.filter(lambda x: 'n' in x.last_name):
        print(member)
