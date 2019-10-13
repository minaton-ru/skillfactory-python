import time

# Декоратор, который принимает на вход количество прогонов
def time_this(NUM_RUNS):
# Внутри декоратора функция, которая принимает в качестве параметра оборачиваемую функцию
    def decorator(func):
        avg_time = 0
        for _ in range(NUM_RUNS):
            t0 = time.time()
            func()
            t1 = time.time()
            avg_time += (t1 - t0)
        avg_time /= NUM_RUNS
        return "Среднее время выполнения " + str(avg_time)
    return decorator

@time_this(100)
def fibonachisum():
    fibonachilist=[1, 2]
# Определяем до какого числа будем строить последовательность Фибоначчи
    while fibonachilist[-1]<1000000000000000000:
        fibonachilist.append(fibonachilist[-2]+fibonachilist[-1])
    i = 0
    sum_ = 0
# Сумма четных элементов последовательности Фибоначчи
    while i != len(fibonachilist):
      if fibonachilist[i] % 2 == 0:
          sum_ = sum_ + fibonachilist[i]
      i = i + 1
    #return "Сумма: " + str(sum_)

print(fibonachisum)
