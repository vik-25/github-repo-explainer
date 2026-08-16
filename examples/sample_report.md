# Overview

**Requests** is an HTTP library for Python (officially supporting Python 3.10+). Its main purpose is to make sending HTTP/1.1 requests simple, intuitive, and developer-friendly without needing to manually handle lower-level networking, query string construction, form encoding, or socket management.

The library is designed for Python developers who need to interact with web APIs and remote HTTP services. Key features include persistent session management, automatic connection pooling, browser-style TLS/SSL verification, cookie persistence, proxy routing, and automatic decompression/decoding of response payloads.

# Tech Stack

- **Python (3.10+)**: Core programming language.
- **urllib3**: The underlying HTTP transport engine powering connection pooling, keep-alive, and low-level socket execution.
- **charset_normalizer / chardet**: Character set detection libraries used to determine response encodings when reading textual HTTP response payloads.
- **idna**: Provides Internationalized Domain Names (IDN) support.
- **certifi**: Provides root CA certificates for default TLS/SSL certificate verification.
- **Setuptools & Pyproject.toml**: Package build system and project metadata configuration standard (PEP 517/518/621).
- **Ruff & Pyright**: Tools used for code linting, formatting, and strict static type checking.
- **Pytest & Tox**: Test automation frameworks for running unit and integration tests across target environments.
- **GitHub Actions**: Continuous Integration pipeline provider running automated workflows for testing, linting, typechecking, security scanning (`zizmor`, `codeql`), and publishing.

# Repository Structure

- `src/requests/`: Main package source code.
  - `api.py`: Entry points for functional API calls (`requests.get`, `requests.post`, etc.).
  - `sessions.py`: Implements stateful sessions, environment setting merging, and redirect loop handling.
  - `models.py`: Defines key HTTP data structures (`Request`, `PreparedRequest`, `Response`).
  - `adapters.py`: Transport adapters bridging Requests calls to `urllib3` connection pools.
  - `auth.py`, `cookies.py`, `structures.py`, `utils.py`: Supporting utilities for authentication mechanisms, cookie management, case-insensitive dictionaries, and helper functions.
- `tests/`: Unit and integration test suite, including a local test server implementation (`tests/testserver/`) and mock SSL/TLS certificate setups (`tests/certs/`).
- `docs/`: Sphinx-based project documentation containing user guides, API references, and contributor instructions.
- `.github/`: CI/CD workflow definitions (`workflows/`), issue templates, code ownership settings, and security policies.
- `ext/`: Static media assets and branding graphics.

# Key Files

### `src/requests/sessions.py`
- **What it does**: Implements the `Session` object and `SessionRedirectMixin`. It manages persistent headers, cookies, authentication settings, and proxy parameters across multiple requests, while handling HTTP redirect chains (`resolve_redirects`) and safely stripping credentials when cross-domain redirects occur (`should_strip_auth`).
- **Why a developer should read it**: It reveals the central orchestration layer of the library, showing how session-level defaults are merged with per-request arguments and dispatched through configured transport adapters.

### `src/requests/adapters.py`
- **What it does**: Defines `BaseAdapter` and `HTTPAdapter`, which serve as the interface between Requests and `urllib3`. It handles low-level HTTP/HTTPS connection pooling (`PoolManager`), proxy configuration (including SOCKS proxies via `SOCKSProxyManager`), SSL/TLS verification setup, and maps `urllib3` errors into Requests exceptions.
- **Why a developer should read it**: It explains how Requests encapsulates transport mechanics and decouples high-level HTTP semantics from low-level connection management and socket handling.

### `src/requests/models.py`
- **What it does**: Defines `Request`, `PreparedRequest`, and `Response`. `PreparedRequest` parses URLs, performs IDNA hostname encoding, constructs multipart/form-data bodies, and formats headers. `Response` manages content consumption, unicode decoding (`text`), JSON parsing (`json()`), streaming (`iter_content`), and HTTP status validation (`raise_for_status()`).
- **Why a developer should read it**: It details the lifecycle of an HTTP call from an unbaked `Request` into a byte-precise `PreparedRequest`, as well as how raw incoming HTTP response streams are converted into Python objects.

# Suggested Improvement

**Replace `assert` statements in runtime dependency version checks with explicit conditionals.**

In `src/requests/__init__.py`, the `check_compatibility` function uses `assert` statements to verify supported versions of `urllib3`, `chardet`, and `charset_normalizer` (e.g., `assert major >= 1`). 

Because Python strips `assert` statements when executed with optimizations enabled (`python -O` or `PYTHONOPTIMIZE=1`), these version compatibility checks will be bypassed entirely in optimized production environments. Replacing `assert` checks with explicit `if` conditions that raise `AssertionError` or `ValueError` ensures compatibility validation remains active regardless of Python execution flags.