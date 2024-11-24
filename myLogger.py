import loguru
import os

logDir = os.path.join(os.getcwd(), 'logs')
num = (len(os.listdir(logDir)))
logPath = os.path.join(logDir, f"log_{str(num)}.log")
logger = loguru.logger
logger.add(logPath, mode='w', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", encoding='utf-8',
           rotation="1 MB", compression="zip")

if __name__ == '__main__':
    logger.info('hello world')
