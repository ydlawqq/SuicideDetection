import asyncio
import logging
import contextlib
logger = logging.getLogger(__name__)



class BatchWorker():
    def __init__(self, predictor, 
                 batch_size: int = 8, 
                 time_limit: float = 1.0):
        self.predictor = predictor
        self.batch_size = batch_size
        self.time_limit = time_limit
        self.queue = asyncio.Queue()
        self._inflight = []

    async def score(self, text: str):
        fut = asyncio.get_running_loop().create_future()
        await self.queue.put((text, fut))
        return await fut

    async def _collect(self):
        first = await self.queue.get()
        items = [first]
        while len(items) < self.batch_size:
            try:
                more = await asyncio.wait_for(self.queue.get(), timeout=self.time_limit)
                items.append(more)
            except asyncio.TimeoutError:
                break
        return items
        
    async def _process(self, items: list[tuple]):
        texts = [t for t, _ in items]
        try:
            logger.info('Вычисление скоров')
            scores = await asyncio.to_thread(self.predictor.predict, texts)
            for (text, fut), score in zip(items, scores):
                fut.set_result(score)

        except Exception as e:
            logger.exception('Батч упал')
            for _, fut in items:
                fut.set_exception(e)
            
        finally:
            logger.debug('В батче: %s', len(items))

    async def _run(self):
        while True:
            logger.info('Берет items')
            items = await self._collect()
            self._inflight = items
        
            try:
                await self._process(items)
            finally:
                self._inflight = None

    async def start(self):
        logger.info('Запуск генерации')
        self._task = asyncio.create_task(self._run())


    async def stop(self):
        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
        while not self.queue.empty():
            _, fut = self.queue.get_nowait()
            fut.set_exception(RuntimeError('Остановка сервиса'))
        if self._inflight:
            for _, fut in self._inflight:
                fut.set_exception(RuntimeError('Остановка сервиса'))