#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Profile mem usage envelope of IPython commands and report interactively"""
from __future__ import division  # 1/2 == 0.5, as in Py3
from __future__ import absolute_import  # avoid hiding global modules with locals
from __future__ import print_function  # force use of print("hello")
from __future__ import unicode_literals  # force unadorned strings "" to be unicode without prepending u""
import time
import memory_profiler
from collections import namedtuple
import threading
from IPython import get_ipython

__version__ = "0.2.5"


class MemWatcher(object):

    def __init__(self):
        # keep a global accounting for the last known memory usage
        # which is the reference point for the memory delta calculation
        self.previous_call_memory_usage = memory_profiler.memory_usage()[0]
        self.t1 = time.time() # will be set to current time later
        self.keep_watching = True
        self.peak_memory_usage = -1
        self.peaked_memory_usage = -1
        self.memory_delta = 0
        self.time_delta = 0
        self.watching_memory = True
        self.ip = get_ipython()
        self.input_cells = self.ip.user_ns['In']
        self._measurements = namedtuple(
            'Measurements',
            ['memory_delta', 'time_delta', 'memory_peak', 'memory_usage'],
            )

    @property
    def measurements(self):
        return self._measurements(
            self.memory_delta, self.time_delta,
            self.peaked_memory_usage, self.previous_call_memory_usage)

    def start_watching_memory(self):
        """Register memory profiling tools to IPython instance."""

        # Just in case start is called more than once, stop watching. Hence unregister events.
        self.stop_watching_memory()

        self.watching_memory = True
        self.ip.events.register("post_run_cell", self.watch_memory)
        self.ip.events.register("pre_run_cell", self.pre_run_cell)

    def stop_watching_memory(self):
        """Unregister memory profiling tools from IPython instance."""
        self.watching_memory = False
        try:
            self.ip.events.unregister("post_run_cell", self.watch_memory)
        except ValueError:
            pass
        try:
            self.ip.events.unregister("pre_run_cell", self.pre_run_cell)
        except ValueError:
            pass

    def watch_memory(self):
        if not self.watching_memory:
            return
        # calculate time delta using global t1 (from the pre-run
        # event) and current time
        self.time_delta = time.time() - self.t1
        new_memory_usage = memory_profiler.memory_usage()[0]
        self.memory_delta = new_memory_usage - self.previous_call_memory_usage
        self.keep_watching = False
        self.peaked_memory_usage = max(0, self.peak_memory_usage - new_memory_usage)
        num_commands = len(self.input_cells) - 1
        cmd = "In [{}]".format(num_commands)
        # convert the results into a pretty string
        output_template = ("{cmd} used {memory_delta:0.3f} MiB RAM in "
                           "{time_delta:0.3f}s, peaked {peaked_memory_usage:0.3f} "
                           "MiB above current, total RAM usage "
                           "{memory_usage:0.3f} MiB")
        output = output_template.format(
            time_delta=self.time_delta,
            cmd=cmd,
            memory_delta=self.memory_delta,
            peaked_memory_usage=self.peaked_memory_usage,
            memory_usage=new_memory_usage)
        print(str(output))
        self.previous_call_memory_usage = new_memory_usage


    def during_execution_memory_sampler(self):
        import time
        import memory_profiler
        self.peak_memory_usage = -1
        self.keep_watching = True

        n = 0
        WAIT_BETWEEN_SAMPLES_SECS = 0.001
        MAX_ITERATIONS = 60.0 / WAIT_BETWEEN_SAMPLES_SECS
        while True:
            mem_usage = memory_profiler.memory_usage()[0]
            self.peak_memory_usage = max(mem_usage, self.peak_memory_usage)
            time.sleep(WAIT_BETWEEN_SAMPLES_SECS)
            if not self.keep_watching or n > MAX_ITERATIONS:
                # exit if we've been told our command has finished or
                # if it has run for more than a sane amount of time
                # (e.g. maybe something crashed and we don't want this
                # to carry on running)
                if n > MAX_ITERATIONS:
                    print("{} SOMETHING WEIRD HAPPENED AND THIS RAN FOR TOO LONG, THIS THREAD IS KILLING ITSELF".format(__file__))
                break
            n += 1


    def pre_run_cell(self):
        """Capture current time before we execute the current command"""
        # start a thread that samples RAM usage until the current
        # command finishes
        ipython_memory_usage_thread = threading.Thread(
            target=self.during_execution_memory_sampler)
        ipython_memory_usage_thread.daemon = True
        ipython_memory_usage_thread.start()
        self.t1 = time.time()
