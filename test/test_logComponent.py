import pytest
from unittest.mock import patch, MagicMock
from logger.logComponent import LogComponent

@pytest.fixture
def log_component():
    return LogComponent()

@pytest.mark.asyncio
async def test_write_log(log_component):
    log_component.start()
    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        await log_component.write("Test message")
        await log_component.flush()
        mock_open.assert_called_once()  # Assert that a file was attempted to be opened
    
    await log_component.shutdown(wait=True)

@pytest.mark.asyncio
async def test_new_file_at_midnight():
    log_component = LogComponent()
    log_component.start()

    log_component._get_log_file_name = MagicMock(return_value="2023-01-01.log")
    # Mock the method to return a specific file name for the first log
    await log_component.write("Test log message")
    await log_component.flush()
    first_log_file = log_component.current_log_file
    print(first_log_file.name)

    log_component._get_log_file_name = MagicMock(return_value="2023-01-02.log")
    # Mock the method to return a different file name for the next log
    await log_component.write("Another log message")
    await log_component.flush()
    second_log_file = log_component.current_log_file
    print(second_log_file.name)

    # Asserting that different files are used for different dates
    assert first_log_file != second_log_file, "No new file created at midnight"
    await log_component.shutdown(wait=True)


@pytest.mark.asyncio
async def test_graceful_shutdown(log_component):
    log_component.start()
    log_component._get_log_file_name = MagicMock(return_value="graceful.log")
    # Add multiple log messages to the queue
    for _ in range(100):
        await log_component.write("Log message")

    await log_component.shutdown(wait=True)

    # Assert that the log file was filled with 10000000 log messages
    with open("graceful.log", "r") as file:
        log_content = file.readlines()
    assert len(log_content) == 100

    with open("graceful.log", "w") as file:
        file.write("")

@pytest.mark.asyncio
async def test_force_shutdown(log_component):
    log_component.start()
    log_component._get_log_file_name = MagicMock(return_value="force.log")
    # Add multiple log messages to the queue
    for _ in range(10):
        await log_component.write("Log message")
    await log_component.flush()
    for _ in range(10000):
        await log_component.write("Log message")

    await log_component.shutdown(wait=False)

    # Assert that the log file was filled with 10000000 log messages
    with open("force.log", "r") as file:
        log_content = file.readlines()
    assert len(log_content) < 10010

    with open("force.log", "w") as file:
        file.write("")