import numpy as np
class Convert_ratio:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def make_ratio_to_dict(self,df,col_name):
        """비율 딕셔너리 저장"""
        # from phase2_module.src.utils.manage_pkl_files import PickleManager as pkl_manager
        dict_ ={}
        flag = df.groupby(col_name)['is_converted'].agg(['sum','count'])
        for idx, plus, counts in zip(flag.index,flag['sum'],flag['count']):
            cond =  df[col_name] == idx
            ratio = (plus / counts) * 100
            df.loc[cond,f'{col_name}_converted_ratio'] = round(ratio,2)
            dict_[idx] = ratio
        # save
        # pkl_manager.save(f"{col_name}",f"{col_name}_converted_ratio",dict_)
        return dict_

    def ratio_preprocessing(self,df, col_name, ratio_dict):
        # 검증
        for i in np.sort(df[col_name].unique()):
            if i not in ratio_dict.keys(): # 없으면 추가
                self.lead_owner_converted_ratio[i] = 0.0
        df[f'{col_name}_converted_ratio'] = df[col_name].map(ratio_dict)
        return df
        
    def lead_owner(self,df):
        return self.ratio_preprocessing(df, 'lead_owner', self.lead_owner_converted_ratio)
    
    def apply(self, df, module_list):
        if not module_list:
            raise ValueError("Not used modules")

        if not isinstance(module_list, list):
            module_list = [module_list]

        for module in module_list:
            method = getattr(self, module)

            df = method(df)
        return df