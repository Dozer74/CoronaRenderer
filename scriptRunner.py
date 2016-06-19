# coding=utf-8
import os
import sys
import argparse

sys.path.append(os.path.realpath('maxconnect'))
import maxconnect


def readArgs():
    """
    производит чтнение аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timeLimit", type=int, help="sets time limit in sec", default=0)
    parser.add_argument("-n", "--noiseLimit", type=float, help="sets noise limit", default=0)
    parser.add_argument("-p", "--passLimit", type=int, help="sets pass limit", default=0)
    parser.add_argument("-rp", "--resultsPath", type=str, help="sets path to file with results",
                        default=os.path.expanduser("~/Desktop/results.txt"))
    return parser.parse_args()


def writeArgsToFile(args):
    """
    записывает аргументы в файл. После чтения в main.py файл удаляется
    """
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'params.txt')
    f = open(path, 'w')
    f.writelines(
        [str(args.passLimit) + '\n', str(args.noiseLimit) + '\n', str(args.timeLimit) + '\n', args.resultsPath])
    f.close()


args = readArgs()
writeArgsToFile(args)
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'main.py')
cmd = r'python.ExecuteFile @"%s";' % filename
maxconnect.scriptrunner.run(cmd)
