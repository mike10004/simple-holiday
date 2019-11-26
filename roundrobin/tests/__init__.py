#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging

_logging_configured = False

if not _logging_configured:
    level = logging.__dict__[os.getenv('SIMPLE_HOLIDAY_TESTS_LOG_LEVEL', 'INFO')]
    logging.basicConfig(level=level)
    _logging_configured = True
