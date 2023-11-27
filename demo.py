import asyncio
import datetime
from logger.logComponent import LogComponent

async def log_messages(log_component, num_messages=5, delay=1):
    for i in range(num_messages):
        message = f"[{datetime.datetime.now()}] Log message {i+1}"
        print("Writing message:", message)
        await log_component.write(message)
        await asyncio.sleep(delay)

async def main():
    # Initialize the LogComponent
    log_component = LogComponent()
    log_component.start()

    # Log some messages
    await log_messages(log_component, num_messages=10, delay=0.5)

    # Demonstrate shutdown behavior
    print("Initiating graceful shutdown (waiting for queue to empty)...")
    await log_component.shutdown(wait=True)
    print("Shutdown complete.")

    # Restarting the component to demonstrate immediate shutdown
    log_component.start()
    await log_messages(log_component, num_messages=5, delay=0.5)
    await log_messages(log_component, num_messages=10, delay=0.000001)
    print("Initiating immediate shutdown (not waiting for queue to empty)...")
    await log_component.shutdown(wait=False)
    print("Immediate shutdown complete.")

# Run the demo
asyncio.run(main())
