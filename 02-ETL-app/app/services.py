
def data_preprocessor(data):
        data = data.drop(['Previous_sales'], axis=1)
        data = data.drop(['id'], axis=1)
        categorical_columns = data.select_dtypes(include=['object', 'category', 'str']).columns.tolist()
        numerical_columns = data.select_dtypes(include=['int', 'float']).columns.tolist()
        for numerical_column in numerical_columns:
            data[numerical_column] = data[numerical_column].fillna(data[numerical_column].mean())
        for cat_column in categorical_columns:
            data[cat_column] = data[cat_column].fillna(data[cat_column].mode()[0])
        return data