import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        self._db = redis.Redis(host=host, port=port)

        """
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
        """

    def get(self,count=1):
        proxies = self._db.lrange("proxies", 0, count-1)
        self._db.ltrim('proxies', count, -1)
        return proxies

    def put(self, proxy):
        self._db.rpush('proxies', proxy)

    def pop(self):
        try:
            return self._db.rpop('proxies').decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        return self._db.llen('proxies')

    def flush(self):
        self._db.flushall()

if __name__ == '__main__':
    conn = RedisClient()
    #print(conn.pop())
