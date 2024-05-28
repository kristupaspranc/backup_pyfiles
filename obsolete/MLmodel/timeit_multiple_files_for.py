import matplotlib.pyplot as plt
from timeit import Timer


def pythonic_way(all_columns, target_columns):
    for target in target_columns:
        if target not in all_columns:
            raise ValueError(
                f"Provided target not in given columns: \ntarget => \
                    {target}\ncolumns => {all_columns}")
    
    target_indices = [all_columns.index(target) for target in target_columns]


def pythonic_way_ed(all_columns, target_columns):
    if not all(target in all_columns for target in target_columns):
        print(True)
    
    target_indices = [all_columns.index(target) for target in target_columns]


def old_way(all_columns, target_columns):
    target_indices = []

    for target in target_columns:
        if target in all_columns:
            target_indices.append(all_columns.index(target))
        else:
            raise ValueError(
                f"Provided target not in given columns: \ntarget => \
                    {target}\ncolumns => {all_columns}"
            )


def single_list_comprehension(all_columns, target_columns):
    d = [all_columns.index(target) if target in all_columns else target for target in target_columns]

    # if len(d)<len(target_columns):
    #     raise ValueError


if __name__ == "__main__":
    a = [str(x) for x in range(1000)]
    b = [str(x) for x in range(0,1000,2)]

    print("Pythonic_way")
    t1 = Timer(lambda: pythonic_way(a,b))
    pw = [t1.timeit(number=1) for _ in range(100)]

    print("Pythonic_way_edited")
    t4 = Timer(lambda: pythonic_way_ed(a,b))
    pwe = [t4.timeit(number=1) for _ in range(100)]

    print("Old way")
    t2 = Timer(lambda: old_way(a,b))
    ow = [t2.timeit(number=1) for _ in range(100)]

    print("Single list comprehension")
    t3 = Timer(lambda: single_list_comprehension(a,b))
    sw = [t3.timeit(number=1) for _ in range(100)]

    # Plot the losses
    plt.plot(pw,label="pythonic_way")
    plt.plot(pw,label="pythonic_way_ed")
    plt.plot(ow,label="old_way")
    #plt.plot(sw,label="single_list_comprehension")
    plt.xlabel("no. of epochs")
    plt.ylabel("total loss")
    plt.legend()
    plt.show()

