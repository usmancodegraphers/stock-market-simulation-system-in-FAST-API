from celery_service.celery import celery_app
from db.database import get_db
from models.user import User


@celery_app.task
def saving_transactions(user_id, new_balance: float) -> None:
    """
    Update user balance and commit changes.
    Args:
        user_id (int): User ID.
        new_balance (float): New balance value.
    Returns:
        None
    """
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.balance = new_balance
        db.commit()
        db.refresh(user)
