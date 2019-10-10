# -*- coding: utf-8 -*-
import argparse
import sys
import re

import numpy as np


def parse_arguements(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_dir', type=str, help='', default='./logs/2n8c-n0.log')
    parser.add_argument('--output_dir', type=str, help='', default='../output')
    parser.add_argument('--model', type=str, help='', default='resnet50')
    parser.add_argument('--total_batch', type=int, help='', default=16)
    parser.add_argument('--max_step', type=int, help='', default=100)
    return parser.parse_args(argv)


def extract_time_per_step(log_dir, max_step):
    time_per_step = []
    source = open(log_dir,'r',encoding='UTF-8')
    lines = source.readlines()
    string = str(max_step) + "/"
    for line in lines:
        if line.startswith("Epoch:") & (string in line):
            p1 = re.compile(r'[(](.*?)[)]', re.S)
            time = re.findall(p1, line)
            time_per_step.append(float(time[0]))
    return time_per_step


def compute_throughput_rate(args):
    print("Computing throughput rate")
    time_per_step = np.mean(extract_time_per_step(args.log_dir, args.max_step))
    step_per_sec = 1 / time_per_step
    throughput_rate = step_per_sec * args.total_batch
    print("Throughput rate is : ", throughput_rate)


def main(args):
    print("Start to commpute:")
    compute_throughput_rate(args)


if __name__ == '__main__':
    main(parse_arguements(sys.argv[1:]))
