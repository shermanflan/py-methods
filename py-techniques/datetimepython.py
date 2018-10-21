from datetime import timedelta, datetime, tzinfo, timezone

# Complete the time_delta function below.
def time_delta(t1, t2):

    try:
        # "Sun 10 May 2015 13:54:36 -0700"
        dt = datetime.strptime(t1, "%a %d %b %Y %H:%M:%S %z")
        dt2 = datetime.strptime(t2, "%a %d %b %Y %H:%M:%S %z")
        td1 = dt - dt2
        return '{0:.0f}'.format(abs(td1.total_seconds()))
    except Exception as e:
        print(e)
        
    return '0'
