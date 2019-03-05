"""
Author: Stan Slupecki
Operating Systems Scheduling HW

This program demonstrates how a round robin process scheduler affects
process throughput for a CPU

This program calculates two categories of values:
------------------
PER PROCESS VALUES
------------------
- Start Time: clock time when the process first arrives in ready queue
- End Time: clock time when process terminates
- Interarrival Time: Time between the start time of current process
    minus the start time of the previous process (if there is one)
    Interarrival Time = Current Start Time - Prev Start Time
- Initial Wait Time: amount of time process stays in wait queue before
- Total Wait Time: total time process was in wait queue
- Turnaround Time: time needed to execute a process
    Turnaround Time = Start time - end time
------------------
CUMULATIVE VALUES
------------------
- Average Service Time: time to finish all processes
    divided by # of processes
- Average Turnaround Time: average turnaround time over all processes
------------------
OTHER NOTES
------------------
This implementation of the round robin has the timer interrupt run
at fixed intervals. If the timer interrupt last fired at time N,
the next time it will fire will be time N+Q,
where Q is the quantum length

Further, if the CPU is executing a context switch,
the timer interrupt will not start a new context switch or queue
up more processes. It will continue with the current context switch
uninterrupted.
"""
from collections import deque
from cpu_tools import *
from log import *
"""
------------------
MASTER VARIABLES
------------------
Edit these values to change how the program runs
"""
# CPU clock time
CLOCK_TIME = 0
# context switch time
CONTEXT_SWITCH_TIME = 0
# lenght of round robin interval
QUANTUM_TIME = 15
# list of pre-made processes to feed into ready queue
PROCESSES = [Process(1, 75, 0),
             Process(2, 40, 10),
             Process(3, 25, 10),
             Process(4, 20, 80),
             Process(5, 45, 85)]


def main():
    """
    driver function that demonstrates the scheduling system
    """
    # create the Log
    log = Log()
    # create a local var to represent clocktime
    # based on global var
    clock_time = CLOCK_TIME
    # create the ready queue
    ready_queue = deque()

    # create process manager
    process_manager = ProcessManager(PROCESSES, ready_queue)
    # init with PROCESSES defined above and the ready queue

    # create the round robin scheduler
    scheduler = RoundRobin(QUANTUM_TIME)

    # create the CPU
    cpu = CPU(CONTEXT_SWITCH_TIME, clock_time)

    # on deck is a process that is awaiting for
    # a context switch to complete
    on_deck = None

    # add all processes to log
    # but make sure to sort them by their arrival time first
    for process in sorted(PROCESSES, key=lambda a: a.arrival_time):
        log.add_entry(process.id, process.arrival_time)

    # flag indicating whether there are still processes
    keep_processing = True
    while keep_processing:
        # 1. FEED PROCESSES
        # give the current time to process manager
        process_manager.feed_ready_queue(clock_time)
        # this will feed processes into the ready queue
        # at the appropriate time

        # 2. GIVE CPU NEW CLOCK TIME
        cpu.set_clock(clock_time)

        # 3. CLEAR ON_DECK IF PROCESSOR IS RUNNING
        if cpu.status == "running":
            on_deck = None
        # 4. CHECK IF A CONTEXT SWITCH IS APPROPRIATE
        # 4.1 IF THIS IS THE FIRST PROCESS AND A FULL CS
        #   ISN'T NEEDED
        if cpu.first_process:
            # directly pop processes into CPU
            # if a process is in the ready queue yet
            if ready_queue:
                cpu.switch_process(ready_queue.pop())
        # 4.2 IF THE PROCESSOR IS FREE
        elif cpu.status == "free":
            # if a process has terminated and the CPU
            # is free
            # and if there's a process available in the ready queue
            if ready_queue:
                on_deck = ready_queue.pop()
                # store in on_deck for bookkeeping
                cpu.switch_process(on_deck)
        # 4.3 IF THE ROUND ROBIN INTERRUPT HAS GONE OFF
        #   AND THE PROCESSOR ISN'T MID CS
        elif scheduler.switch_process(clock_time) and cpu.status != "cs":
            # switch due to timer interrupt
            # only if not already mid context switch
            # and if there's a process available in the ready queue
            if ready_queue:
                on_deck = ready_queue.pop()
                # store in on_deck for bookkeeping
                cpu.switch_process(on_deck)

        # 5. EXECUTE PROCESS
        if cpu.status == "running":
            # if the CPU is running, execute the process
            log.unset_initial_wait_flag(cpu.active_process.id)
            # tell the log to no longer track initial wait time
            # for this process
            finished_process_id = cpu.execute_process()
            # 5.1 IF THE PROCESS IS DONE EXECUTING
            if finished_process_id:
                # if the process is done do some bookkeeping
                log.set_end_time(finished_process_id, clock_time)
                # save this process's end time
                if ready_queue:
                    # first try to immediately load a new process
                    on_deck = ready_queue.pop()
                    # store in on_deck for bookkeeping
                    cpu.switch_process(on_deck)
                else:
                    # otherwise, mark the CPU as free
                    cpu.status = "free"


        # 6. RECOVER PROCESS FROM CPU AFTER CONTEXT SWITCH
        old_process = cpu.retrieve_previous_process()
        if old_process:
            ready_queue.appendleft(old_process)

        # 7. BOOKKEEPING
        # 7.1 INCREMENT READY QUEUE WAIT TIMES
        for process in ready_queue:
            log.increment_wait_time(process.id)
        # 7.2 INCREMENT ON DECK WAIT TIMES
        if(on_deck):
            log.increment_wait_time(on_deck.id)
        # 7.3 SIGNAL END OF DRIVER IF APPROPRIATE
        if not ready_queue and not PROCESSES and cpu.status == "free":
            keep_processing = False
            # note the final clock time in the log
            log.final_complete_time = clock_time
        # 7.4 INCREMENT CLOCKTIME
        clock_time += 1

    # print results
    log.printData()

main()

