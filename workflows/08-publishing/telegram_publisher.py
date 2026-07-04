import os
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger("TelegramPublisher")

class TelegramPublisherCapability:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publishes content to a Telegram channel.
        """
        logger.info("TelegramPublisherCapability executing")
        
        content = payload.get("content", "")
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID", "@your_channel")
        
        if not bot_token or bot_token == "your_telegram_token_here":
            logger.warning("TELEGRAM_BOT_TOKEN not set. Simulating publish.")
            return {"status": "SUCCESS", "message": "Simulated publish to Telegram", "platform_id": "sim_123"}
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": content,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return {"status": "SUCCESS", "platform_response": response.json()}
        except Exception as e:
            logger.error(f"Failed to publish to Telegram: {e}")
            return {"status": "FAILED", "reason": str(e)}
