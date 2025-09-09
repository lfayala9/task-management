from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_task_notification(task_id, notification_type):
	import os
	import django
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
	django.setup()
	from apps.tasks.models import Task
	from django.conf import settings
	try:
		task = Task.objects.get(id=task_id)
		recipients = [task.created_by.email]
		subject = f"Task {task_id} - {notification_type}"
		message = f"Task {task_id} has been {notification_type}."
		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
		return f"Email sent for task {task_id}"
	except Exception as e:
		logger.error(f"Failed to send email for task {task_id}: {str(e)}")
		return f"Failed to send email for task {task_id}: {str(e)}"

@shared_task
def generate_daily_summary():
    from django.utils import timezone
    from django.contrib.auth import get_user_model
    from django.db.models import Q
    from apps.tasks.models import Task
    from datetime import datetime, timedelta
    import logging
    
    logger = logging.getLogger(__name__)
    User = get_user_model()
    try:
        today = timezone.now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        if timezone.is_naive(start_of_day):
            start_of_day = timezone.make_aware(start_of_day)
        if timezone.is_naive(end_of_day):
            end_of_day = timezone.make_aware(end_of_day)
        users_with_tasks = User.objects.filter(
            tasks_created__isnull=False
        ).distinct()
        summaries_sent = 0
        for user in users_with_tasks:
            try:
                user_tasks_today = Task.objects.filter(
                    created_by=user,
                    created_at__range=(start_of_day, end_of_day)
                )
                tasks_created_today = user_tasks_today.count()
                pending_tasks = Task.objects.filter(
                    created_by=user,
                ).exclude(
                    Q(status='completed') | Q(completed=True)
                ).count() if hasattr(Task, 'status') or hasattr(Task, 'completed') else Task.objects.filter(created_by=user).count()
                if tasks_created_today > 0 or pending_tasks > 0:
                    subject = f"Daily Task Summary - {today.strftime('%B %d, %Y')}"
                    message = f"This is the summary"
                    if tasks_created_today > 0:
                        message += "Tasks created today:\n"
                        for task in user_tasks_today[:5]:
                            message += f"- {task.title}\n"
                        if tasks_created_today > 5:
                            message += f"... and {tasks_created_today - 5} more tasks\n"
                        message += "\n"
                    if hasattr(Task, 'due_date'):
                        upcoming_tasks = Task.objects.filter(
                            created_by=user,
                            due_date__range=(today + timedelta(days=1), today + timedelta(days=7))
                        ).exclude(
                            Q(status='completed') | Q(completed=True)
                        )[:3]
                        
                        if upcoming_tasks.exists():
                            message += "Upcoming tasks this week:\n"
                            for task in upcoming_tasks:
                                message += f"- {task.title} (due: {task.due_date.strftime('%m/%d')})\n"
                            message += "\n"
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False
                    )
                    summaries_sent += 1
            except Exception as user_error:
                logger.error(f"Error generating summary for user {user.id}: {str(user_error)}")
                continue
        result_message = f"Daily summary task completed. Summaries generated for {summaries_sent} users."
        logger.info(result_message)
        return result_message
    except Exception as e:
        error_message = f"Error in generate_daily_summary: {str(e)}"
        logger.error(error_message)
        return error_message

@shared_task
def check_overdue_tasks():
    from django.utils import timezone
    from django.contrib.auth import get_user_model
    from apps.tasks.models import Task
    from datetime import datetime
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        now = timezone.now()
        overdue_tasks = Task.objects.filter(
            due_date__lt=now,
        )  
        notifications_sent = 0
        tasks_marked = 0
        for task in overdue_tasks:
            try:
                tasks_marked += 1
                if hasattr(task, 'created_by') and task.created_by:
                    notifications_sent += 1
                if hasattr(task, 'assigned_users'):
                    for assigned_user in task.assigned_users.all():
                        logger.info(f"Overdue notification for assigned task {task.id} to {assigned_user.email}")
                        print(f"[EMAIL SIMULATION] Assigned task overdue notification sent to: {assigned_user.email}")
                        notifications_sent += 1
            except Exception as task_error:
                logger.error(f"Error processing overdue task {task.id}: {str(task_error)}")
                continue
        result_message = f"Overdue check completed. {tasks_marked} tasks processed, {notifications_sent} notifications sent."
        logger.info(result_message)
        return result_message
    except Exception as e:
        error_message = f"Error in check_overdue_tasks: {str(e)}"
        logger.error(error_message)
        return error_message

@shared_task
def cleanup_archived_tasks():
    from django.utils import timezone
    from apps.tasks.models import Task
    from datetime import timedelta
    import logging
    logger = logging.getLogger(__name__)
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        old_archived_tasks = Task.objects.filter(
            created_at__lt=thirty_days_ago,
        )
        tasks_to_delete = old_archived_tasks.count()
        if tasks_to_delete == 0:
            result_message = "No archived tasks found for cleanup."
            logger.info(result_message)
            return result_message
        deleted_task_info = []
        for task in old_archived_tasks[:10]:
            deleted_task_info.append({
                'id': task.id,
                'title': task.title,
                'created_at': task.created_at,
                'created_by': task.created_by.username if task.created_by else 'N/A'
            })
        deleted_count = old_archived_tasks.delete()
        logger.info(f"Cleanup completed. Deleted {deleted_count} archived tasks.")
        logger.info(f"Sample of deleted tasks: {deleted_task_info}")
        result_message = f"Cleanup completed. {deleted_count} archived tasks deleted (older than 30 days)."
        print(f"[CLEANUP] {result_message}")
        return result_message
    except Exception as e:
        error_message = f"Error in cleanup_archived_tasks: {str(e)}"
        logger.error(error_message)
        return error_message