#!/usr/bin/env python2
#coding=utf-8

try:
    from exception import Exception, Warning, StandardError
except ImportError:
    StandardError = Exception

class ConnSqlError(StandardError):
    """Exception that connect to the sql error.
    """

class CreateTableError(StandardError):
    """Exception raised by create database or table
    """

