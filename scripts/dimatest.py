import sys
from os.path import isdir, splitext
string = 'something.exi'
splitext(string)[1]
str = sys.argv[1]
if isdir(str):
    print(f'{str} is a directory, congrats (not a DIMA tho\')')
elif splitext(str)[1]==".mdb":
    print("LET THERE BE DIMA")
else:
    print("have you tried choosing a dima?")

sys.stdout.flush()
