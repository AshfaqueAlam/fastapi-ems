# app/tasks.py
from datetime import datetime
from worker import celery_app
# from sqlalchemy import select, func
from core.database import get_session
from app.models import Event, EventStatus

@celery_app.task(name="worker.tasks.update_completed_events")
def update_completed_events():
    """
    Task to update events to COMPLETED if their end_time has passed.
    """
    session = get_session()
    try:
        current_time = datetime.now(datetime.timezone.utc)
        print("current_time--->", current_time)
        # Query events that are not yet completed and whose end_time is in the past.
        events_to_update = session.query(Event).filter(
            Event.end_time <= current_time,
            Event.status != EventStatus.COMPLETED
        ).all()
        print("events_to_update---> ", events_to_update)

        if events_to_update:
            print("### events_to_update ### ---> ", events_to_update)
            for event in events_to_update:
                event.status = EventStatus.COMPLETED
                # Optionally, log or print the update for audit purposes.
                print(f"Event ID {event.event_id} updated to COMPLETED.")

            # Commit all changes in one transaction.
            session.commit()
        else:
            print("No events to update at this time.")

    except Exception as e:
        session.rollback()
        # Log the exception as appropriate in your application.
        print(f"Error updating events: {e}")
        raise e
    finally:
        session.close()

