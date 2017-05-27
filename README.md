# check_apache404
Apache is one of the most popular open-source HTTP server, whose main function is to process among other requests the hyper-Text Transfer Protocol (HTTP). When responding, Apache associates each response a predefined state. These states specify the type of response to the request, and because they are relevant events, are logged in a log file. The 404 state is one of several states of this software, which in addition to indicating the inability of the server to meet the request for unavailability of content, may also indicate attempted access to unauthorized content, which may be evidence of an event susceptible to compromise the security.

This Nagios plugin monitors the Apache server log file in search of State 404, receiving as arguments the full path of the log file, and the maximum values for warning and critical, these values are passed in pairs (50.100), to specify the value of records per IP address and the total respectively. By default the plugin audits all contents of the file, and can be parameterized the number of rows to be read using -n argument. Nagios signals with the warning or critical states, depending on the amount of records detected.


Mandatory arguments: The following arguments must be specified whenever the module is executed:

-p or --path used to specify the path of the Apache log file.

-c or --critical used to specify the values from which to be considered critical situation, this argument receives two values, one for the general case, i.e. total number of errors encountered, and the other for the number of errors per IP address.

-w or --warning used to specify the values from which the script should consider the result as warning, the resemblance of the -c this argument is also twofold.

Optional arguments: The following arguments are optionally invoked, as required by the user:

-n or --number used to specify the number of rows to read in the log file.

-V or --version used to query the module version.

-A or --author used to query the author's data.

Command-Line Execution example:

./check_apache404.py -p /var/log/apache2/access.log -c 300,200 -w 200,150 -n 1000

