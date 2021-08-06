import argparse
import sys
import pytz

def parse_args(args):
    parser = argparse.ArgumentParser(description='Matching timestamps of a periodic task.')
    parser.add_argument('--period', dest='period', action='store', help='specify the period', required=True, choices=['1h', '1d', '1mo', '1y']) #'1w', '1m', '1s'
    parser.add_argument('--t1', dest='startpoint', action='store', help='startpoint in UTC', required=True)
    parser.add_argument('--t2', dest='endpoint', action='store', help='endpoint in UTC', required=True)
    parser.add_argument('--tz', dest='timezone', metavar='timezone', action='store', help='specify the timezone', required=True, choices=pytz.all_timezones)
    try:
        return parser.parse_args(args)
    except SystemExit:
        sys.exit(10)

def main(mode='normal', test_param = None):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    from dateutil import tz
    
    if mode == 'unittest': # Unittest
        args = parse_args(test_param)
    else:
        args = parse_args(sys.argv[1:])

    try:
        timezone = args.timezone
        t1_utc = datetime.strptime(args.startpoint, "%Y%m%dT%H%M%SZ").astimezone(pytz.utc) # t1 in UTC
        t2_utc = datetime.strptime(args.endpoint, "%Y%m%dT%H%M%SZ").astimezone(pytz.utc) #t2 in UTC
    except ValueError:
        print("ERROR. Wrong Date Format provided", file=sys.stderr)
        sys.exit(10)

    t1 = t1_utc.replace(tzinfo=pytz.utc).astimezone(tz.gettz(timezone)) # store t1 in provided TIMEZONE
    t2 = t2_utc.replace(tzinfo=pytz.utc).astimezone(tz.gettz(timezone)) # store t2 in provided TIMEZONE

    # Truncate t1 datetime based on period provided.
    if args.period == '1h':
        t1 = t1 + relativedelta(hours=+1)
        t1 = t1.replace(minute=0, second=0)
    elif args.period == '1d':
        t1 = t1 + relativedelta(days=+1)
        t1 = t1.replace(hour=0, minute=0, second=0)
    elif args.period == '1mo':
        t1 = t1 + relativedelta(months=+1)
        t1 = t1.replace(day=1, hour=0, minute=0, second=0)
    elif args.period == '1y':
        t1 = t1 + relativedelta(years=+1)
        t1 = t1.replace(month=1, day=1, hour=0, minute=0, second=0)
    else:
        # In order to achieve further extensibility code must be inserted here with the same logic as above.
        pass

    #choices like '1w':'weeks', '1m': minutes, '1s': seconds can be added in the dictionary in order to achieve extensibility.
    choices = {'1h':'hours', '1d':'days', '1mo':'months', '1y':'years'} #'1w':'weeks', '1m': 'minutes', '1s': 'seconds'} 
    date = t1 # will be used in the following loop so that ptlist will be filled.
    ptlist = [] # initialize a list of dates between t1 and t2.
    dct = {choices[args.period]:+1} # pack arguments for relative delta to achieve extensibility.
    while date < t2:
        date_utc = date.replace(tzinfo=tz.gettz(timezone)).astimezone(pytz.utc).strftime("\"%Y%m%dT%H%M%SZ\"")  #Revert to UTC and print in the appropriate layout.)
        print(date_utc)
        ptlist.append(date_utc) #append to list for unit-testing.
        date = date + relativedelta(**dct)
    return ptlist

if __name__ == "__main__":
    main()