import sys
from main import main

"""     

    RUN THIS FILE TO START THE PROGRAM

    Optional flags:
    -f video file number
    -p participant number 
    -t show time

"""

if __name__ == "__main__":

    args = sys.argv

    if len(args) == 1:
        main(1, False)

    elif len(args) > 1:

        if "-f" in args:
            for i in range(len(args)):
                if args[i] == "-f":

                    if len(args[i + 1]) == 1:
                        num = (int(args[i + 1]))

                        if num > 5:
                            raise ValueError("File number must be 1,2,3,4,5,6,7,8 or 9.")
                        break

                    else:
                        raise ValueError("File number must be 1,2,3,4,5,6,7,8 or 9.")
        else:
            num = (1)

        if "-p" in args:
            for i in range(len(args)):
                if args[i] == "-p":

                    if len(args[i + 1]) == 1:
                        p = (int(args[i + 1]))

                        if p > 5:
                            raise ValueError("Participant number must be 1,2,3,4 or 5.")
                        break

                    else:
                        raise ValueError("Participant number must be 1,2,3,4 or 5.")
        else:
            p = (1)

        if "-t" in args:
            t = True
        else:
            t = False

        main(num, t,p)
