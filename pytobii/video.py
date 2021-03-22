import cv2
import glob
import screeninfo
import time


def read_video(num):
    dir_path = "../../../../videos/" + num.__str__() + "/"
    file_name = glob.glob(dir_path + "*.jpg")
    file_name.sort()
    frame_lst = [cv2.imread(img) for img in file_name]
    frame_size = frame_lst[0].shape[0:2]
    frame_size = (frame_size[1], frame_size[0])
    return frame_lst, frame_size


def display_first(frame, window_name):
    cv2.imshow(window_name, frame)


def display_video(frame_lst, window_name):

    show = True
    time_lst = []
    last_time = time.time()
    for i in range(0, len(frame_lst)):
        frame = frame_lst[i]
        cv2.imshow(window_name, frame)
        current_time = time.time()
        time_lst.append(1/(current_time - last_time))
        last_time = current_time
        if i == len(frame_lst)-1:
            show = False
            frame_nr = i

        if cv2.waitKey(1) & 0xFF == ord('q'):
            show = False
            frame_nr = i
            break
    return show, frame_nr, time_lst


def make_video(frame_lst):
    h,w,l = frame_lst[0].shape
    size = (w,h)
    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(frame_lst)):
        out.write(frame_lst[i])
    out.release()
