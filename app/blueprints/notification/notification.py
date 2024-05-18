from flask import jsonify
from flask import Blueprint
from flask_login import current_user,login_required
from app.models import Notification
from app.extensions import db



notify_bp = Blueprint("notify", __name__)

@notify_bp.route('/inbox')
@login_required
def inbox():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    notifications_data = [
        {
            'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'message': notification.get_data().get('message', ''),
            'post_id': notification.post_id if notification.post_id else None  # 处理可能的空值
        }
        for notification in notifications
    ]
    return jsonify(notifications=notifications_data)

@notify_bp.route('/delete_all_notifications', methods=['POST'])
@login_required
def delete_all_notifications():
    Notification.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'All notifications deleted'}), 200