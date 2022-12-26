import datetime
def parser(time):
    date = time.split('-')

    year = int(date[0])
    month = int(date[1])
    day = int(date[2].split('T')[0])

    
    time = date[2].split('T')[1][1:-1].split(':')

    hour = int(time[0])
    minute = int(time[1])
    second = int(time[2].split('.')[0])
    subsecond = min(int(time[2].split('.')[1]), 999999)
    
    return datetime.datetime(year, month, day, hour, minute, second, subsecond)

