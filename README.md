# check_apache404
This Nagios plugin monitors the Apache server log file in search of State 404, receiving as arguments the full path of the log file, and the maximum values for warning and critical, these values are passed in pairs (50.100), to specify the value of records per IP address and the total respectively. By default the plugin audits all contents of the file, and can be parameterized the number of rows to be read using -n argument. Nagios signals with the warning or critical states, depending on the amount of records detected.
