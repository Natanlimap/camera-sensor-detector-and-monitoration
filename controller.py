from sys import argv

import webcam

def record():
    print("Gravando")
    webcam.setHasRecordTrue()

def delete():
    print("DELETAR")
    #TODO DELETAR VIDEO

def start():
    webcam.main()

if(argv[1]=="delete"):
    delete()

