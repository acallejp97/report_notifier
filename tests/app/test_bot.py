import asyncio
import unittest
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from bot import ester
from bot import parking
from bot import start


class TestBotCommands(unittest.TestCase):
    @patch("bot.subprocess.run")
    def test_parking_command(self, mock_subprocess):
        """Test parking command sends message and runs subprocess"""
        mock_update = AsyncMock()
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        mock_context.args = []

        asyncio.run(parking(mock_update, mock_context))

        mock_update.message.reply_text.assert_called_once()
        mock_subprocess.assert_called_once_with(["python", "main.py", "parking"])

    @patch("bot.subprocess.run")
    def test_ester_command(self, mock_subprocess):
        """Test ester command sends message and runs subprocess"""
        mock_update = AsyncMock()
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        mock_context.args = []

        asyncio.run(ester(mock_update, mock_context))

        mock_update.message.reply_text.assert_called_once()
        mock_subprocess.assert_called_once_with(["python", "main.py", "ester"])

    def test_start_command(self):
        """Test start command sends welcome message"""
        mock_update = AsyncMock()
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()

        asyncio.run(start(mock_update, mock_context))

        mock_update.message.reply_text.assert_called_once_with("Bot iniciado correctamente")

    @patch("bot.subprocess.run")
    def test_parking_command_message_content(self, mock_subprocess):
        """Test parking command sends correct message"""
        mock_update = AsyncMock()
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        mock_context.args = []

        asyncio.run(parking(mock_update, mock_context))

        call_args = mock_update.message.reply_text.call_args[0][0]
        self.assertIn("parking", call_args.lower())

    @patch("bot.subprocess.run")
    def test_ester_command_message_content(self, mock_subprocess):
        """Test ester command sends correct message"""
        mock_update = AsyncMock()
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        mock_context.args = []

        asyncio.run(ester(mock_update, mock_context))

        call_args = mock_update.message.reply_text.call_args[0][0]
        self.assertIn("€STER", call_args)

    @patch("bot.subprocess.run")
    def test_parking_command_with_args(self, mock_subprocess):
        """Test parking command handles args correctly"""
        mock_update = AsyncMock()
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        mock_context.args = ["some_arg"]

        asyncio.run(parking(mock_update, mock_context))

        # Should still work even with args
        mock_update.message.reply_text.assert_called_once()

    @patch("bot.get_bot_token")
    @patch("bot.Application")
    def test_main_function_initializes_bot(self, mock_app_class, mock_get_token):
        """Test main function initializes bot application"""
        mock_get_token.return_value = "test_token_123"

        mock_builder = MagicMock()
        mock_app = MagicMock()

        # Setup the builder chain
        mock_builder.token.return_value = mock_builder
        mock_builder.build.return_value = mock_app
        mock_app_class.builder.return_value = mock_builder

        # Mock run_polling to prevent actual polling
        mock_app.run_polling = MagicMock()

        from bot import main

        # Call main and catch the run_polling
        with patch("bot.Application.builder", return_value=mock_builder):
            try:
                main()
            except Exception:
                pass

        # Verify token was retrieved
        mock_get_token.assert_called_once()

        # Verify builder was called with token
        mock_builder.token.assert_called_once_with("test_token_123")


if __name__ == "__main__":
    unittest.main()
