from datetime import datetime, timedelta
import pandas as pd

def get_time_df():
    time = datetime.utcnow() + timedelta(hours=2)
    df_row = [{ 'time': time }]
    df = pd.DataFrame(df_row)
    return df

def log_this_run():
    log_file = 'run_log.csv'
    try:
        log = pd.read_csv(log_file, index_col=0)
    except:
        log = pd.DataFrame()
    log = log.append(get_time_df())
    log.to_csv(log_file)
    return