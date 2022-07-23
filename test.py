from datetime import datetime
today = (2022, 7, 23)
# today = tuple(datetime(*today[0:3]).timetuple())[0:3]
# today = tuple(datetime(*today[:]))[:6]]
# today_str = str(today)
# today_str = ','.join(str(today[:]))
num = -5000
s, num = 'X', int(abs(num))
# s = f'{"X" * 10}'
s = 'X' * (int(abs(num)) //1000)
print(s)
