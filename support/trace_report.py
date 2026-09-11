import json
import zipfile
from html import escape
from pathlib import Path


def build_trace_summary_html(trace_zip_path: Path) -> str:
    """Parse a Playwright trace.zip and render a collapsible debugging summary."""
    events = _read_jsonl(trace_zip_path, "trace.trace")
    actions = _extract_actions(events)
    console_errors = [e for e in events if e.get("type") == "console" and e.get("messageType") == "error"]
    failed_requests = _extract_failed_requests(trace_zip_path)

    sections = [
        _render_failed_action(actions),
        _render_timeline(actions),
        _render_console_errors(console_errors),
        _render_failed_requests(failed_requests),
    ]
    body = "".join(section for section in sections if section)
    if not body:
        body = "<div style='padding:8px;color:#666;'>No actions, console errors, or failed requests recorded.</div>"

    summary_style = (
        "cursor:pointer;font-weight:bold;text-decoration:underline;font-size:15px;"
        "font-family:'Courier New',Courier,monospace;"
    )
    # <details> already renders its own native disclosure triangle before <summary>.
    # The expanded body is position:absolute so it floats over the row instead of
    # pushing the screenshot below it down when opened.
    return (
        '<details style="position:relative;margin:8px 0;">'
        f'<summary style="{summary_style}">🔍 Trace Summary</summary>'
        '<div style="position:absolute;z-index:10;top:100%;left:0;width:600px;max-width:90vw;'
        'max-height:300px;overflow-y:auto;background:#fff;border:1px solid #ccc;'
        f'box-shadow:0 2px 8px rgba(0,0,0,.15);padding:4px;">{body}</div></details>'
    )


def _read_jsonl(trace_zip_path: Path, member: str) -> list:
    """Read a JSONL member out of the trace zip. Returns [] if the member is missing."""
    with zipfile.ZipFile(trace_zip_path) as zf:
        if member not in zf.namelist():
            return []
        raw = zf.read(member).decode("utf-8", errors="replace")
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def _extract_actions(events: list) -> list:
    """Pair before/after events by callId into a single ordered action list."""
    by_call_id = {e["callId"]: e for e in events if e.get("type") == "before" and "callId" in e}
    actions = []
    for e in events:
        if e.get("type") != "after" or e.get("callId") not in by_call_id:
            continue
        before = by_call_id[e["callId"]]
        actions.append({
            "label": f'{before.get("class", "")}.{before.get("method", "")}',
            "target": _format_target(before.get("params", {})),
            "duration_ms": round(e.get("endTime", 0) - before.get("startTime", 0), 1),
            "error": _format_error(e.get("error"), e.get("result")),
        })
    return actions


def _format_target(params: dict) -> str:
    """Pull out the most relevant param (selector/url/expression) for a compact label."""
    for key in ("selector", "url", "expression", "key"):
        if params.get(key):
            return str(params[key])
    return ""


def _format_error(error, result) -> str:
    """error.message is often generic (e.g. "Expect failed"); the real diagnostic for
    expect()/locator actions lives in result.errorMessage and result.log instead."""
    if not error:
        return ""
    lines = []
    if isinstance(error, dict) and error.get("message"):
        lines.append(str(error["message"]))
    elif error:
        lines.append(str(error))
    if isinstance(result, dict):
        if result.get("errorMessage"):
            lines.append(str(result["errorMessage"]))
        for log_line in result.get("log") or []:
            lines.append(str(log_line))
    return "\n".join(lines)


def _extract_failed_requests(trace_zip_path: Path) -> list:
    events = _read_jsonl(trace_zip_path, "trace.network")
    failed = []
    for e in events:
        snapshot = e.get("snapshot", {})
        request = snapshot.get("request", {})
        status = snapshot.get("response", {}).get("status")
        if isinstance(status, int) and status >= 400:
            failed.append({"method": request.get("method", ""), "url": request.get("url", ""), "status": status})
    return failed


def _render_failed_action(actions: list) -> str:
    # Last errored action, not first: an earlier error may have been caught/retried by
    # the page object and isn't what actually failed the test.
    failed = next((a for a in reversed(actions) if a["error"]), None)
    if not failed:
        return ""
    target = escape(failed["target"])
    target_suffix = f" ({target})" if failed["target"] else ""
    return (
        '<div style="margin:8px 0;padding:8px;border-left:4px solid #bf0026;background:#fff4f4;">'
        '<strong style="color:#bf0026;">❌ Failed step:</strong> '
        f'{escape(failed["label"])}{target_suffix}'
        f'<pre style="margin-top:4px;color:#bf0026;white-space:pre-wrap;font-family:inherit;">{escape(failed["error"])}</pre>'
        '</div>'
    )


def _render_timeline(actions: list) -> str:
    if not actions:
        return ""
    rows = "".join(
        '<tr>'
        f'<td style="padding:2px 8px;">{"❌" if a["error"] else "✅"}</td>'
        f'<td style="padding:2px 8px;">{escape(a["label"])}</td>'
        f'<td style="padding:2px 8px;">{escape(a["target"])}</td>'
        f'<td style="padding:2px 8px;">{a["duration_ms"]} ms</td>'
        '</tr>'
        for a in actions
    )
    return (
        '<div style="margin:8px 0;"><strong>Action timeline:</strong>'
        '<table style="border-collapse:collapse;font-size:12px;">'
        f'{rows}</table></div>'
    )


def _render_console_errors(console_errors: list) -> str:
    if not console_errors:
        return ""
    items = "".join(
        f'<li>{escape(e.get("text", ""))} '
        f'<span style="color:#888;">({escape(e.get("location", {}).get("url", ""))})</span></li>'
        for e in console_errors
    )
    return f'<div style="margin:8px 0;"><strong>Console errors:</strong><ul style="margin:4px 0;">{items}</ul></div>'


def _render_failed_requests(failed_requests: list) -> str:
    if not failed_requests:
        return ""
    items = "".join(
        f'<li>{r["status"]} {escape(r["method"])} {escape(r["url"])}</li>'
        for r in failed_requests
    )
    return f'<div style="margin:8px 0;"><strong>Failed requests:</strong><ul style="margin:4px 0;">{items}</ul></div>'
