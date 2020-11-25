import time
from app import celery


@celery.task()
def run(arg):
    print(f"Worker invoked with {arg}")
    for i in range(10):
        time.sleep(10)
        print(f"Sleep {i*10} seconds!")
