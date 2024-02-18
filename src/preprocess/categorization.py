import pandas as pd
from collections import Counter

class Categorization:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def cat_customer_idx(self, df):
        """ Categorize for Customer_idx """
        df['new_customer_idx'] = df['customer_idx'].astype(str).str[:2]
        return df

    def customer_idx_merge_enterprise(self, df):
        """Classify Enterprise"""
        def most_common(x):
            return Counter(x).most_common(1)[0][0]

        mode_df = df.groupby('new_customer_idx')['enterprise'].agg(most_common).reset_index()
        df = df.drop('enterprise', axis=1).merge(mode_df, on='new_customer_idx')
        return df
    
    def historical_cnt_mean(self, df):
        historical_dict = df.groupby('new_customer_idx')['historical_existing_cnt'].mean().sort_values(ascending=False).to_dict()
        df['historial_existing_mean'] = df['new_customer_idx'].map(historical_dict)
        return df
    
    def apply(self, df, module_list):
        if not module_list:
            raise ValueError("Not used modules")

        if not isinstance(module_list, list):
            module_list = [module_list]

        for module in module_list:
            method = getattr(self, module)

            df = method(df)

        return df