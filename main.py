from finance_calendars import finance_calendars as fc
from datetime import datetime, timedelta
from ics import Calendar, Event
import ics
from datetime import datetime, date
import pandas as pd
import traceback

"""
pip install finance_calendars ics
"""

def gen_calendar_event(row):
    alarm1 = ics.alarm.AudioAlarm(trigger= timedelta(days=-4, hours=10)) #4天前的10点
    alarm2 = ics.alarm.AudioAlarm(trigger= timedelta(days=-1, hours=10)) #1天前的10点
    alarms = [alarm1, alarm2]


    event_name = '%s %s财报' % (row['symbol'], row['time_cn'])
    e = Event(alarms=alarms, name=event_name)
    e.begin = row['publish_date'] + ' 00:00:00'
    e.make_all_day()
    return e


def get_time_chn(raw_text):
    time2chn = {
        'time-pre-market': '盘前',
        'time-after-hours': '盘后',
        'time-not-supplied': '',
    }
    return time2chn.get(raw_text, '')

g_symbols_needed = [
    "AMD",
    "SE",
    "BILI",
    "GOOGL",
    "GOOG",
    "AMZN",
    "AAPL",
    'TSLA',
    'JMIA',
    'PDD',
    'COIN',
    'SHOP',
    'ARM',
    'BABA',
    'SMCI',
    'TSM',
    'JD',
    'NIO',
    'LI',
    'LKNCY',
    'BIDU',
    'XPEV',
]

def main():
    date_list = []
    for i in range(-7, 30):
        today = datetime.today().date()
        date_list.append(today + timedelta(days=i))
        
    df_list = []
    for fetch_date in date_list:
        try:
            print(fetch_date)
            df = fc.get_earnings_by_date(fetch_date)
            if len(df) == 0:
                continue
                
            df=df.reset_index()
            df['publish_date'] = fetch_date.strftime('%Y-%m-%d') # date2str
            df['time_cn']      = df['time'].apply(lambda x: get_time_chn(x))
            df['is_valid']     = df['symbol'].apply(lambda x: x in g_symbols_needed)
            df = df[df['is_valid']]
            df_list.append(df)
        except Exception as e:
            # 获取并输出详细的异常信息
            print("An exception occurred:", fetch_date)
            traceback.print_exc()
            continue
        

    df_final = pd.concat(df_list)


    calendar = Calendar()
    for index, row in df_final.iterrows():
        e = gen_calendar_event(row)
        calendar.events.add(e)


    with open('./data/my_calendar.ics', 'w') as f:
        f.writelines(calendar.serialize_iter())
        
    print('Done')


if __name__ == "__main__":
    main()