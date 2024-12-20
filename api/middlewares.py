import logging
import json
from redis import Redis
from django.conf import settings
from api.tasks import process_votes  # Import the Celery task

logger = logging.getLogger(__name__)

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class VoteRateLimiterMiddleware:
    """
    Middleware to enqueue votes for Celery processing.
    The actual vote processing (e.g., rate limiting, locking, etc.)
    will happen in the Celery task.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.vote_api_path = "/api/vote/"

    def __call__(self, request):
        if request.method == "POST" and request.path == self.vote_api_path:
            logger.info(f"Received a POST request to {self.vote_api_path}.")

            content_id = self._get_content_id(request)
            if content_id:
                logger.info(f"Adding vote for content_id {content_id} to Celery queue.")
                self._enqueue_vote(content_id)
            else:
                logger.warning("Invalid content_id in request. Skipping.")

        return self.get_response(request)

    def _get_content_id(self, request):
        """
        Extract the content_id from the POST request body.
        """
        try:
            data = json.loads(request.body)
            return data.get("content")
        except Exception as e:
            logger.error(f"Error parsing content_id from request: {e}")
            return None

    def _enqueue_vote(self, content_id):
        """
        Enqueue the vote into the Celery task queue for processing.
        """
        try:
            process_votes.delay(content_id)
            logger.info(f"Vote for content_id {content_id} enqueued successfully.")
        except Exception as e:
            logger.error(f"Error enqueueing vote for content_id {content_id}: {e}")
