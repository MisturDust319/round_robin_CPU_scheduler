# Class for logging CPU info

class Log:
    """
    Book-Keeping class
    holds all data needed to display final results
    """
    class Entry:

        def __init__(self, pid, clock_time, last_entry=None):
            """
            Constructor for Log's embedded class, Entry
            This class stores data for individual processes
            :param pid:
            The process id and identifier for the log entry
            :param clock_time:
            The process' arrival time
            :param last_entry:
            Holds the previous entry of the log
            This stores the entries as a linked list
            """
            # the id of the process this entry tracks data for
            self.pid = pid
            # the start time is the initial clock time
            self.start_time = clock_time
            # this helps calculate initial wait vs. total wait
            self.calculate_initial_wait = True
            # log entries are implemented as a linked list
            #   this makes it easier to calculate interarrival time
            self.last_entry = last_entry
            # the time when the last process has been terminated
            self.final_complete_time = 0

            # when the process completed
            self.end_time = 0
            # time between two processes arrivals
            self.interarrival_time = 0
            # time between entry into into ready queue and first
            # execution
            self.initial_wait = 0
            # total time in wait queue
            self.total_wait = 0
            # time between arrival and execution
            self.turnaround_time = 0

        def printData(self):
            # calculate interarrival time
            #   AND recursively print previous entries
            if (self.last_entry):
                self.last_entry.printData()
                self.interarrival_time = self.start_time - self.last_entry.start_time

            # Calculate turnaround time
            self.turnaround_time = self.end_time - self.start_time

            # print individual output
            print("# Process Num: " + str(self.pid))
            print("# Start Time: " + str(self.start_time) + " End Time: " + str(self.end_time))
            print("# Interarrival Time: " + str(self.interarrival_time))
            print("# Initial Wait: " + str(self.initial_wait) + " Total Wait: " + str(self.total_wait))
            print("# Turnaround Time: " + str(self.turnaround_time))
            print("########################################################################")
    def __init__(self):
        """
        Constructor for Log
        Log will log data for you
        """
        # init Log with 0 entries
        self.entries = None
        self.number_of_entries = 0

    def add_entry(self, pid, clock_time):
        """
        create a new log entry
        :param pid:
        the new entry's id
        :param clock_time:
        the start time for this entry
        :return:
        """
        # create a new entry with entries as the previous entry
        new_entry = self.Entry(pid, clock_time, self.entries)
        # then set the new entry as the new value for entry
        self.entries = new_entry
        # then increment the number of entries
        self.number_of_entries += 1

    def modify_entry(self, entry_number, value, callback):
        """
        Helper function that modifies an entry based using callback
        :param entry_number:
        the entry to modify
        :param value:
        a value to use in callback
        :param callback:
        the callback function to use to modify entry
        :return:
        True if able to call the callback
        False otherwise
        """
        def recursive_search(entry, entry_number, value, callback):
            if(entry and entry.pid == entry_number):
                # If the proper entry has been found,
                # call the callback on it
                callback(entry, value)
                return True
            elif(entry and entry.last_entry):
                # otherwise, try again with the last entry
                # if it exists
                recursive_search(entry.last_entry, entry_number, value, callback)
            else:
                return False
        return recursive_search(self.entries, entry_number, value, callback)

    def check_for_entry(self, entry_number):
        """
        Checks for an entry with pid==entry_number
        :param entry_number:
        the process number to look for
        :return:
        True if found,
        False otherwise
        """
        return self.modify_entry(entry_number, None, lambda a, b: True)

    def increment_wait_time(self, entry_number):
        """
        Increments wait time for an entry in the log
        :param entry_number:
        The PID for the entry to modify
        :return:
        True if successful
        False otherwise
        """
        def increment_wait(entry, dummy):
            # this always increments total wait
            entry.total_wait += 1
            if entry.calculate_initial_wait:
                # but only calculates initial wait as needed
                entry.initial_wait += 1
            else:
                #print("Entry w/o initial wait flag: " + str(entry.pid))
                pass
        return self.modify_entry(entry_number, None, increment_wait)

    def set_end_time(self, entry_number, value):
        """
        Sets the end time of an entry
        :param entry_number:
        The id of the entry to modify
        :param value:
        The end time of the process
        """
        def mod_end_time(entry, value):
            entry.end_time = value
        self.modify_entry(entry_number, value, mod_end_time)

    def unset_initial_wait_flag(self, entry_number):
        """
        Tells the log to stop tracking the initial wait time
        for a particular process
        :param entry_number:
        the process id you wish to modify
        """
        def unset_flag(entry, dummy):
            entry.calculate_initial_wait = False
        self.modify_entry(entry_number, None, unset_flag)

    def printData(self):
        """
        Prints the data stored in the log
        """
        # create a nice little heading
        print("########################################################################")
        # PRINT INDIVIDUAL LOG ENTRY DATA
        self.entries.printData()

        # PRINT CUMULATIVE RESULTS
        def get_total_turnaround_time(entry):
            if(entry.last_entry):
                # if there's a previous log entry
                # recursively add the previous entry's turnaround
                return entry.turnaround_time + get_total_turnaround_time(entry.last_entry)
            else:
                # otherwise return the entry's turnaround time
                return entry.turnaround_time

        average_turnaround_time = get_total_turnaround_time(self.entries)/self.number_of_entries
        # avg service time: time to finish last process / num processes
        average_service_time = self.final_complete_time/self.number_of_entries
        print("########################################################################")
        print("# Average Turnaround Time: " + str(average_turnaround_time))
        print("# Average Service Time: " + str(average_service_time))
        print("########################################################################")

