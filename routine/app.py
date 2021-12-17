import math
from datetime import date, datetime, timedelta

opening_date = datetime(2021, 8, 16, 0, 0)
today = datetime.today()
week = timedelta(days=7)


days_passed = today - opening_date
result = days_passed / timedelta(days=7)
if type(result == float):
    print(math.ceil(result))
else:
    print(result)
