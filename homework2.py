def is_bush(potential_bush, valid_names):
    name = potential_bush.get("name", "").lower()
    return name in valid_names


def is_not_too_expensive(sum_of_costs):
    return sum_of_costs <= 42.00


def looks_nice(sum_of_costs, unique_symbols):
    if int(sum_of_costs) != 0:
        return len(unique_symbols) % int(sum_of_costs) == 0
    else:
        return False


def function_that_says_ni(*args, **kwargs):
    valid_names = ["храст", "shrub", "bush"]
    sum_of_costs = 0
    unique_symbols = set()

    for arg in args:
        if isinstance(arg, dict) and is_bush(arg, valid_names):
            sum_of_costs += arg.get("cost", 0)

    for key, potential_bush in kwargs.items():
        if isinstance(potential_bush, dict) and is_bush(potential_bush, valid_names):
            sum_of_costs += potential_bush.get("cost", 0)
            unique_symbols.update(set(key))

    if is_not_too_expensive(sum_of_costs) and looks_nice(sum_of_costs, unique_symbols):
        return "{:.2f}лв".format(sum_of_costs)
    else:
        return "Ni!"
