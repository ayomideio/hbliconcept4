
# import os

# directory = "GeeksforGeeks"


# parent_dir = "C:/"


# path = os.path.join(parent_dir, directory)


# # os.mkdir(path)
# # print("Directory '% s' created" % directory)


# directory = "Geeks"

# parent_dir = "C:/GeeksforGeeks"

# mode = 0o666


# path = os.path.join(parent_dir, directory)

# try:
#     os.mkdir(path, mode)
# except OSError as error:
#     print(error)
# else:
#     print("Directory '% s' created" % directory)

# try:
#     f= open("guru9999999.txt","r")
# except OSError as error:
#     f= open("guru9999999.txt","w+")
# else:
#     # f= open("guru9999999.txt","w+")
#     print("Yes")

 if f.mode == 'r':

           contents =f.read()
           print (contents)
           search_word = "computer ip|"
           if(search_word in f.read()):
                print("word found")
           else:
                print("word not found")
                f.write("""session Id|trehad|computer ip|computername|userid|creatordate|logtype|logtext|pluginid|ic4application|ic4operation|ic4recorddate|ic4recorddatetime""")
        