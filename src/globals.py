import matplotlib


def init() -> None:
    """Initialize the global variables"""
    global CAN_SHOW_GRAPH
    global WHATSAPP_MEMBER_LIMIT
    global SIGNAL_MEMBER_LIMIT
    global HOURS_LIST

    try:
        matplotlib.use('TkAgg')
        CAN_SHOW_GRAPH = True
    except ImportError:
        print('Warning: Tkinter is not installed, graphs will not be shown')
        CAN_SHOW_GRAPH = False

    WHATSAPP_MEMBER_LIMIT = 256

    SIGNAL_MEMBER_LIMIT = 1000

    HOURS_LIST = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                  '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
