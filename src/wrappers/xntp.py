#!/usr/bin/env python

import argparse
import os
from os import path
from subprocess import check_call

import arg_parser
import context

def main():
    args = arg_parser.receiver_first()
    cc_repo = path.join(context.third_party_dir,'xntp')
    recv_dir = path.join(cc_repo,'xntp3-recver')
    send_dir = path.join(cc_repo,'xntp3-sender')
    
    if args.option == 'receiver':
        # cmd = [recv_dir,"-p",args.port]
        cmd = [recv_dir,"-p",args.port,"-v","-d","/opt/pantheon/third_party/xntp/recver"]
        check_call(cmd)
        return 
    
    if args.option == 'sender':
        print(send_dir)
        # cmd = [send_dir,"-a", args.ip,"-p",args.port,"-f","/opt/pantheon/third_party/xntp/video.y4m"]
        cmd = [send_dir,"-a", args.ip,"-p",args.port,"-f","/opt/pantheon/third_party/xntp/video.y4m","-v","-d","/opt/pantheon/third_party/xntp/sender"]
        check_call(cmd)
        return 

if __name__ == '__main__':
    main()