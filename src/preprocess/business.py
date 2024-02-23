import numpy as np

class Business:
    def __init__(self, **kwargs):
        # Load pickle file
        for key, value in kwargs.items():
            setattr(self, key, value)

    def business_double(self, df):
        """ business """
        
        filter1 = self.filter1
        filter2 = self.filter2
        
        df['business_area_tmp']=np.NaN
        df['business_area_tmp2']=np.NaN
        
        for key, value in filter1.items():
            for v in value:
                df.loc[
                (df['business_area'].isnull())
                &(df['business_unit']==key),
                'business_area_tmp'
                ] = v
        
        for key, value in filter2.items():
            for v in value:
                df.loc[
                (df['category_3']==key)
                &(df['business_area_tmp'].str.contains(v)),
                'business_area_tmp2'
                ] = v
    
        df.loc[
        df['business_area'].isnull(), 
        'business_area'
        ] = df['business_area_tmp2']
    
        df.drop(['business_area_tmp', 'business_area_tmp2'], axis=1, inplace=True)
        
        return df


    def business_only(self, df):
        """ business_only """
        
        filter2 = self.filter2
        df['business_area_tmp']=np.NaN
        
        for key, value in filter2.items():
            for v in value:
                df.loc[
                (df['business_area'].isnull())
                &(df['category_3']==key),
                'business_area_tmp'
                ] = v
        
        df.loc[
        df['business_area'].isnull(), 
        'business_area'
        ] = df['business_area_tmp']
        
        df.drop(['business_area_tmp'], axis=1, inplace=True)
        df['business_area'].fillna('Space', inplace=True)
        
        return df
    
    def apply(self, df, module_list=None):
    
        df = self.business_only(df)
        return df
