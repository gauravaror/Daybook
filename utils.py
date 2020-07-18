import pandas as pd
def get_timezone(df_file, chat_id):
    df = pd.read_pickle(df_file)
    output = df[df.chat_id == chat_id]
    if len(output) > 0:
        output.iloc[0].timezone
    else:
        return None

def save_timezone(df_file, chat_id, timezone):
    df = pd.read_pickle(df_file)
    df[df.chat_id == chat_id].iloc[0]

