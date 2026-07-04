import uuid
from typing import List
from shared_libs.core.contracts.publishing import PublishingContext, NotificationMessage

class NotificationEngine:
    def generate(self, context: PublishingContext) -> List[NotificationMessage]:
        """
        Pure Python. Generates structurally formatted NotificationMessage objects.
        Supports Executive, Manager, Technical verbosity.
        DOES NOT actually dispatch to Telegram/Slack directly here.
        """
        notifications = []
        
        dec_ids = [d.decision_id for d in context.decision_package.business_decisions]
        
        # 1. Executive
        notifications.append(NotificationMessage(
            message_id=str(uuid.uuid4()),
            channel="Telegram",
            verbosity="Executive",
            subject=f"AAOS Alert: {context.branding.company_name}",
            body=f"Decisions approved: {len(dec_ids)}. Critical risks detected: {len(context.decision_package.risk_assessments)}.",
            decision_ids=dec_ids
        ))
        
        # 2. Manager
        notifications.append(NotificationMessage(
            message_id=str(uuid.uuid4()),
            channel="Slack",
            verbosity="Manager",
            subject="Action Plan Generated",
            body=f"New actions assigned. {len(context.decision_package.business_actions)} actions in pipeline.",
            decision_ids=dec_ids
        ))
        
        # 3. Technical
        notifications.append(NotificationMessage(
            message_id=str(uuid.uuid4()),
            channel="Teams",
            verbosity="Technical",
            subject="Execution Trace",
            body=f"Pipeline executed successfully. Execution IDs attached.",
            decision_ids=dec_ids
        ))
        
        return notifications
