import sys
import io

from proxypool.scheduler import Scheduler

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()

if __name__ == '__main__':
    main()
