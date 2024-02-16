import pandas as pd
from collections import Counter


class Basic:
    def __init__(self):
        pass

    def drop_columns(self, df):
        pass

    def drop_duplicated(self, df):
        df = df.drop_duplicates()
        df.reset_index(drop=True, inplace=True)
        return df

    def customer_idx_merge_enterprise(self, df):
        def most_common(x):
            return Counter(x).most_common(1)[0][0]

        mode_df = df.groupby('customer_idx')['enterprise'].agg(most_common).reset_index()
        df = df.drop('enterprise', axis=1).merge(mode_df, on='customer_idx')
        return df

    def cusotmer_idx_categorization(self,df, bins=[0, 2, 10, 100, 1000, 10000]):
        """customer_idx 범주화"""
        customer_idx_counts = df['customer_idx'].value_counts()
        df_counts = pd.cut(customer_idx_counts, bins=bins, labels=False, right=False)
        df['customer_idx_group'] = df['customer_idx'].map(df_counts)
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
