import redis.asyncio as aioredis


class RedisManager:
    def __init__(self, host="localhost", port=6379, db=0):
        self._host = host
        self._port = port
        self._db = db
        self._client = None

    async def connect(self):
        if self._client is None:
            self._client = aioredis.Redis(host=self._host, port=self._port, db=self._db)

    async def disconnect(self):
        if self._client:
            await self._client.close()
            self._client = None

    async def delete_all(self):
        if self._client:
            await self._client.flushdb()

    @property
    def client(self):
        if self._client is None:
            raise RuntimeError("Redis client is not connected. Call 'connect' first.")
        return self._client

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.client.set(key, value, ex=expire)
        else:
            await self.client.set(key, value)

    async def get(self, key: str):
        return await self.client.get(key)

    async def delete(self, key: str):
        await self.client.delete(key)
