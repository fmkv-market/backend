import logging
import sys
import uuid
from typing import Any
import warnings

import structlog
from structlog.typing import EventDict, WrappedLogger

from logiro.schema import LogConfig


def setup_logger(config: LogConfig) -> None:
    if config.json_enabled is False:
        warnings.warn(
            "Do not use not a json_enabled in production runtime. "
            "This me be the reason, why outer logging collectors can't handle messages (logs).\n"
            "Use this parameter only in development, for convenient presentation of log in the console.",
            stacklevel=2,
        )

    _setup_structlog(json_format=config.json_enabled)
    _setup_logging(level=config.level, json_format=config.json_enabled)


def _setup_structlog(*, json_format: bool) -> None:
    processors = [
        *_build_default_processors(json_format=json_format),
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure_once(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def _setup_logging(level: str | int, *, json_format: bool) -> None:
    renderer_processor = structlog.processors.JSONRenderer() if json_format else structlog.dev.ConsoleRenderer()
    default_processors = _build_default_processors(json_format=json_format)

    logging_processors = [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        renderer_processor,
    ]

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=default_processors,
        processors=logging_processors,
    )

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.set_name("default")
    handler.setLevel(level)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def _additional_serialize(
    logger: WrappedLogger,
    name: str,
    event_dict: EventDict,
) -> EventDict:
    for key, value in event_dict.items():
        if isinstance(value, uuid.UUID):
            event_dict[key] = str(value)
    return event_dict


def _build_default_processors(*, json_format: bool) -> list[Any]:
    pr = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.ExtraAdder(),
        _additional_serialize,
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True),
        structlog.processors.dict_tracebacks,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.THREAD,
                structlog.processors.CallsiteParameter.THREAD_NAME,
                structlog.processors.CallsiteParameter.PROCESS,
                structlog.processors.CallsiteParameter.PROCESS_NAME,
            },
        ),
    ]
    if json_format:
        pr.insert(0, structlog.processors.format_exc_info)

    return pr
