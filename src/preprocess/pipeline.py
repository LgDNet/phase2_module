def runner(data, **kwargs):
    df = kwargs.get(data)
    for value in kwargs["Instances"]:
        instance = value.get("instance")
        if param := value["params"]:
            instance = instance(**param)

        else:
            instance = instance()
        df = instance.apply(df, value.get("method"))
        
    return df
