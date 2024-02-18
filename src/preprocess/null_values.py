def fillna(df):
    """
    결측치 채우기
    """
    for col in df.columns:
        if df[col].isna().sum():
            if df[col].dtypes == 'O':
                df[col].fillna('Space', inplace=True)
            else:
                df[col].fillna(0, inplace=True)
    return df
