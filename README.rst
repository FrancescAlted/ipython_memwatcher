ipython_memwatcher
==================

IPython tool to report memory usage deltas for every command you
type. If you are running out of RAM then use this tool to understand
what's happening. It also records the time spent running each command.

This tool helps you to figure out which commands use a lot of RAM and
take a long time to run, this is very useful if you're working with
large numpy matrices. In addition it reports the peak memory usage
whilst a command is running which might be higher (due to temporary
objects) than the final RAM usage. Built on @fabianp's
`memory_profiler`.

As a simple example - make 10,000,000 random numbers, report that it
costs 76MB of RAM and took 0.3 seconds to execute::

  In [1]: import numpy as np

  In [2]: from ipython_memwatcher import MemWatcher

  In [3]: mw = MemWatcher()

  In [4]: mw.start_watching_memory()
  In [4] used 0.0156 MiB RAM in 2.77s, peaked 0.00 MiB above current, total RAM usage 36.27 MiB

  In [5]: arr=np.random.uniform(size=1e7)
  In [5] used 76.3320 MiB RAM in 0.33s, peaked 0.00 MiB above current, total RAM usage 112.60 MiB

And if we also want to have access to the measurements, just call the
`measurements` property::

  In [6]: mw.measurements
  Out[6]: Measurements(memory_delta=76.33203125, time_delta=0.32660794258117676, memory_peak=0, memory_usage=112.59765625)
  In [6] used 0.0664 MiB RAM in 0.10s, peaked 0.00 MiB above current, total RAM usage 112.66 MiB

Works with Python 2.7 and 3.4 or higher, and with IPython 3.0 and up.

**Note**: This work is strongly based on
https://github.com/ianozsvald/ipython_memory_usage by Ian Ozsvald and
adds basically a handier object interface and a `.measurements` property
for getting access to the actualy memory values. In the future
`ipython_memwatcher` can merged back into `ipython_memory_usage`.

Example usage
=============

We can measure on every line how large array operations allocate and
deallocate memory::

  In [1]: import numpy as np

  In [2]: from ipython_memwatcher import MemWatcher

  In [3]: mw = MemWatcher()

  In [4]: mw.start_watching_memory()
  In [4] used 0.0156 MiB RAM in 5.24s, peaked 0.00 MiB above current, total RAM usage 36.20 MiB

  In [5]: a = np.ones(1e7)
  In [5] used 76.3320 MiB RAM in 0.13s, peaked 0.00 MiB above current, total RAM usage 112.53 MiB

  In [6]: b = np.ones(1e7)
  In [6] used 76.3203 MiB RAM in 0.12s, peaked 0.00 MiB above current, total RAM usage 188.85 MiB

  In [7]: b = a * b
  In [7] used 0.0859 MiB RAM in 0.14s, peaked 2.23 MiB above current, total RAM usage 188.93 MiB

  In [8]: mw.measurements
  Out[8]: Measurements(memory_delta=0.0859375, time_delta=0.1445159912109375, memory_peak=2.234375, memory_usage=188.93359375)
  In [8] used 0.0703 MiB RAM in 0.10s, peaked 0.00 MiB above current, total RAM usage 189.00 MiB

You can use `stop_watching_memory` to stop watching and printing
memory usage after each statement::

  In [9]: mw.stop_watching_memory()
  In [10]: b = a * b

  In [11]:

Important RAM usage note
========================

It is much easier to debug RAM situations with a fresh IPython
shell. The longer you use your current shell, the more objects remain
inside it and the more RAM the Operating System may have reserved. RAM
is returned to the OS slowly, so you can end up with a large process
with plenty of spare internal RAM (which will be allocated to your
large objects), so this tool (via memory_profiler) reports 0MB RAM
usage. If you get confused or don't trust the results, quit IPython
and start a fresh shell, then run the fewest commands you need to
understand how RAM is added to the process.

Requirements
============

 * `memory_profiler` https://github.com/fabianp/memory_profiler

Tested on
=========

 * IPython 3.2 with Python 2.7 on Linux 64bit (2015-07)
 * IPython 7.2 with Python 3.7 on Mac OSX 64bit (2019-09)
