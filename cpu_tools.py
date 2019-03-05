# various classes used to model CPU and related concepts
class Process:
    """
    Process Class
    This represents a simple process
    Here, the class holds an id, service time,
    and arrival time
    """
    def __init__(self, id, service_time, arrival_time):
        self.id = id
        self.service_time = service_time
        self.arrival_time = arrival_time

    def execute(self):
        """"
        default execution instructions are to decrement
        the service time
        """
        self.service_time -= 1

    def get_state(self):
        """"
        returns process state info
        :return:
        the state of the process as a string
            "running" if running
            "terminated" if not
        """
        if(self.service_time):
            return "running"
        elif self.service_time == 0:
            return "terminated"


class RoundRobin:
    def __init__(self, quantum=15):
        """
        The constructor for the Round Robin scheduler
        :param quantum:
        The time quantum for the timer interrupt
        """
        self.quantum = quantum

    def switch_process(self, clock_time):
        """
        This computes the time to fire the timer interrupt
        :param clock_time:
        the current clock tum
        :return:
        True if it's time to switch processes
        False otherwise
        """
        if clock_time != 0 and (clock_time % self.quantum == 0):
            # this will not fire at t=0 which could complicate
            #   running the first process
            return True
        return False

class CPU:
    """
    Represents a CPU
    cs is the context switch speed
        that is, how fast the CPU switches processes
    clock_time is clock time
        the amount of time the CPU has been actively
        processing something
    """
    def __init__(self, cs, clock_time):
        """
        Constructor for the CPU class
        :param cs:
        This is how long a context switch will take
        :param clock_time:
        The starting clock time
        """
        self.cs = cs
        self.clock_time = clock_time
        self.active_process = None

        # this is used to automatically run the first
        # process w/o doing a full context switch
        self.first_process = True

        # these values are used during a context switch
        # the time of the initial context switch call
        self.cs_start_time = None
        # flag for cpu state
        # "free", "running", "cs"
        #   free: the CPU has no active process
        #       and will accept a new one
        #   running: the CPU has an active process
        #       but will still respond to interrupts
        #   cs: the CPU is mid context switch and
        #       won't respond to interrupts
        self.status = "free"

        # this holds the previous process after a context
        #   switch so that it may be retrieved
        self.old_process = None

    def set_clock(self, clock_time):
        """
        feed the CPU the current clock time
        also unblock CPU after context switch if needed
        :param clock_time:
        the current clock time
        """
        self.clock_time = clock_time

        # set CPU to running if a context switch has been completed
        if self.status == "cs" and self.clock_time >= (self.cs + self.cs_start_time):
            self.status = "running"

    def execute_process(self):
        """
        Executes a process
        :return:
        A completed process id if it has been terminated
        Or None otherwise
        """
        if self.status == "running":
            self.active_process.execute()

            state = self.active_process.get_state()
            # if the process is done...
            if state == "terminated":
                # store the old process for bookkeeping
                old_process = self.active_process
                # set the CPU status to "free"
                self.status = "free"
                # remove the active process
                self.active_process = None
                # return the old process's id
                return old_process.id
            else:
                return None
        else:
            return None

    def switch_process(self, new_process):
        """
        Start a context switch
        :param new_process:
        The process to pass in
        """
        if self.first_process:
            # set up first process immediately
            self.active_process = new_process
            # start CPU in running
            self.status = "running"
            # unset first process flag
            self.first_process = False
        elif self.status != "cs":
            # only start if not currently performing context switch
            # set status to cs
            self.status = "cs"
            # set the cs start time as the current time
            self.cs_start_time = self.clock_time
            # store the old process
            self.old_process = self.active_process
            # store the new process
            self.active_process = new_process

    def retrieve_previous_process(self):
        """
        Used to retrieve the old process after a context switch
        if one has been performed and the process is now
        available
        :return:
        The old process if available
        Return None otherwise
        """
        if self.status == "running" and self.old_process:
            previous_process = self.old_process
            self.old_process = None
            return previous_process
        else:
            return None

class ProcessManager:
    def __init__(self, processes, ready_queue):
        """
        This manages the flow of processes to the ready queue
        :param processes:
        A list of processes
        :param ready_queue:
        A deque that represents the ready queue
        """
        self.processes = processes
        self.ready_queue = ready_queue

    def feed_ready_queue(self, clock_time):
        """
        Feed clock time in, and if it matches a process
        arrival time, feed it into the ready queue
        :param clock_time:
        The current clock time
        """
        results = []
        for process in self.processes:
            # check for all processes with arrival
            # time equal to process time

            if process.arrival_time == clock_time:
                # temporarily store the found processes in results
                results.append(process)

        # next, add the results to the ready queue
        # and remove them from the process list
        for process in results:
            self.ready_queue.appendleft(process)
            self.processes.remove(process)
