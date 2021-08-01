from sys import argv
import os
import webcam
import parser

def record():
    print("Gravando")
    webcam.setHasRecordTrue()

def delete(index):
    print("DELETAR")
    os.remove(f'./videos/output{index}.avi')

