#!/usr/bin/python

import re
import os

fd = open('/etc/crontab')
ignored_lines = 0
shell = path = mailto = ''
crons = list()

shell_pattern = re.compile('SHELL=["\']?((/[a-zA-Z]+)+)["\']?')
path_pattern = re.compile('PATH=["\']?(((/[a-zA-Z]+)+:?)+)["\']?')
mailto_pattern = re.compile('MAILTO=([a-zA-Z0-9\-_]+(@[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+)?)')
command_match = re.compile('(\#?)(((((([0-9]+,?)+)|\*|(\*/[0-9]+)))[ \t]+){5}([a-zA-Z0-9]+)[ \t]+(.+))')
comment_match = re.compile('(\#.+)')


class CronItem:
    pre_comment = cmd = moh = hod = dom = moy = dow = ''
    invalid = commented = False

    def __init__(self):
        pass


line = 0
invalid = 0
commented = 0
invalid_lines = 0

for x in fd:
    line += 1
    if len(x.strip()) > 0:
        match = shell_pattern.match(x)
        if match and len(match.groups()) > 0:
            shell = match.groups()[0]
            continue

        match = path_pattern.match(x)
        if match and len(match.groups()) > 0:
            path = match.groups()[0]
            continue

        match = mailto_pattern.match(x)
        if match and len(match.groups()) > 0:
            mailto = match.groups()[0]
            continue

        match = command_match.match(x)
        if match and len(match.groups()) > 0:
            item = CronItem()

            cmd = str(match.groups()[-1])
            es = os.system("echo '%s' | bash -n &> /dev/null" % cmd)

            if match.groups()[0]:
                item.commented = True
                commented += 1

            item.cmd = cmd
            crons.append(item)

            if es != 0:
                item.invalid = True
                invalid += 1
                print("lines %s contains invalid cron command" % line)
            continue

        match = comment_match.match(x)
        if match and len(match.groups()) > 0:
            match.groups()
            continue

        print("lines %s is invalid" % line)
        invalid_lines += 1

print("[SUMMARY] %s lines" % line)
print("[SUMMARY] %s total crons" % len(crons))
print("[SUMMARY] %s invalid lines " % invalid_lines)
print("[SUMMARY] %s invalid cron commands  " % invalid)
print("[SUMMARY] %s commented commands " % commented)
