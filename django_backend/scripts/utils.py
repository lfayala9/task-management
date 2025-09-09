from rest_framework_simplejwt.tokens import RefreshToken
from apps.tasks.celery_tasks import send_task_notification
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def authenticate_request(request):
		auth = JWTAuthentication()
		try:
			user_auth_tuple = auth.authenticate(request)
			if user_auth_tuple is not None:
				return user_auth_tuple[0]
		except AuthenticationFailed as e:
			logger.error(f"Authentication failed: {str(e)}")
			return None
		return None


def get_token(user):
	refresh = RefreshToken.for_user(user)
	return {
		'refresh': str(refresh),
		'access': str(refresh.access_token),
	}

def test_notification(request):
    try:
        result = send_task_notification.delay(1, "task_created")
        return JsonResponse({
            "status": "Task enqueued", 
            "task_id": result.id
        })
    except Exception as e:
        return JsonResponse({
            "status": "Error", 
            "error": str(e)
        }, status=500)
