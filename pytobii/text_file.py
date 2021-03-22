def read_txt_file(filename):
    """"
    Read eye tracker data from text file to get a list object

    :param
    filename : full file name (test_path + "participant_" + participant.__str__() + "_ID_" + ID.__str__() + ".txt")


    :return
    eye tracker data list with [x,y,time stamp] in each list element
    """
    f = open(filename, "r")
    xy_list = [line.rstrip('\n') for line in f]
    xy_list = [string.split(',') for string in xy_list]
    return xy_list


def read_fps_file(filename):
    """"
    Read fps data from text file to get a list object

    :param
    filename : full file name ( test_path + "participant_" + participant.__str__() + "_ID_" + ID.__str__() + "_FPS.txt")


    :return
    fps list
    """
    f = open(filename)
    lst = [line.rstrip('\n') for line in f]
    return lst