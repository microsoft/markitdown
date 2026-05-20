"""PaddleOCR API Client - handles job submission, polling, and result fetching."""

import json
import logging
import time
from typing import Optional

import requests

from ._config import PaddleOcrConfig

logger = logging.getLogger(__name__)


class PaddleOcrError(Exception):
    """PaddleOCR API error."""

    pass


class PaddleClient:
    """Client for PaddleOCR cloud API.

    Workflow: submit job → poll status → fetch JSONL result → extract markdown.
    """

    def __init__(self, config: Optional[PaddleOcrConfig] = None, **kwargs):
        if config is None:
            config = PaddleOcrConfig(**kwargs)
        self.config = config

        # Token from config or env
        self.token = config.token
        if not self.token:
            import os
            self.token = os.environ.get("BAIDU_PADDLE_TOKEN", "")

    def _headers(self) -> dict:
        """Build authorization headers."""
        return {"Authorization": f"bearer {self.token}"}

    def _optional_payload(self) -> dict:
        """Build optional payload flags."""
        return {
            "useDocOrientationClassify": self.config.use_doc_orientation_classify,
            "useDocUnwarping": self.config.use_doc_unwarping,
            "useChartRecognition": self.config.use_chart_recognition,
        }

    def ocr(
        self,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        file_url: Optional[str] = None,
    ) -> str:
        """Run OCR on a file or URL, return concatenated markdown.

        Args:
            file_bytes: File content bytes (for local file upload).
            filename: Filename for multipart upload (e.g. "page.png").
            file_url: File URL (for URL mode, alternative to file_bytes).

        Returns:
            Markdown text extracted from all pages.

        Raises:
            PaddleOcrError: On API errors or timeout.
        """
        # 1. Submit job
        job_id = self._submit(file_bytes=file_bytes, filename=filename, file_url=file_url)
        logger.info("Job submitted: %s", job_id)

        # 2. Poll until done
        result_url = self._poll(job_id)
        logger.info("Job completed, result URL obtained")

        # 3. Fetch and parse results
        return self._fetch_markdown(result_url)

    def _submit(
        self,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        file_url: Optional[str] = None,
    ) -> str:
        """Submit an OCR job, return job ID."""
        headers = self._headers()

        if file_url:
            # URL mode
            headers["Content-Type"] = "application/json"
            payload = {
                "fileUrl": file_url,
                "model": self.config.model,
                "optionalPayload": self._optional_payload(),
            }
            resp = requests.post(self.config.job_url, json=payload, headers=headers)
        elif file_bytes is not None:
            # Local file mode - multipart upload
            data = {
                "model": self.config.model,
                "optionalPayload": json.dumps(self._optional_payload()),
            }
            fname = filename or "document"
            files = {"file": (fname, file_bytes)}
            resp = requests.post(self.config.job_url, headers=headers, data=data, files=files)
        else:
            raise PaddleOcrError("Either file_bytes or file_url must be provided")

        if resp.status_code != 200:
            raise PaddleOcrError(f"Submit failed (HTTP {resp.status_code}): {resp.text}")

        result = resp.json()
        job_id = result.get("data", {}).get("jobId")
        if not job_id:
            raise PaddleOcrError(f"No jobId in response: {result}")

        return job_id

    def _poll(self, job_id: str) -> str:
        """Poll job status until done, return JSONL result URL."""
        headers = self._headers()
        url = f"{self.config.job_url}/{job_id}"
        start = time.time()

        while True:
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                raise PaddleOcrError(f"Poll failed (HTTP {resp.status_code}): {resp.text}")

            data = resp.json().get("data", {})
            state = data.get("state", "")

            if state == "done":
                result_url = data.get("resultUrl", {}).get("jsonUrl", "")
                if not result_url:
                    raise PaddleOcrError("Job done but no resultUrl in response")
                return result_url

            if state == "failed":
                error_msg = data.get("errorMsg", "Unknown error")
                raise PaddleOcrError(f"Job failed: {error_msg}")

            # Still pending or running
            if state == "running":
                progress = data.get("extractProgress", {})
                total = progress.get("totalPages", "?")
                extracted = progress.get("extractedPages", "?")
                logger.debug("Running: %s/%s pages", extracted, total)
            else:
                logger.debug("State: %s", state)

            # Check timeout
            elapsed = time.time() - start
            if elapsed > self.config.poll_timeout:
                raise PaddleOcrError(
                    f"Job polling timed out after {self.config.poll_timeout}s (state={state})"
                )

            time.sleep(self.config.poll_interval)

    def _fetch_markdown(self, jsonl_url: str) -> str:
        """Fetch JSONL result and extract markdown from all pages."""
        resp = requests.get(jsonl_url)
        resp.raise_for_status()

        markdown_parts = []
        lines = resp.text.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            try:
                page_data = json.loads(line)
            except json.JSONDecodeError:
                logger.warning("Skipping invalid JSONL line")
                continue

            result = page_data.get("result", {})
            layout_results = result.get("layoutParsingResults", [])

            for layout in layout_results:
                md_text = layout.get("markdown", {}).get("text", "")
                if md_text.strip():
                    markdown_parts.append(md_text.strip())

        return "\n\n".join(markdown_parts)
