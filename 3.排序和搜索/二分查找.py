# bisect 用于确定在顺序列表中确定插入的元素的位置
from bisect import bisect, bisect_left


def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
	i = bisect(breakpoints, score)
	return grades[i]


grades = [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
print(grades)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

data = [('red', 5), ('blue', 1), ('yellow', 8), ('black', 0)]
data.sort(key=lambda r: r[1])
keys = [r[1] for r in data]
print(data[bisect_left(keys, 5)])
