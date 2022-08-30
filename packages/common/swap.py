def swap(main_list: list, based_on: list) -> list:
    """swap arranges a list based on another indexed list.


    Args:
        main_list (list): The list that you want to be arranged. e.g.: ['red', 'blue', 'green']
        based_on (list): The list that you wnat the main list be arranged based on. e.g.: [0, 2, 1]

    Returns:
        list: Arranged list. e.g.: ['red', 'green', 'blue']
    """
    new_list = []
    for el in based_on:
        new_list.append(main_list[el])
    return new_list