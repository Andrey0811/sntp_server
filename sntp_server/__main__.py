import argparse

from sntp_server.server import Server


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delta', type=int, default=0, help='shift time')
    parser.add_argument('-p', '--port', type=int, default=123, help='port listening')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_args()
        Server(args.delta, port=args.port).work()
    except KeyboardInterrupt:
        exit(0)
