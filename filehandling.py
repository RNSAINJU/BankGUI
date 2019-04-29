
# f =open('test.rxr','r')
#f.close()

with open('test.txt','r') as f:
    # f_contents =f.read() prints all content in seperate lines

    #list of all line in file in list
    f_contents = f.readlines()

    #reads first line and so on
    f_contents = f.readline()

    #prints file in seperate lines
    for line in f:
        print(line)

    #prints 100 characters
    f_contents=f.read(100)

    #print all contents in seperate lines
    #looping through 10 characters
    size_to_read=10

    f_contents=f.read(size_to_read)

    while len(f_contents)>0:
        print(f_contents, end ='')
        f_contents=f.read(size_to_read)

    f.tell()

#
    size_to_read = 10

    f_contents = f.read(size_to_read)
    f.seek(0)

    f_contents=f.read(size_to_read)

with open('test.txt','r') as f: