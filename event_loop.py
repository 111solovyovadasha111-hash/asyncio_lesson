from collections import deque

messages = deque()
while True:
    if messages:
        message = messages.pop()
        process_message(message)