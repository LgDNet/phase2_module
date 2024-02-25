import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class Budget:
    def __init__(self, **kwargs):
        # Load pickle file
        for key, value in kwargs.items():
            setattr(self, key, value)


    def budget_ratio(self, df):
    
        df['title'] = df['seniority_level']
        df['timeline'] = df['new_expected_timeline'].map(self.timeline_order_dict)
        df['needs'] = df['new_inquiry_type'].map(self.needs_order_dict)
        df['budget']=np.NaN
        
        mMscaler = MinMaxScaler()
        
        bant_df = df[['title', 'timeline', 'needs']]
        scaled_df = mMscaler.fit_transform(bant_df[['title', 'timeline', 'needs']])
        df.drop(['title', 'timeline', 'needs'], axis=1, inplace=True)
        scaled_df = pd.DataFrame(scaled_df, columns=bant_df.columns)
        df = pd.concat([df, scaled_df], axis=1)
        df['budget'] = df['bant_submit'] - (df['title']*0.25+ df['timeline']*0.25+df['needs']*0.25)
        
        df.drop(['title', 'timeline', 'needs'], axis=1, inplace=True)
        
        return df
    
    def apply(self, df, module_list=None):
    
        df = self.budget_ratio(df)
        return df
