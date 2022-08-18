def swap(main_list: list, based_on: list) -> list:
    print(based_on)
    new_list = []
    for el in based_on:
        new_list.append(main_list[el])
    return new_list