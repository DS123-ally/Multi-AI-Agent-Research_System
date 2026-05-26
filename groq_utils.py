import re
import time


def is_rate_limit_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "rate_limit" in msg or "429" in msg or "rate limit" in msg


def parse_retry_seconds(message: str) -> float | None:
    match = re.search(r"try again in ([\d.]+)s", message, re.IGNORECASE)
    if match:
        return float(match.group(1)) + 0.5
    return None


def invoke_with_retry(callable_fn, *, max_retries: int = 6):
    """Retry Groq calls when TPM/rate limits are hit."""
    last_exc = None
    for attempt in range(max_retries):
        try:
            return callable_fn()
        except Exception as exc:
            last_exc = exc
            if not is_rate_limit_error(exc) or attempt == max_retries - 1:
                raise
            wait = parse_retry_seconds(str(exc)) or min(3 * (2**attempt), 60)
            time.sleep(wait)
    raise last_exc

def stream_with_retry(callable_fn, *, max_retries: int = 6):
    """Retry Groq streams when TPM/rate limits are hit, buffering the first chunk."""
    last_exc = None
    for attempt in range(max_retries):
        try:
            stream = callable_fn()
            # Try to get the first chunk to catch immediate rate limits
            iterator = iter(stream)
            first_chunk = next(iterator)
            
            # If we succeed, yield the first chunk and then the rest of the stream
            yield first_chunk
            yield from iterator
            return # Exit generator after successful stream
            
        except StopIteration:
            return # Stream was empty
        except Exception as exc:
            last_exc = exc
            if not is_rate_limit_error(exc) or attempt == max_retries - 1:
                raise
            wait = parse_retry_seconds(str(exc)) or min(3 * (2**attempt), 60)
            time.sleep(wait)
            
    raise last_exc
