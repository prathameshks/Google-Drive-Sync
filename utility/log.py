from os import path


def write_log(message: str):
    with open("debug.log", "a") as f:
        f.write(message + "\n")


def write_to_file(*messages, file_name: str = "debug.log", end: str = "\n"):
    if path.exists(file_name):
        with open(file_name, "a") as f:
            f.write(" ".join(messages) + end)
    else:
        with open(file_name, "w") as f:
            f.write(" ".join(messages) + end)

def pretty_print_dict(dict_to_print:dict)->str:
    ans = ""
    ans += '{\n'
    for key, value in dict_to_print.items():
        ans += f"\t {key} : {value}, \n"
    ans += '}\n'
    return ans
    