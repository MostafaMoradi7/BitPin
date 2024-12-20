from celery import shared_task
from redis import Redis
from django.conf import settings
import logging

# Initialize Redis client
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

logger = logging.getLogger(__name__)

VOTE_THRESHOLD_PERIOD = int(settings.VOTE_THRESHOLD_PERIOD)
VOTE_THRESHOLD_COUNT_LIMIT = int(settings.VOTE_THRESHOLD_COUNT_LIMIT)
LOCK_DURATION = int(settings.LOCK_DURATION)


@shared_task(queue="vote_queue")
def process_votes(content_id):
    """
    Celery task to process a single vote for the given content_id.
    Handles rate limiting, locking, and vote counting.
    """
    logger.info(f"Processing vote for content_id {content_id}...")
    logger.info(f"VOTE_THRESHOLD_PERIOD: {VOTE_THRESHOLD_PERIOD}")
    logger.info(f"VOTE_THRESHOLD_COUNT_LIMIT: {VOTE_THRESHOLD_COUNT_LIMIT}")
    logger.info(f"LOCK_DURATION: {LOCK_DURATION}")
    vote_count_key = f"content_{content_id}_vote_count"
    lock_key = f"content_{content_id}_locked"

    if redis_client.exists(lock_key):
        ttl = redis_client.ttl(lock_key)
        logger.warning(
            f"Content ID {content_id} is locked. TTL: {ttl if ttl > 0 else 'Expired'} seconds."
        )
        return "Content is locked"

    try:
        current_count = redis_client.incr(vote_count_key)
        logger.info(f"Current vote count for content_id {content_id}: {current_count}")

        if current_count == 1:
            redis_client.expire(vote_count_key, VOTE_THRESHOLD_PERIOD)
            logger.info(
                f"Set expiration for vote_count_key {vote_count_key}: {VOTE_THRESHOLD_PERIOD} seconds."
            )

        if current_count > VOTE_THRESHOLD_COUNT_LIMIT:
            redis_client.delete(vote_count_key)  # Reset the counter
            redis_client.set(lock_key, 1, ex=LOCK_DURATION)
            logger.warning(
                f"Threshold exceeded for content_id {content_id}. Counter reset and lock applied for {LOCK_DURATION} seconds."
            )
    except Exception as e:
        logger.error(f"Error processing vote for content_id {content_id}: {e}")
