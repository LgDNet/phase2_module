class Categorization():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def cat_customer_idx(self, df):
        df['new_customer_idx'] = df['customer_idx'].astype(str).str[-1:]
        return df
    
    def apply(self, df, module_list=None):
        df = self.cat_customer_idx(df)
        return df