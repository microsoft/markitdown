"""Metrics collection for the API server."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict
import time


@dataclass
class Metrics:
    """Metrics collection for monitoring."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_processing_time: float = 0
    request_times: Dict[str, float] = field(default_factory=dict)
    request_counts: Dict[str, int] = field(default_factory=dict)
    error_counts: Dict[str, int] = field(default_factory=dict)
    request_sizes: Dict[str, int] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.now)

    def track_request(
        self,
        endpoint: str,
        duration: float,
        success: bool,
        size: int = 0,
        error: str = None,
    ) -> None:
        """Track a request's metrics."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            if error:
                self.error_counts[error] = self.error_counts.get(error, 0) + 1

        self.total_processing_time += duration
        self.request_times[endpoint] = (
            self.request_times.get(endpoint, 0) + duration
        )
        self.request_counts[endpoint] = (
            self.request_counts.get(endpoint, 0) + 1
        )
        if size > 0:
            self.request_sizes[endpoint] = (
                self.request_sizes.get(endpoint, 0) + size
            )

    def get_stats(self) -> dict:
        """Get current statistics."""
        uptime = datetime.now() - self.start_time
        avg_processing_time = (
            self.total_processing_time / self.total_requests
            if self.total_requests > 0
            else 0
        )

        stats = {
            "uptime_seconds": uptime.total_seconds(),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": (
                self.successful_requests / self.total_requests
                if self.total_requests > 0
                else 0
            ),
            "average_processing_time": avg_processing_time,
            "requests_per_endpoint": self.request_counts,
            "average_time_per_endpoint": {
                endpoint: time / self.request_counts[endpoint]
                for endpoint, time in self.request_times.items()
            },
            "total_size_per_endpoint": self.request_sizes,
            "error_counts": self.error_counts,
        }

        return stats


# Global metrics instance
metrics = Metrics()