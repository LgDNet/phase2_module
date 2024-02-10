import re


class Customer:
    def __init__(self, **kwargs):
        # Load pickle file
        for key, value in kwargs.items():
            setattr(self, key, value)

    def complementary(
        self, customer_df, target_col, dictionary, comple_list, default_value="etc"
    ):
        """customer_column의 결측값을 채워주는 함수"""
        customer_df.loc[:,["customer_type", "customer_job", "customer_position"]] = customer_df[["customer_type", "customer_job", "customer_position"]].applymap(
            lambda x: re.sub("(&|-|/|:)", "", x.lower().replace(" ", ""))
            if isinstance(x, str)
            else x
        )
        customer_df[target_col] = None

        for col in comple_list:
            for key, value in dictionary.items():
                for val in value:
                    true_list = []
                    val = re.sub("(&|-|/|:)", "", val).replace(" ", "").lower()

                    true_list = list(
                        customer_df.loc[
                            customer_df[col].str.contains(val, na=False)
                        ].index
                    )
                    customer_df.loc[
                        (customer_df[target_col].isnull())
                        & (customer_df.index.isin(true_list)),
                        target_col,
                    ] = key

        comple_col = comple_list[0]
        customer_df.loc[
            (customer_df[comple_col].notnull()) & (customer_df[target_col].isnull()),
            target_col,
        ] = "etc"

        customer_df[target_col].fillna("Unknown", inplace=True)

        return customer_df

    def apply(self, customer_df, pkl):
        """실행 함수"""
        customer_type2 = self.customer_type2
        job_function = self.job_function
        seniority_level = self.seniority_level

        customer_df = self.complementary(
            customer_df,
            "customer_type2",
            customer_type2,
            ["customer_type", "customer_job", "customer_position"],
        )
        customer_df = self.complementary(
            customer_df,
            "job_function",
            job_function,
            ["customer_job", "customer_type", "customer_position"],
        )
        customer_df = self.complementary(
            customer_df,
            "seniority_level",
            seniority_level,
            ["customer_position", "customer_type", "customer_job"],
        )
        return customer_df
