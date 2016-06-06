#!/usr/bin/python

import sys
import os
import getopt
import string
import pprint
import yaml
import subprocess

cfg_yaml_obj = None

g_config_name = ""
g_case_name = ""

g_topdir = ""
g_commondir = ""
g_casedir = ""
g_rundir = ""

g_common_path_key = "${COMMON}"
g_case_path_key = "${CASE}"
g_run_path_key = "${RUN}"

def _load_yaml_config(config_name):
    yaml_file = file(config_name, 'r')
    yml_obj = yaml.load(yaml_file)
    return yml_obj

def _create_case_config():
    return {
        'pre-run': [],
        'run': [],
        'verify': []
    }

def _validate_args():
    if g_config_name == "":
        print "Error: config name is empty"
        return False

    if g_case_name == "":
        print "Error: case name is empty"
        return False

    if g_topdir == "":
        print "Error: topdir is empty"
        return False

    return True

def _parse_config(cfg_name):
    # 1. Load config
    cfg_yaml_obj = _load_yaml_config(cfg_name)

    # 2. Create formated case config object
    case_config = _create_case_config()

    # 2.1 convert 'pre-run' section
    pre_run_actions = cfg_yaml_obj['pre-run']
    if not isinstance(pre_run_actions, list): raise
    case_config['pre-run'] = pre_run_actions

    # 2.2 convert 'run' section
    run_actions = cfg_yaml_obj['run']
    if not isinstance(run_actions, list): raise
    case_config['run'] = run_actions

    # 2.3 convert 'verify' section
    verify_actions = cfg_yaml_obj['verify']
    if not isinstance(verify_actions, list): raise
    case_config['verify'] = verify_actions

    return case_config

def _execute_commands(case_config, tab):
    global g_common_path_key
    global g_case_path_key
    global g_run_path_key

    commands = case_config[tab]
    if commands == None or isinstance(commands, list) == False:
        print "Error: wrong tab(%s) which cannot be executed" % tab
        raise

    for action in commands:
        # replace macros
        action = str(action).replace(g_common_path_key, g_commondir)
        action = str(action).replace(g_case_path_key, g_casedir)
        action = str(action).replace(g_run_path_key, g_rundir)

        # execute command
        ret = subprocess.call(action, shell=True)
        if ret != 0:
            print "Error: command execute failed: %s" % action
            raise

def _execute_case_commands(case_config):
    _execute_commands(case_config, "pre-run")
    _execute_commands(case_config, "run")
    _execute_commands(case_config, "verify")

    return True

def _generate_report():
    return

def usage():
    print "usage:"
    print "  ft-executor.py -c $config -t $topdir -n $caseName"

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    try:
        # 1. parse the args
        opts, args = getopt.getopt(sys.argv[1:], 'c:t:n:')

        for op, value in opts:
            if op == "-c":
                g_config_name = value
            elif op == "-t":
                g_topdir = value
            elif op == "-n":
                g_case_name = value

        g_casedir = g_topdir + "/cases/" + g_case_name
        g_rundir = g_topdir + "/run/" + g_case_name
        g_commondir = g_topdir + "/common/"
        print "topdir: %s" % g_topdir
        print "commondir: %s" % g_commondir
        print "casedir: %s" % g_casedir
        print "rundir: %s" % g_rundir

        # 2. validate args
        if _validate_args() == False:
            print "Error: Parameters validation failed"
            usage
            raise

        # 3. parse the config
        ft_config = _parse_config(g_config_name)

        # 4. execute commands according to the config
        _execute_case_commands(ft_config)

        # 5. generate a report
        _generate_report()

    except Exception, e:
        print "Fatal: " + str(e)
        usage()
        raise