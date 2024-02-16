import re


class Inquiry:
    def __init__(self):
        self.inquiry_type = {}

        consulation = {
            "Quotation": "Quotation or Purchase Consultation",  # 견적 또는 구매 상담
            "Sales": "Quotation or Purchase Consultation",
            "Product": "Quotation or Purchase Consultation",
            "Purchase": "Quotation or Purchase Consultation",
            "Event": "Quotation or Purchase Consultation",
            "Partner": "Quotation or Purchase Consultation",
        }

        demo = {
            "Demo": "Request a Demo",  # 데모 요청하기
        }

        oem_odm = {
            "Oem": "OEM/ODM Request",
            "Odm": "OEM/ODM Request",
        }

        technic = {
            "Usage": "Usage or Technical Consultation",  # 사용 또는 기술 상담
            "Technical": "Usage or Technical Consultation",
            "Trainings": "Usage or Technical Consultation",
            "Services": "Usage or Technical Consultation",
            "Suggestions": "Usage or Technical Consultation",
        }

        distributorship = {
            "Distributorship": "Request for Distributorship",  # 대리점에 요청
        }

        others = {
            "Other": "Other",
            "Etc": "Other",
        }

        self.inquiry_category = [
            consulation,
            demo,
            oem_odm,
            technic,
            distributorship,
            others,
        ]

        for category in self.inquiry_category:
            self.inquiry_type.update(category)

        self.start_patterns = [
            re.compile(f"(?i)^{i}") for i in self.inquiry_type.keys()
        ]
        self.exists_patterns = [
            re.compile(f"(?i){i}") for i in self.inquiry_type.keys()
        ]

        self.expected_timeline_dict = {
            "Follow": "Follow up",
            "Already": "Follow up",
            "Respond": "No Response",
            "Response": "No Response",
            "Required": "No Response",
            "Requirement": "No Response",
            "Budget": "Budget Issue",
            "Interest": "Not Interest",
        }
        self.expected_timeline_exists_patterns = [
            re.compile(f"(?i){i}") for i in self.expected_timeline_dict.keys()
        ]

        self.categories = [
            "Less than 3 Months",
            "3 months ~ 6 months",
            "more than a year",
            "9 months ~ 1 year",
            "6 months ~ 9 months",
            "Follow up",
            "No Response",
            "Budget Issue",
            "Not Interest",
            "Space",
        ]

    def fill(self, df):
        df["inquiry_type"].fillna("-", inplace=True)
        df['expected_timeline'] = df['expected_timeline'].replace("Months", 'months')
        return df

    def new_inquiry_type(self, old_inquiry_type):
        for pattern in self.start_patterns:
            find = pattern.search(old_inquiry_type.strip())
            if find:
                return self.inquiry_type.get(find.group().capitalize())
        return "Other"

    def retry_unknown_value_mapping(self, new_inquiry_type, old_inquiry_type):
        if new_inquiry_type == "Other":
            for pattern in self.exists_patterns:
                find = pattern.search(old_inquiry_type.strip())
                if find:
                    return self.inquiry_type.get(find.group().capitalize())
            return "-"

        return new_inquiry_type

    def convert_timeline_in_tilda(self, timeline):
        if "~" in timeline:
            timeline = timeline.replace("_", " ")
            split_timeline = timeline.split("~")
            return split_timeline[0].strip() + " ~ " + split_timeline[1].strip()
        return timeline

    def less_value_categorial(self, timeline):
        find = None
        numeric_value = None
        scope = {
            "3": "Less than 3 Months",
            "6": "3 months ~ 6 months",
            "9": "6 months ~ 9 months",
        }

        if "less" in timeline:
            less_index = timeline.index("less")
            find = re.search(r"\d{1,2}", timeline[less_index:])
        if find:
            numeric_value = find.group()

            for k, v in scope.items():
                if int(numeric_value) <= int(k):
                    return v
        return timeline

    def more_value_categorial(self, timeline):
        find = None
        numeric_value = None
        scope = {
            "9": "More than a year",
            "6": "6 months ~ 9 months",
            "3": "3 months ~ 6 months",
            "0": "Less than 3 Months",
        }

        if "more" in timeline:
            more_index = timeline.index("more")
            find = re.search(r"\d{1,2}", timeline[more_index:])

        if find:
            numeric_value = find.group()

            for k, v in scope.items():
                if int(numeric_value) >= int(k):
                    return v
        return timeline.replace("_", " ")

    def timeline_retry_unknown_value_mapping(self, new_expected_timeline):
        for pattern in self.expected_timeline_exists_patterns:
            find = pattern.search(new_expected_timeline.strip())
            if find:
                return self.expected_timeline_dict.get(find.group().capitalize())

        return new_expected_timeline

    def create_expected_timeline_ratio(self, df):
        lead_owner_dict = {}
        col_name = 'new_expected_timeline'
        flag = df.groupby(col_name)['is_converted'].agg(['sum', 'count'])
        for idx, plus, counts in zip(flag.index, flag['sum'], flag['count']):
            cond = df[col_name] == idx
            ratio = (plus / counts) * 100
            df.loc[cond, f'{col_name}_converted_ratio'] = round(ratio, 2)
            lead_owner_dict[idx] = ratio

        return df

    def apply(self, df, module_list=None):
        df = self.fill(df)
        df["new_inquiry_type"] = df["inquiry_type"].apply(self.new_inquiry_type)
        df["new_inquiry_type"] = df.apply(
            lambda row: self.retry_unknown_value_mapping(
                row["new_inquiry_type"], row["inquiry_type"]
            ),
            axis=1,
        )

        df.loc[df["new_inquiry_type"] == "-", "new_inquiry_type"] = "Other"
        df["expected_timeline"].fillna("Space", inplace=True)

        df["new_expected_timeline"] = df["expected_timeline"].apply(
            self.convert_timeline_in_tilda
        )

        df["new_expected_timeline"] = df["new_expected_timeline"].apply(
            self.less_value_categorial
        )
        df["new_expected_timeline"] = df["new_expected_timeline"].apply(
            self.more_value_categorial
        )

        df["new_expected_timeline"] = df["new_expected_timeline"].apply(
            self.timeline_retry_unknown_value_mapping
        )

        df["new_expected_timeline"] = df["new_expected_timeline"].where(
            df["new_expected_timeline"].isin(self.categories), "Unknown"
        )

        df = self.create_expected_timeline_ratio(df)

        return df
