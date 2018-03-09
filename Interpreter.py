import operations

parse_string = {"create": ["create", "table", "parameter1", "parameter2"],
                "insert": ["insert", "into", "parameter1"],
                "select": ["select", "parameter1", "from", "parameter2", "where", "parameter3"],
                "join": ["join", "parameter1", "parameter2"],
                "exit": ["exit"],
                "help" : ["help"]}


def SyntaxAnalyzer(query):
    parameters = {}
    splitted_query = query.split(" ")
    is_correct_syntax = True

    if(splitted_query[0] in parse_string):
        parameters["operation"] = splitted_query[0]
        index = 0

        while(index < min(len(splitted_query), len(parse_string[splitted_query[0]]))):
            keyword = parse_string[splitted_query[0]][index]

            if("parameter" not in keyword and "secondary_syntax" not in keyword):
                if(splitted_query[index] != keyword):
                    is_correct_syntax = False
                    break
            else:
                parameters[keyword] = splitted_query[index]
            index += 1

        if("where" in parse_string[splitted_query[0]]):
            if(index != parse_string[splitted_query[0]].index("where") and index != len(parse_string[splitted_query[0]])):
                is_correct_syntax = False
        else:
            if(index != len(parse_string[splitted_query[0]])):
                is_correct_syntax = False
    else:
        is_correct_syntax = False

    return parameters, is_correct_syntax

def ImplementOperations(parameters):

    if(parameters["operation"] == "create"):
        field_names, data_types = GetFieldNamesAndDatatypes(parameters["parameter2"])
        operations.CreateTable(parameters["parameter1"], field_names, data_types)
        return True

    elif(parameters["operation"] == "insert"):
        operations.insert(parameters["parameter1"])
        return True

    elif(parameters["operation"] == "select"):
        operations.Select(parameters)
        return True

    elif(parameters["operation"] == "exit"):
        return False

    elif(parameters["operation"] == "help"):
        operations.PrintSyntaxes()
        return True

    elif(parameters["operation"] == "join"):
        operations.join(parameters)
        return True


def GetFieldNamesAndDatatypes(fields):
    fields = fields.split(",")
    field_names = []
    data_types = []
    for field in fields:
        field = field.split(":")
        field_names.append(field[0])
        data_types.append(field[1])

    print(field_names, data_types)
    return field_names, data_types

