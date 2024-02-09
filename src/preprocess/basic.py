class Basic:
    def __init__(self):
        pass

    def drop_columns(self, df):
        pass

    def drop_duplicated(self, df):
        df = df.drop_duplicates()
        df.reset_index(drop=True, inplace=True)
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
