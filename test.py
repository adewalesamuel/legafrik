def inner_func():
    raise Exception("There was and error")
    # print("hello world!")

def safe_function():
    try:
        inner_func()
    except Exception as err:
        err = str(err)
        print("An error occured !")
        print(err)
