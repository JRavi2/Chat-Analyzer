import matplotlib


def init() -> None:
    """Initialize the global variables"""
    global CAN_SHOW_GRAPH
    global hours_list

    try:
        matplotlib.use('TkAgg')
        CAN_SHOW_GRAPH = True
    except ImportError:
        print('Warning: Tkinter is not installed, graphs will not be shown')
        CAN_SHOW_GRAPH = False
