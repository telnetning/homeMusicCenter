#!/usr/bin/env python2
#coding=utf-8

try:
    from exception import Exception, Warning, StandardError
except ImportError:
    StandError = Exception

class ConnError(Exception):
    """Exception that connect to the sql error.
    """

class CreateError(Exception):
    """Exception raised by create database or table
    """

