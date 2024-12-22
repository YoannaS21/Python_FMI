def type_check(context):
    def decorator(*types):
        def wrapper(func):
            def inner(*args, **kwargs):
                if context == 'in':
                    all_types_ok = True
                    types_list = args + tuple(kwargs.value())
                    for arg in types_list:
                        if not isinstance(arg, types):
                            all_types_ok = False
                            break
                    if not all_types_ok:
                        string_with_types = ','.join(
                            [f'<{str(kind)}>'for kind in types])
                        print(
                            f"Invalid input arguments, expected {string_with_types}!")

                result_from_function = func(*args, **kwargs)

                if context == 'out':
                    if not isinstance(result_from_function, types):
                        string_with_types = ','.join(
                            [f'{str(kind)}'for kind in types])
                        print(
                            f"Invalid output arguments, expected {string_with_types}!")
                return result_from_function
            return inner
        return wrapper
    return decorator
