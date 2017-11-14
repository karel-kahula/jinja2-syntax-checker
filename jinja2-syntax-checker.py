#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jinja2
import os
import glob
import codecs
import argparse

from ConfigParser import RawConfigParser as ConfigParser


def check_templates(template_dirs, jinja2_env_extensions, file_encoding):
    result = 0
    errors = []
    jinja2_env = jinja2.Environment(
        extensions=jinja2_env_extensions)

    for td in template_dirs:
        for file in glob.glob(os.path.join(td, '*.jinja2')):
            print 'Scanning', file
            try:
                with codecs.open(file, 'r', file_encoding) as t:
                        jinja2_env.parse(t.read())
            except jinja2.exceptions.TemplateSyntaxError as e:
                result = 1
                errors.append((file, e.lineno, e.message))
            except UnicodeDecodeError as e:
                result = 1
                errors.append((file, None, str(e)))

    print ''
    if errors:
        print 'ERRORS FOUND:\n============='
        for file, ln, msg in errors:
            print 'Syntax error {file} @{ln}:\n\t{msg}'.format(
                file=file, ln=ln, msg=msg)
    else:
        print 'ALL OK!'

    return result


def get_settings(sparser):
    import re
    split_pattern = r'[^,;\s]+'

    settings = {}
    settings['encoding'] = sparser.get('parser', 'encoding')
    settings['directories'] = re.findall(
        split_pattern, sparser.get('parser', 'directories'))
    settings['jinja2_extensions'] = re.findall(
        split_pattern, sparser.get('parser', 'jinja2_extensions'))
    return settings


def main():
    parser = argparse.ArgumentParser(
        'Scans provided directories for jinja2 telmpates and parses the found '
        'templates for errors.')
    parser.add_argument(
        'settings', type=argparse.FileType('r'), help='Settings file')
    args = parser.parse_args()
    sparser = ConfigParser()
    sparser.readfp(args.settings)
    settings = get_settings(sparser)

    exit(
        check_templates(
            settings['directories'], settings['jinja2_extensions'],
            settings['encoding']))


if __name__ == '__main__':
    main()
