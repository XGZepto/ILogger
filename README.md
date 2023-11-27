## To use logComponent.py:

- Import the module
- Create a logger object
- call start() to start logging
- call write() to write to the log file
- call shutdown(wait=True) to initiate a graceful shutdown of the logger (keep writing until all messages are written)
- call shutdown(wait=False) to initiate an immediate shutdown of the logger (stop writing immediately)