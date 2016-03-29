# Text Parser

A generally useful little tool for extracting info from log files or command
line tools.

The tool will detect the following field separators:
  - space (one or many)
, - comma (ideal for CSV files)
	 - tabs

The tool automatically strips whitespace from the beginning and end of
recovered data. If you don't want this behaviour, specify --raw on the command
line, or, when using Python, .raw() to an instantiated parser and the raw=True
kwarg when initialising the parser.

## Example 1
```bash
ps aux | tp
```

## Example 2
```bash
cat access_log | tp --format '%{ip} - - [%{date_time}] "%{request}" %{status} %{bytes} "%{referrer}" "%{user_agent}' --print "%{request}"
```

## Example 3
```python
import TextParser

tp = TextParser()

 # Parse a heading line and detect separators / field widths
tp.learn(file.readline())

tp.fields() -> ('cmd', 'ppid', 'pid', 'prio', ...)

tp.reap|return|yeild|recover|harvest(('pid', 'command'), file.readline())
-> {'pid': 2505, 'command': 'python'}

tp.reap|return|yeild|recover|harvest(('pid', 'command'), file.readlines())
-> [{'pid': 2505, 'command': 'python'}, {'pid': 2506, 'command': 'grep'}]

tp.op_format('%{pid} %{time} %{user} any other text')
-> '1 0:06 root any other text'
```

## Example 4
```python
tp.ip_format('%{ip} - - [%{date_time}] "%{request}" %{status} %{bytes} "%{referrer}" "%{user_agent}'

tp.parse(data)
```
