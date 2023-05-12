import time

def focus_timer(focus_minutes, break_minutes):
    print(f"开始工作，专注 {focus_minutes} 分钟.")
    time.sleep(focus_minutes * 60)
    print(f"休息时间！休息 {break_minutes} 分钟.")
    time.sleep(break_minutes * 60)

focus_minutes = 25
break_minutes = 5
focus_timer(focus_minutes, break_minutes)
