# pytobii
Cython interface to tobii PDK (https://developer.tobii.com/4l-pdk/)


Run tracker:


Optional flags:
- p x Participant number (x is an integer)

-f x Which video number to use (x is an integer)

-t Show execution times


Example:
Run with for participant 1, video number 2 and show time information:
python3 run.py -p 1 -f 1 -t 

Keyboard shortcuts:

Press p to start the test
Press q to exit