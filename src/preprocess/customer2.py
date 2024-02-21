import numpy as np
import pandas as pd


class Customer2:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def get_type_dict(self, dictionary):
        cate1_dict, cate2_dict = {},{}
        # mapping
        for key, value in dictionary.items():
            cate1_dict[key] = value[0]
            cate2_dict[key] = value[1]
        return(cate1_dict, cate2_dict)
    
    def seniority_level(self, df):
        data =df[['customer_job','customer_type','customer_position','customer_type2','seniority_level','job_function']].copy()
        def map_seniority(row):
            columns = ['customer_position', 'customer_type', 'customer_job', 'job_function']
            for col in columns:
                if isinstance(row[col], str):
                    for key in self.seniority:
                        if key in row[col]:
                            return self.seniority[key]
                        elif row[col] =='Space':
                            return 'Space'
            return 'others'
        data['seniority_level'] = data.apply(map_seniority, axis =1)
        data["seniority_level"] = data["seniority_level"].map(self.seniority_map)
        df['seniority_level'] = data['seniority_level']
        return df
    
    
    def job_function(self, df):
        data =df[['customer_job','customer_type','customer_position','customer_type2','seniority_level','job_function']].copy()
        data['customer_job'] =data['customer_job'].fillna('Space')
        data['customer_job'] = data['customer_job'].str.replace('_', '')
        
        def map_job(row):
            columns = ['customer_job', 'customer_type','customer_position', 'job_function']
            for col in columns:
                if isinstance(row[col], str):
                    for key in self.job_dict:
                        if key in row[col]:
                            return self.job_dict[key]
            for col in columns:
                if isinstance(row[col], str) and 'Space' in row[col]:
                    return 'Space'
            return 'others'
        
        data['job_function'] = data.apply(map_job, axis =1)
        df[['job_function', 'customer_job']] = data[['job_function', 'customer_job']]
        return df
        
    def customer_type(self, df):
        data =df[['customer_job','customer_type','customer_position','customer_type2','seniority_level','job_function']].copy()
        data['customer_type'] =data['customer_type'].fillna('Space')
        def map_type(row):
            columns = ['customer_type', 'customer_type2','customer_position', 'customer_job', 'job_function']
            for col in columns:
                if isinstance(row[col], str):
                    for key in self.customer_type_filter:
                        if key in row[col]:
                            return self.customer_type_filter[key]
            for col in columns:
                if isinstance(row[col], str) and 'other' in row[col]:
                    return 'others'
            return row['customer_type']
        
        data['customer_type'] = data.apply(map_type, axis =1)
        customer_type1, customer_type2 = self.get_type_dict(self.customer_type_dict)
        data["new_customer_type1"] = data["customer_type"].apply(
                lambda x: next((v for k, v in customer_type1.items() if k in x), 'others')
            )
        data["new_customer_type2"] = data["customer_type"].apply(
                lambda x: next((v for k, v in customer_type2.items() if k in x), 'others')
         )
        df[['new_customer_type1','new_customer_type2']] = data[['new_customer_type1','new_customer_type2']]
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