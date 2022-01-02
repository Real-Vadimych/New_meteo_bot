def send(x):
    #put your sending code here
    answer.append(x)


def cutter(s):
    global answer
    answer = []
    s= s.split("\n") # divides the string into lines
 #   print(s)
    #we want to send as many lines as possible without the total size of the sent string being over limit
    limit = 1800 #make this whatever you want
    sending = ""
    total = 0

    for line in s:
        if total + len(line) > limit:
            send(sending[:-1])
            total = len(line)
            sending = line + "\n"
        else:
            total += len(line)
            sending += line + "\n"
    #need to send the final string; there is probably a better way to do this, especially because this will break if the first if is entered on the last iteration
    send(sending[:-1])
    
    return answer