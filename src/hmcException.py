#!/usr/bin/env python2
#coding=utf-8

try:
    from exception import Exception, Warning, StandardError
except importError:
    StandError = Exception

class ConnError(Error):
    """Exception that connect to the sql error.
    """

class CreatError(Error):
    """Exception raised by create database or table
    """

