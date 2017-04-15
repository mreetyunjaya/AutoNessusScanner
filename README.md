# AutoNessusScanner

### Demo Video
<a href='https://youtu.be/3eAhhMZWHXY'>Auto Nessus Scanner Demo</a>

### Overview
[Nessus](https://www.tenable.com/products/nessus-vulnerability-scanner) is a great vulnerability assessment tool that provides flexibility to choose from a variety of different flavors of scans. It also provides a very comprehensive scan report at the end of the scan which can be used further in many ways by automated intrusion detection systems or even human analysts.

This program lets you configure the list of IP addresses that you need to carry out the vulnerability assessment for, and provides a menu driven command line tool to:

1. Create a new basic Nessus scan
2. List all scans
3. Perform a scan
4. Exit program

The code is written in Python 2.7 and works as a BASH command line tool.


### Dependencies
1. [Selenium Web Browser Automation](http://www.seleniumhq.org/)
  * `pip install selenium`
2. [Requests module for HTTP](https://pypi.python.org/pypi/requests)
  * `pip install requests`
3. [Python 2.7 json module](https://docs.python.org/2/library/json.html)
  * `inbuilt module in Python 2.7`

### Configuration
The `NessusScanIPs.txt` file needs to contain a list of IP addresses of machines that need to be scanned for vulnerabilities. Each IP address needs to be specified on a new line in the text file.

Next, simply run the `autonessus.py` file from command line:
 `python autonessus.py`
