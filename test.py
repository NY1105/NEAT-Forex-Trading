from datetime import datetime
today = (2022, 7, 23)
# today = tuple(datetime(*today[0:3]).timetuple())[0:3]
# today = tuple(datetime(*today[:]))[:6]]
# today_str = str(today)
today_str = ','.join(str(today[:]))

print(today_str)
