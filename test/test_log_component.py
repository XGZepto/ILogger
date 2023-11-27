import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from logger.logComponent import LogComponent

@pytest.fixture
def log_component():
    return LogComponent()

@pytest.mark.asyncio
async def test_write_log(log_component):
    log_component.start()
    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        await log_component.write("Test message")
        mock_open.assert_called_once()  # Assert that a file was attempted to be opened

    await log_component.shutdown(wait=True)

# @pytest.mark.asyncio
# async def test_file_rotation(log_component):
#     log_component.start()
#     with patch('log_component.LogComponent._get_log_file_name') as mock_get_log_file_name:
#         # Simulate a file name based on different dates
#         mock_get_log_file_name.side_effect = lambda: datetime.now().strftime("%Y-%m-%d.log")

#         # Write a log to initialize the log file
#         await log_component.write("Initial log message")

#         # Simulate the passing of a day
#         mock_get_log_file_name.side_effect = lambda: (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d.log")

#         # Write another log for the next day
#         await log_component.write("Log message after midnight")

#         # Expect two different files to be created
#         assert mock_get_log_file_name.call_count == 2

#     await log_component.shutdown(wait=True)

# @pytest.mark.asyncio
# async def test_graceful_shutdown(log_component):
#     log_component.start()
#     with patch('builtins.open', new_callable=MagicMock) as mock_open:
#         # Add multiple log messages to the queue
#         for _ in range(10):
#             await log_component.write("Log message")

#         # Shutdown without waiting for the queue to empty
#         await log_component.shutdown(wait=False)
#         # The log file should be opened only once since we're not waiting
#         mock_open.assert_called_once()

#         # Reset the mock for the next part of the test
#         mock_open.reset_mock()

#         # Add more log messages
#         for _ in range(10):
#             await log_component.write("Log message")

#         # This time, wait for the queue to empty before shutting down
#         await log_component.shutdown(wait=True)
#         # The log file should be opened again for the new messages
#         mock_open.assert_called_once()

# @pytest.mark.asyncio
# async def test_error_handling_in_logging(log_component):
#     log_component.start()
#     with patch('builtins.open', side_effect=Exception("File open error")), \
#          patch('log_component.print') as mock_print:
#         await log_component.write("Log message that triggers an error")
        
#         # Check if the error is caught and printed
#         mock_print.assert_called_with("Error writing log: File open error")

#     await log_component.shutdown(wait=True)
