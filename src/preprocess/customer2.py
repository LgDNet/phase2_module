import numpy as np
import pandas as pd


class Customer2:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def seniority_level(self, df):
        data =df[['customer_job','customer_type','customer_position','customer_type2','seniority_level','job_function']].copy()
        def map_seniority(row):
            columns = ['customer_position', 'customer_type', 'customer_job', 'job_function']
            for col in columns:
                if isinstance(row[col], str):
                    for key in self.seniority:
                        if key in row[col]:
                            return self.seniority[key]
            return 'others'
        data['seniority_level'] = data.apply(map_seniority, axis =1)
        data["seniority_level"] = data["seniority_level"].map(self.seniority_map)
        df['seniority_level'] = data['seniority_level']
        return df
    
    def apply(self, df, module_list: list):
        if not module_list:
            raise ValueError("Not used modules")

        if not isinstance(module_list, list):
            module_list = [module_list]

        for module in module_list:
            method = getattr(self, module)
            df = method(df)

        return df