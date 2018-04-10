import InputOutput

def CreateTable(table_name, field_names, data_types):
    f = open(table_name + ".csv", "w")
    f.close()
    f = open(table_name + "_helper.csv", "w")
    f.write(",".join(name for name in field_names) + "\n")
    f.write(",".join(type for type in data_types) + "\n")
    f.close()


def Select(parameters):
    requested_data = GetRequestedData(parameters, parameters["parameter2"])
    if(parameters["parameter1"] != "*"):
        columns = parameters["parameter1"].split(",")
    else:
        columns = GetFieldNamesFromFile(parameters["parameter2"])
    special_conditions = []
    if("parameter3" in parameters):
        expressions = GetSpecialConditions(parameters)
        requested_data = GetRequestedDataAfterEvaluatingSpecialConditions(requested_data, expressions, parameters["parameter2"])

    InputOutput.DisplayRequestedData(requested_data, columns)

# Returns the requested Data after evaluating special conditions.

def GetRequestedDataAfterEvaluatingSpecialConditions(requested_data, expressions, table_name):
    updated_requested_data =[]
    data = ReadDataFromTable(table_name)
    for index, row in enumerate(data):
        is_row_satisfied = True
        for expression in expressions:
            if(expression[2] == "="):
                if(row[expression[0]] != expression[1]):
                    is_row_satisfied = False
                    break
            if (expression[2] == "<"):
                if (row[expression[0]] >= expression[1]):
                    is_row_satisfied = False
                    break
            if (expression[2] == ">"):
                if (row[expression[0]] <= expression[1]):
                    is_row_satisfied = False
                    break
            if (expression[2] == "<="):
                if (row[expression[0]] > expression[1]):
                    is_row_satisfied = False
                    break
            if (expression[2] == ">="):
                if (row[expression[0]] < expression[1]):
                    is_row_satisfied = False
                    break
        if(is_row_satisfied):
            updated_requested_data.append(requested_data[index])

    return updated_requested_data

# Returns special conditions.

def GetSpecialConditions(parameters):
    special_conditions = parameters["parameter3"].split(",")
    expressions = []
    field_name = GetFieldNamesFromFile(parameters["parameter2"])
    for index, expression in enumerate(special_conditions):
        if("<=" in expression):
            expression = expression.split("<=") + ["<="]
        elif(">=" in expression):
            expression = expression.split(">=") + [">="]
        elif ("=" in expression):
            expression = expression.split("=") + ["="]
        elif ("<" in expression):
            expression = expression.split("<") + ["<"]
        elif (">" in expression):
            expression = expression.split(">") + [">"]

        expression[0] = field_name.index(expression[0])
        expressions.append(expression)

    return expressions

def join(parameters):
    columns1 = GetRequiredColumns(parameters["parameter1"], "*")
    columns2 = GetRequiredColumns(parameters["parameter2"], "*")
    datatypes1 = GetDatatypesFromFile(parameters["parameter1"])
    datatypes2 = GetDatatypesFromFile(parameters["parameter2"])
    dict_of_datatypes = dict(zip(columns1 + columns2, datatypes1 + datatypes2))

    common_columns = list(set(columns1) & set(columns2))

    for common_column in common_columns:
        columns2.pop(columns2.index(common_column))
    columns = columns1 + columns2
    print(datatypes1)
    print(datatypes2)
    datatypes = [dict_of_datatypes[key] for key in columns]

    dict1 = GetDataIntoDic(parameters["parameter1"])
    dict2 = GetDataIntoDic(parameters["parameter2"])

    data = []
    for dict1_index in range(len(dict1[common_columns[0]])):
        row = [dict1[x][dict1_index] for x in dict1]
        if(dict1[common_columns[0]][dict1_index] in dict2[common_columns[0]]):
            dict2_index = dict2[common_columns[0]].index(dict1[common_columns[0]][dict1_index])
            row += [dict2[x][dict2_index] for x in dict2 if x not in common_columns]
        else:
            row += ["-"] * len(columns2)
        data.append(row)

    InputOutput.DisplayRequestedData(data, columns)
    CreateTable(parameters["parameter3"], columns, datatypes)
    InsertDataToFile(parameters["parameter3"], data, "w")

# Retuns Requested columns data

def GetRequestedData(parameters, table_name):

    data = GetDataIntoDic(table_name)
    required_columns = GetRequiredColumns(table_name, parameters["parameter1"])
    no_of_rows = GetNumberOfRows(data)
    requested_data = []
    row_index = 0

    while (row_index < no_of_rows):
        row = []
        for column in required_columns:
            row.append(data[column][row_index])
        requested_data.append(row)
        row_index += 1

    return requested_data

# Returns number of row in a table.

def GetNumberOfRows(data):
    value = list(data.values())
    return len(value[0])

# Returns list of columns requested.

def GetRequiredColumns(table_name, required_columns):

    if (required_columns == "*"):
        required_columns = GetFieldNamesFromFile(table_name)
    else:
        required_columns = required_columns.split(",")
    return required_columns

# Returns dict with keys as column names

def GetDataIntoDic(table_name):
    data = {}
    field_names = GetFieldNamesFromFile(table_name)
    list_of_rows = ReadDataFromTable(table_name)

    for index in range(len(field_names)):
        for row in list_of_rows:
            data.setdefault(field_names[index], [])
            data[field_names[index]].append(row[index])
    return data

# Returns the rows form the table

def ReadDataFromTable(table_name):
    f = open(table_name + ".csv", "r")
    lines = []

    while(True):
        line = f.readline()
        if not line:
            break
        lines.append(line.strip().split(","))

    f.close()
    return lines

def insert(table_name):
    field_names = GetFieldNamesFromFile(table_name)
    data_types = GetDatatypesFromFile(table_name)
    row = []
    index = 0
    length = len(field_names)

    while(index < length):
        row.append(InputOutput.TakeFieldInput(field_names[index], data_types[index]))
        index += 1

    f = open(table_name + ".csv", "a")
    f.write(",".join(str(data) for data in row) + "\n")
    f.close()

def sortby(parameters):
    keys = parameters["parameter2"].split(",")
    #dict_of_columns = dict(zip(GetFieldNamesFromFile(parameters["parameter1"]), GetDatatypesFromFile(parameters["parameter1"])))
    columns = GetFieldNamesFromFile(parameters["parameter1"])
    data = ReadDataFromTable(parameters["parameter1"])
    for key in keys:
        if(key[0] == "-"):
            data.sort(key = lambda x : x[columns.index(key[1 : ])], reverse = True)
        else:
            data.sort(key = lambda x : x[columns.index(key)])

    InputOutput.DisplayRequestedData(data, columns)
    InsertDataToFile(parameters["parameter1"], data, "a")

def find(parameters):
    table_name = parameters["parameter3"]
    requested_columns = parameters["parameter2"].split(",")
    data = ReadDataFromTable(table_name)
    operation = parameters["parameter1"]
    if(operation == "sum"):
        data = FindSum(table_name, data, requested_columns)
        AddColumn(table_name, "total", "int")
        InsertDataToFile(table_name, data, "w")
    InputOutput.DisplayRequestedData(data, GetFieldNamesFromFile(table_name))

def AddColumn(table_name, column_name, data_type):
    column_names = GetFieldNamesFromFile(table_name)
    data_types = GetDatatypesFromFile(table_name)
    column_names.append(column_name)
    data_types.append(data_type)

    f = open(table_name + "_helper.csv", "w")
    f.write(",".join(column_names) + "\n")
    f.write(",".join(data_types) + "\n")
    f.close()

def FindSum(table_name, data, requested_columns):
    columns = GetFieldNamesFromFile(table_name)
    dict_of_columns = dict(zip(columns, range(len(columns))))
    for index in range(len(data)):
        sum = 0
        for requested_column in requested_columns:
            sum += int(data[index][dict_of_columns[requested_column]])
        data[index].append(sum)
    return data

# Returns the list of column or field names.

def GetFieldNamesFromFile(table_name):
    f = open(table_name + "_helper.csv", "r")
    field_names = f.readline()
    f.close()

    field_names = field_names.strip()
    field_names = field_names.split(",")

    return field_names

# Returns list of types of column names.

def GetDatatypesFromFile(table_name):
    f = open(table_name + "_helper.csv", "r")
    field_names = f.readline()
    data_types = f.readline()
    f.close()

    data_types = data_types.strip()
    data_types = data_types.split(",")

    return data_types

def InsertDataToFile(table_name, data, mode):
    f = open(table_name + ".csv", mode)
    for row in data:
        f.write(",".join(str(x) for x in row) + "\n")
    f.close()

def PrintSyntaxes():
    print("Syntax")
    print("========")
    print("create table {table_name} {column1:type,column2:type...}")
    print("insert into {table_name}")
    print("select {column1,column2} or {*} from {table_name}")
    print("select {column1,column2} or {*} from {table_name} where {condition1,condition2}")
    print("join {table1} {table2}")
