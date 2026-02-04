from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

from iloveimg import Iloveimg
from ilovepdf import Ilovepdf
from ilovepdf.element import Element
from ilovepdf.errors import ApiError, Error


COMMON_PARAMS = {
    "packaged_filename",
    "output_filename",
    "ignore_errors",
    "ignore_password",
    "try_pdf_repair",
}


def _load_env_file(path: str) -> Dict[str, str]:
    env: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("\ufeff")
            value = value.strip().strip('"').strip("'")
            env[key] = value
    return env


def _parse_param_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _collect_params(param_pairs: List[str], params_json: Optional[str]) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if params_json:
        with open(params_json, "r", encoding="utf-8") as handle:
            params.update(json.load(handle))
    for item in param_pairs:
        if "=" not in item:
            raise ValueError(f"Invalid --param format: '{item}' (expected key=value)")
        key, value = item.split("=", 1)
        params[key.strip()] = _parse_param_value(value.strip())
    return params


def _apply_params(task: Any, params: Dict[str, Any], strict: bool, quiet: bool) -> None:
    api_params = set(getattr(task, "API_PARAMS", []) or [])
    for key, value in params.items():
        if key == "elements" and hasattr(task, "add_element"):
            if isinstance(value, dict):
                value = [value]
            if not isinstance(value, list):
                raise ValueError("elements must be a list of objects")
            for item in value:
                if isinstance(item, Element):
                    task.add_element(item)
                    continue
                if not isinstance(item, dict):
                    raise ValueError("elements must be a list of objects")
                task.add_element(Element(item))
            continue
        if key in api_params or key in COMMON_PARAMS:
            setattr(task, key, value)
            continue
        if strict:
            raise ValueError(f"Unknown param '{key}'. Allowed: {sorted(api_params)}")
        setattr(task, key, value)
        if not quiet:
            print(f"[warn] Unknown param '{key}' was set dynamically.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ilovepdf",
        description="iLovePDF/iLoveIMG CLI",
    )
    parser.add_argument("--public-key", dest="public_key")
    parser.add_argument("--secret-key", dest="secret_key")
    parser.add_argument("--env-file", dest="env_file")
    parser.add_argument("--timeout", type=int, default=None, help="Request timeout in seconds")
    parser.add_argument("--long-timeout", type=int, default=None, help="Long job timeout in seconds")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--json", dest="json_output", action="store_true")
    parser.add_argument("--strict-params", action="store_true")

    subparsers = parser.add_subparsers(dest="module", required=True)

    for module_name in ("pdf", "img"):
        module_parser = subparsers.add_parser(module_name)
        module_parser.add_argument("tool", help="Tool name, e.g. compress, merge, resize")
        module_parser.add_argument("--file", action="append", default=[], help="Input file path")
        module_parser.add_argument("--url", action="append", default=[], help="Input file URL")
        module_parser.add_argument("--output-dir", default=".")
        module_parser.add_argument("--no-download", action="store_true")
        module_parser.add_argument("--param", action="append", default=[], help="Tool param key=value")
        module_parser.add_argument("--params-json", default=None, help="Path to JSON params")

    return parser


def _resolve_keys(args: argparse.Namespace) -> Dict[str, str]:
    env = dict(os.environ)
    if args.env_file:
        if not os.path.isfile(args.env_file):
            raise FileNotFoundError(f"ENV file not found: {args.env_file}")
        env.update(_load_env_file(args.env_file))

    public_key = args.public_key or env.get("ILOVEPDF_PUBLIC_KEY")
    secret_key = args.secret_key or env.get("ILOVEPDF_SECRET_KEY")
    if not public_key or not secret_key:
        raise ValueError("Missing API keys. Provide --public-key/--secret-key or set env vars.")
    return {"public_key": public_key, "secret_key": secret_key}


def _run_task(args: argparse.Namespace) -> int:
    keys = _resolve_keys(args)
    client = Ilovepdf(keys["public_key"], keys["secret_key"]) if args.module == "pdf" else Iloveimg(keys["public_key"], keys["secret_key"])

    task = client.new_task(args.tool)
    if args.timeout is not None:
        task.timeout = args.timeout
    if args.long_timeout is not None:
        task.long_timeout = args.long_timeout

    params = _collect_params(args.param, args.params_json)
    _apply_params(task, params, args.strict_params, args.quiet)

    if not args.file and not args.url:
        raise ValueError("No input provided. Use --file or --url.")

    for filepath in args.file:
        task.add_file(filepath)
    for url in args.url:
        task.add_file_from_url(url)

    if not args.quiet and not args.json_output:
        print(f"[info] Executing {args.module}:{args.tool} with {len(task.files)} file(s)")

    start = time.time()
    result = task.execute()
    elapsed = time.time() - start

    output_path = None
    if not args.no_download:
        task.download(args.output_dir, create_directory=True)
        output_path = os.path.join(args.output_dir, task.download_info.output_filename or "")

    if args.json_output:
        payload = {
            "module": args.module,
            "tool": args.tool,
            "task_id": task.task_id,
            "elapsed_sec": round(elapsed, 3),
            "output_filename": task.download_info.output_filename,
            "output_path": output_path,
            "result": getattr(result, "body", None),
        }
        print(json.dumps(payload, ensure_ascii=False))
    elif not args.quiet:
        print(f"[done] elapsed={elapsed:.2f}s output={output_path or 'n/a'}")
    return 0


def _reorder_global_args(argv: List[str]) -> List[str]:
    opts_with_value = {
        "--public-key",
        "--secret-key",
        "--env-file",
        "--timeout",
        "--long-timeout",
    }
    flags = {
        "--quiet",
        "--json",
        "--strict-params",
    }
    global_args: List[str] = []
    rest: List[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in opts_with_value:
            if i + 1 < len(argv):
                global_args.extend([arg, argv[i + 1]])
                i += 2
                continue
        if any(arg.startswith(opt + "=") for opt in opts_with_value):
            global_args.append(arg)
            i += 1
            continue
        if arg in flags:
            global_args.append(arg)
            i += 1
            continue
        rest.append(arg)
        i += 1
    return global_args + rest


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    if argv is None:
        argv = sys.argv[1:]
    argv = _reorder_global_args(argv)
    args = parser.parse_args(argv)
    try:
        return _run_task(args)
    except (ApiError, Error, ValueError, FileNotFoundError) as exc:
        if args.json_output:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        else:
            print(f"[error] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
