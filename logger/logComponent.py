import asyncio
import datetime

from logger.ilog import ILog

class LogComponent(ILog):
    def __init__(self):
        self.log_queue = asyncio.Queue()
        self.current_log_file = None
        self._stop_signal = object()
        self._stop_event = asyncio.Event()
        self.new_message_event = asyncio.Event()
        self._writer_task = None

    def start(self):
        if self._writer_task is None:
            self._writer_task = asyncio.create_task(self._write_logs())

    def _get_log_file_name(self):
        return datetime.datetime.now().strftime("%Y-%m-%d.log")

    async def _write_logs(self):
        while not self._stop_event.is_set():
            await self.new_message_event.wait()
            self.new_message_event.clear()

            while not self.log_queue.empty():
                message = self.log_queue.get_nowait()
                self.log_queue.task_done()

                if message is self._stop_signal:
                    self._stop_event.set()
                    break

                if self.current_log_file is None or self.current_log_file.name != self._get_log_file_name():
                    if self.current_log_file is not None:
                        self.current_log_file.close()
                    self.current_log_file = open(self._get_log_file_name(), 'a')

                try:
                    print(message, file=self.current_log_file)  # Write to log file
                except Exception as e:
                    print(f"Error writing log: {e}")

    async def flush(self):
        await self.log_queue.join()

    async def write(self, message: str):
        await self.log_queue.put(message)
        self.new_message_event.set()

    async def shutdown(self, wait: bool):
        await self.log_queue.put(self._stop_signal)
        self.new_message_event.set()
        if wait:
            await self.log_queue.join()
        else:
            while not self.log_queue.empty():
                self.log_queue.get_nowait()
                self.log_queue.task_done()

        self._stop_event.set()
        await self._writer_task

        if self.current_log_file is not None:
            self.current_log_file.close()
            self.current_log_file = None
        
        self._stop_event.clear()
        self._writer_task = None