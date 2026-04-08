import random

def generate_task():
    task_type = random.choice(["spam", "meeting", "complaint"])

    if task_type == "meeting":
        return {
            "id": "meeting",
            "email": {
                "sender": "manager@company.com",
                "subject": "Schedule Meeting",
                "body": f"Let's meet at {random.choice(['10 AM','2 PM','4 PM'])}"
            },
            "expected": {
                "action_type": "reply",
                "priority": "medium"
            }
        }

    if task_type == "complaint":
        return {
            "id": "complaint",
            "email": {
                "sender": "customer@shop.com",
                "subject": "Issue with product",
                "body": random.choice([
                    "Product is damaged",
                    "Delivery was late",
                    "Wrong item received"
                ])
            },
            "expected": {
                "action_type": "reply",
                "priority": "high"
            }
        }

    return {
        "id": "spam",
        "email": {
            "sender": "promo@spam.com",
            "subject": "FREE CASH!!!",
            "body": "Click now to win money"
        },
        "expected": {
            "action_type": "ignore",
            "priority": "low"
        }
    }