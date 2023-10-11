from sqlite3 import Connection
from datetime import datetime, timedelta
from pandas import DataFrame

def append_example_data(conn: Connection):
    """Appends example data to database"""
    today = datetime.now()
    
    activity = [
        ['PROGRAMING', '#6B8F71', '#D9FFF5', 0],
        ['STUDING', '#046E8F', '#38AECC', 0],
        ['LEETCODING', '#E70E02', '#E89005', 0]
    ]
    
    data =[
        [(today - timedelta(days=400)).strftime('%Y-%m-%d'), '10:20:30', '7200', '100', 'Testing StopWatch distant date', '1'],
        [(today - timedelta(days=160)).strftime('%Y-%m-%d'), '10:20:30', '100', '100', 'Testing StopWatch distant date', '1'],
        [(today - timedelta(days=80)).strftime('%Y-%m-%d'), '10:20:30', '1500', '100', 'Testing StopWatch distant date', '1'],
        [(today - timedelta(days=31)).strftime('%Y-%m-%d'), '10:20:30', '1800', '100', 'Testing StopWatch distant date', '1'],
        [(today - timedelta(days=29)).strftime('%Y-%m-%d'), '10:20:30', '1800', '100', 'Testing StopWatch distant date', '2'],
        [(today - timedelta(days=12)).strftime('%Y-%m-%d'), '10:20:30', '1800', '100', 'Testing of actions hovering over each other', '2'],
        [(today - timedelta(days=12)).strftime('%Y-%m-%d'), '10:56:30', '1800', '100', 'Testing of actions hovering over each other', '1'],
        [(today - timedelta(days=10)).strftime('%Y-%m-%d'), '12:20:30', '1800', '100', 'Testing of actions hovering over each other', '2'],
        [(today - timedelta(days=10)).strftime('%Y-%m-%d'), '12:53:00', '8000', '0', 'Testing of actions hovering over each other', '1'],
        [(today - timedelta(days=9)).strftime('%Y-%m-%d'), '12:20:30', '700', '60', 'Testing precision of action positioning', '3'],
        [(today - timedelta(days=6)).strftime('%Y-%m-%d'), '12:12:12', '3600', '180', 'Testing multiple events in one day', '2'],
        [(today - timedelta(days=6)).strftime('%Y-%m-%d'), '14:01:30', '7990', '600', 'Testing multiple events in one day', '3'],
        [(today - timedelta(days=6)).strftime('%Y-%m-%d'), '18:20:30', '700', '60', 'Testing multiple events in one day', '4'],
        [(today - timedelta(days=5)).strftime('%Y-%m-%d'), '18:16:30', '120', '60', 'Testing precision of action positioning', '2'],
        [(today - timedelta(days=5)).strftime('%Y-%m-%d'), '18:45:01', '900', '1', 'Testing precision of action positioning', '2'],
        [(today - timedelta(days=3)).strftime('%Y-%m-%d'), '13:12:12', '3600', '180', 'Testing StopWatch', '4'],
        [(today - timedelta(days=2)).strftime('%Y-%m-%d'), '10:00:01', '18000', '2900', 'Test long action', '2'],
        [(today - timedelta(days=2)).strftime('%Y-%m-%d'), '18:15:01', '4910', '1621', 'Testing StopWatch', '3'],
        [(today - timedelta(days=2)).strftime('%Y-%m-%d'), '23:45:01', '7200', '300', 'Passing through 2 days', '4'],
        [(today - timedelta(days=1)).strftime('%Y-%m-%d'), '3:50:12', '60', '10', 'Long desc: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla imperdiet posuere libero, et dignissim nisl aliquet sit amet. In sit amet elit eget ex sagittis tempor in a erat. Nullam ut libero sit amet mauris molestie molestie vitae aliquam elit. Vivamus libero orci, scelerisque sit amet nisl id, venenatis euismod.', '3'],
        [(today).strftime('%Y-%m-%d'), '4:20:20', '14060', '1800', 'Test movescroll on first iteration', 3]
    ]
    
    df_activities = DataFrame({
        'name': [a[0] for a in activity],
        'bg': [a[1] for a in activity],
        'fg': [a[2] for a in activity],
        'auto': [a[3] for a in activity]
    })
    df_activities.to_sql('activities', conn, if_exists='append', index=False)
    
    df_data = DataFrame({
                    'date': [d[0] for d in data],
                    'start_time': [d[1] for d in data],
                    'main_time': [d[2] for d in data],
                    'break_time': [d[3] for d in data],
                    'desc': [d[4] for d in data],
                    'activity': [d[5] for d in data]
                })
    df_data.to_sql('data', conn, if_exists='append', index=False)