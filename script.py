def main():
    import argparse
    import sys
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    import pytz

    parser = argparse.ArgumentParser(description='Matching timestamps of a periodic task.')
    parser.add_argument('--period', dest='period', action='store', help='specify the period', required=True, choices=['1h', '1d', '1mo', '1y'])
    parser.add_argument('--t1', dest='startpoint', action='store', help='startpoint in UTC', required=True)
    parser.add_argument('--t2', dest='endpoint', action='store', help='endpoint in UTC', required=True)
    parser.add_argument('--tz', dest='timezone', metavar='timezone', action='store', help='specify the timezone', required=True, choices=pytz.all_timezones)
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(10)
    try:
        t1 = datetime.strptime(args.startpoint, "%Y%m%dT%H%M%SZ")
        t2 = datetime.strptime(args.endpoint, "%Y%m%dT%H%M%SZ")
    except ValueError:
        print("ERROR. Wrong Date Format", file=sys.stderr)
        sys.exit(10)
        
    #choices like '1w':'weeks', '1m': minutes, '1s': seconds can be added in the dictionary in order to achieve extensibility.
    choices = {'1h':'hours', '1d':'days', '1mo':'months', '1y':'years'} #'1w':'weeks', '1m': 'minutes', '1s': 'seconds'} 
    date = t1
    lod = [] #initialize a list of dates between t1 and t2
    dct = {choices[args.period]:+1} #pack arguments to achieve extensibility.
    #print(date + relativedelta(**dct))
    while date < t2:
        date = date + relativedelta(**dct)
        lod.append(date)
    #print(t1, t2)
    print(date)
    for obj in lod:
        print(obj)
    #print(lod) #Do not print last element

if __name__ == "__main__":
    main()