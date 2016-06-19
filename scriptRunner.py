# coding=utf-8
import os
import sys
import argparse

sys.path.append(os.path.realpath('maxconnect'))
import maxconnect

parampath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'params.txt')


def get_limits(args):
    f = open(parampath,'w')
    f.writelines(['get\n', args.path])
    f.close()


def set_limits(args):
    f = open(parampath, 'w')
    f.writelines(['set\n',
                  str(args.passLimit)+'\n',
                  str(args.noiseLimit)+'\n',
                  str(args.timeLimit)+'\n'])
    f.close()


def read_args():
    """
    производит чтнение аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='List of commands')
    # get parser
    getlimits_parser = subparsers.add_parser('get', help='Get the values of limits')
    getlimits_parser.add_argument('-path', dest='path', type=str,
                                  help='Path to file with result',
                                  default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'limits.txt'))
    getlimits_parser.set_defaults(func=get_limits)
    # set parser
    setlimits_parser = subparsers.add_parser('set', help='Set the values of limits')
    setlimits_parser.add_argument('-p', '--passLimit', type=int, default=-1, help='Pass limit value')
    setlimits_parser.add_argument('-n', '--noiseLimit', type=float, default=-1.0, help='Noise limit value')
    setlimits_parser.add_argument('-t', '--timeLimit', type=int, default=-1, help='Time limit value (in seconds)')
    setlimits_parser.set_defaults(func=set_limits)
    return parser.parse_args()


args = read_args()
args.func(args)
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'main.py')
cmd = r'python.ExecuteFile @"%s";' % filename
maxconnect.scriptrunner.run(cmd)
