from datetime import datetime, timedelta
import pytz


now = datetime.now(tz=pytz.timezone('US/Eastern'))
time_30_days_ago = now - timedelta(days=30)

print(time_30_days_ago)
print(now)
        