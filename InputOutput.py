def TakeCommand():
    return input("\n>>> ")

def DisplayRow(row):
    print(row)

def TakeFieldInput(field_name, data_type):
    if(data_type == "int"):
        return int(input(field_name + ":"))
    elif(data_type == "float"):
        return float(input(field_name + ":"))
    elif(data_type == "bool"):
        return bool(input(field_name + ":"))
    elif(data_type == "str"):
        return input(field_name + ":")

def PrintHeading(columns):
    column_name = ""
    for column in columns:
        column_name += column + (" " * (20 - len(column)))
    DisplayRow(column_name)
    print("-" * 20 * len(columns))

def DisplayRequestedData(requested_data, columns):
    PrintHeading(columns)

    for row in requested_data:
        DisplayRow(ConvertToSpaceSeparatedString(row))

def ConvertToSpaceSeparatedString(row):
    s = ""
    for word in row:
        s += str(word) + (" " * (20 - len(word)))

    return s