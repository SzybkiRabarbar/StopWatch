from datetime import datetime, timedelta

def last_week_dates() -> str:
    today = datetime.now()
    week = [today - timedelta(days=x) for x in range(7)]
    week = [f"{d.year}-{d.month}-{d.day}" for d in week]
    return week

if __name__=="__main__":
    
    print(last_week_dates())