def swap(main_list: list, based_on: list) -> list:
    for ind, el in enumerate(based_on):
        temp = main_list[el]
        main_list[el] = main_list[ind]
        main_list[ind] = temp
    return main_list