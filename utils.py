# utils.py
import logging
import os
from datetime import datetime

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logfile = f"logs/run_{timestamp}.log"
    
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def print_summary(movies_with_directors):
    total_movies = len(movies_with_directors)
    total_directors = sum(len(directors) for _, directors in movies_with_directors)
    summary = f"\n✅ Done. Imported {total_movies} movies and {total_directors} directors.\n"
    print(summary)
    logging.info(summary.strip())
