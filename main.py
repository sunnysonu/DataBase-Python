import Interpreter
import InputOutput

def main():
    repeat = True
    while(repeat):
        query = InputOutput.TakeCommand()
        parameters, is_syntax_correct = Interpreter.SyntaxAnalyzer(query)
        if(is_syntax_correct):
            repeat = Interpreter.ImplementOperations(parameters)
        else:
            print("Syntax Error")

if __name__ == "__main__":
    main()