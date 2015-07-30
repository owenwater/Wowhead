#!/usr/bin/python
# encoding: utf-8

def show(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.wf.send_feedback()
    return wrapper

