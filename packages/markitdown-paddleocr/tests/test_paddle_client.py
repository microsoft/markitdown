"""Tests for PaddleClient."""

import json
import pytest
from unittest.mock import MagicMock, patch

from markitdown_paddleocr._paddle_client import PaddleClient, PaddleOcrError
from markitdown_paddleocr._config import PaddleOcrConfig


class TestPaddleClientInit:
    """Client initialization tests."""

    def test_init_with_token(self):
        """Init with explicit token."""
        client = PaddleClient(token="test-token")
        assert client.token == "test-token"

    @patch.dict("os.environ", {"BAIDU_PADDLE_TOKEN": "env-token"})
    def test_init_from_env(self):
        """Init from environment variable."""
        client = PaddleClient()
        assert client.token == "env-token"

    def test_init_with_config(self):
        """Init with PaddleOcrConfig."""
        config = PaddleOcrConfig(token="config-token", model="custom-model")
        client = PaddleClient(config=config)
        assert client.token == "config-token"
        assert client.config.model == "custom-model"


class TestPaddleClientSubmit:
    """Job submission tests."""

    def test_submit_local_file(self):
        """Submit local file via multipart upload."""
        client = PaddleClient(token="test-token")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"jobId": "job-123"}}

        with patch("requests.post", return_value=mock_response) as mock_post:
            job_id = client._submit(file_bytes=b"fake-image", filename="test.png")

        assert job_id == "job-123"
        # Verify multipart upload was used (files parameter)
        call_kwargs = mock_post.call_args
        assert "files" in call_kwargs.kwargs or len(call_kwargs.args) > 0

    def test_submit_url_mode(self):
        """Submit file URL via JSON."""
        client = PaddleClient(token="test-token")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"jobId": "job-456"}}

        with patch("requests.post", return_value=mock_response) as mock_post:
            job_id = client._submit(file_url="https://example.com/doc.pdf")

        assert job_id == "job-456"

    def test_submit_error(self):
        """Submit with API error."""
        client = PaddleClient(token="test-token")

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(PaddleOcrError, match="Submit failed"):
                client._submit(file_bytes=b"fake", filename="test.png")

    def test_submit_no_input(self):
        """Submit without file or URL raises error."""
        client = PaddleClient(token="test-token")
        with pytest.raises(PaddleOcrError, match="Either file_bytes or file_url"):
            client._submit()


class TestPaddleClientPoll:
    """Job polling tests."""

    def test_poll_done_immediately(self):
        """Job is done on first poll."""
        client = PaddleClient(token="test-token")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "state": "done",
                "resultUrl": {"jsonUrl": "https://result.url/data.jsonl"},
            }
        }

        with patch("requests.get", return_value=mock_response):
            result_url = client._poll("job-123")

        assert result_url == "https://result.url/data.jsonl"

    def test_poll_failed(self):
        """Job fails."""
        client = PaddleClient(token="test-token")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"state": "failed", "errorMsg": "Processing error"}
        }

        with patch("requests.get", return_value=mock_response):
            with pytest.raises(PaddleOcrError, match="Job failed"):
                client._poll("job-123")

    def test_poll_timeout(self):
        """Polling timeout."""
        config = PaddleOcrConfig(token="test-token", poll_interval=0.01, poll_timeout=0.05)
        client = PaddleClient(config=config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"state": "pending"}}

        with patch("requests.get", return_value=mock_response):
            with pytest.raises(PaddleOcrError, match="timed out"):
                client._poll("job-123")


class TestPaddleClientFetchMarkdown:
    """Result fetching tests."""

    def test_fetch_single_page(self):
        """Fetch single page result."""
        client = PaddleClient(token="test-token")

        jsonl_content = json.dumps({
            "result": {
                "layoutParsingResults": [
                    {"markdown": {"text": "# Title\n\nHello world"}}
                ]
            }
        })

        mock_response = MagicMock()
        mock_response.text = jsonl_content
        mock_response.raise_for_status = MagicMock()

        with patch("requests.get", return_value=mock_response):
            markdown = client._fetch_markdown("https://result.url/data.jsonl")

        assert "# Title" in markdown
        assert "Hello world" in markdown

    def test_fetch_multi_page(self):
        """Fetch multi-page result."""
        client = PaddleClient(token="test-token")

        page1 = json.dumps({
            "result": {
                "layoutParsingResults": [
                    {"markdown": {"text": "Page 1 content"}}
                ]
            }
        })
        page2 = json.dumps({
            "result": {
                "layoutParsingResults": [
                    {"markdown": {"text": "Page 2 content"}}
                ]
            }
        })
        jsonl_content = f"{page1}\n{page2}"

        mock_response = MagicMock()
        mock_response.text = jsonl_content
        mock_response.raise_for_status = MagicMock()

        with patch("requests.get", return_value=mock_response):
            markdown = client._fetch_markdown("https://result.url/data.jsonl")

        assert "Page 1 content" in markdown
        assert "Page 2 content" in markdown

    def test_fetch_empty_result(self):
        """Fetch empty result."""
        client = PaddleClient(token="test-token")

        mock_response = MagicMock()
        mock_response.text = ""
        mock_response.raise_for_status = MagicMock()

        with patch("requests.get", return_value=mock_response):
            markdown = client._fetch_markdown("https://result.url/data.jsonl")

        assert markdown == ""


class TestPaddleClientOcr:
    """Full OCR workflow tests."""

    def test_ocr_workflow(self):
        """Complete OCR workflow: submit → poll → fetch."""
        client = PaddleClient(token="test-token")

        # Mock submit
        submit_resp = MagicMock()
        submit_resp.status_code = 200
        submit_resp.json.return_value = {"data": {"jobId": "job-789"}}

        # Mock poll
        poll_resp = MagicMock()
        poll_resp.status_code = 200
        poll_resp.json.return_value = {
            "data": {
                "state": "done",
                "resultUrl": {"jsonUrl": "https://result.url/data.jsonl"},
            }
        }

        # Mock fetch
        jsonl_content = json.dumps({
            "result": {
                "layoutParsingResults": [
                    {"markdown": {"text": "# OCR Result\n\nExtracted text."}}
                ]
            }
        })
        fetch_resp = MagicMock()
        fetch_resp.text = jsonl_content
        fetch_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=submit_resp), \
             patch("requests.get", side_effect=[poll_resp, fetch_resp]):
            markdown = client.ocr(file_bytes=b"fake-image", filename="test.png")

        assert "# OCR Result" in markdown
        assert "Extracted text." in markdown
