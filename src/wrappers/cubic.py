#!/usr/bin/env python

from subprocess import check_call

import arg_parser


def main():
    args = arg_parser.receiver_first()

    if args.option == 'deps':
        print('iperf')
        return

    # iperf -Z 代表使用0拷贝方式发送数据
    # -s 运行服务器模式
    if args.option == 'receiver':
        cmd = ['iperf', '-Z', 'cubic', '-s', '-p', args.port]
        check_call(cmd)
        return

    # -c 代表以客户端方式运行， -t 传输时间
    if args.option == 'sender':
        cmd = ['iperf', '-Z', 'cubic', '-c', args.ip, '-p', args.port,
               '-t', '75']
        check_call(cmd)
        return


if __name__ == '__main__':
    main()
