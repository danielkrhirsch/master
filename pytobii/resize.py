import screeninfo
import cv2


def resize_video(lst, screen_nr):
    """"
    Resize video to be able to show on full screen

    :param
    lst : frame list
    screen_nr : the number of the screen where the eye tracker is placed (should be 2)


    :return
    new_lst : scaled version of input lst
    window_name : used for later plots to get correct window resolution
    new_size : (width, height) of the frame sin new_lst
    """
    new_lst = []
    screen = screeninfo.get_monitors()[screen_nr]
    window_name = 'Video'
    # Comment out the two lines below if the function is used for analysis
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    s_w = screen.width
    s_h = screen.height
    v_w = lst[0].shape[1]
    v_h = lst[0].shape[0]
    scale_w = v_w/s_w
    scale_h = v_h/s_h

    if scale_w != scale_h:
        if scale_w < scale_h:
            width = int(v_w*(scale_h*s_w/v_w))
            height = v_h
        else:
            height = int(v_h*(scale_w*s_h/v_h))
            width = v_w
    else:
        width = v_w
        height = v_h

    for i in range(0, len(lst)):
        frame = lst[i]
        new_frame = cv2.resize(frame, (width, height))
        new_lst.append(new_frame)
    new_size = new_lst[0].shape[0:2]
    new_frame_size = (new_size[1], new_size[0])
    return new_lst, window_name, new_size