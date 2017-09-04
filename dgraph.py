#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A wrapper script for distribution.

Distribution (https://github.com/philovivero/distribution) is a script for
creating ASCII graphical histograms in the terminal. dgraph.py is a wrapper
script for distribution and its intention is to make the graph creation process
easier and faster for some common use cases.

:copyright: (c) 2017 by miroslavvidovic.
:license: MIT, see LICENSE for more details.
"""

import subprocess
from subprocess import PIPE

import click


@click.group()
def cli():
    """Draw ascii graphs in the terminal."""
    pass


@click.command()
@click.argument('file', type=click.Path(exists=True))
def word_frequency(file):
    """
    Draw a word frequency graph from a file.

    Args:
        file (str): path to a file
    """
    print("Word frequency for:%s \n\n" % file)
    cat = subprocess.Popen(['cat', file], stdout=PIPE)
    xargs = subprocess.Popen(['xargs', '-0'], stdin=cat.stdout, stdout=PIPE)
    cat.stdout.close()
    distribution = subprocess.Popen(['distribution', '--tokenize=word',
                                     '--match=word', '--color', '--char=ba',
                                     '--size=large'], stdin=xargs.stdout)
    xargs.stdout.close()
    distribution.communicate()


@click.command()
@click.argument('directory', type=click.Path(exists=True))
def space_usage(directory):
    """
    Draw a space usage graph for a directory.

    Args:
        directory (str): path to a system directory
    """
    print("Space usage for:%s \n\n" % directory)
    du_space = subprocess.Popen(['du', '--max-depth=1', '--all', directory],
                                stdout=PIPE, stderr=subprocess.DEVNULL)
    # sed removs the last line (the total line)
    sed = subprocess.Popen(['sed', '$d'], stdin=du_space.stdout, stdout=PIPE)
    du_space.stdout.close()
    distribution = subprocess.Popen(['distribution', '-g', '-v',
                                     '--color', '--char=ba', '--size=large'],
                                    stdin=sed.stdout)
    sed.stdout.close()
    distribution.communicate()


@click.command()
@click.argument('path', type=click.Path(exists=True))
def commits(path):
    """
    Draw a number of commits graph by author for a git path.

    Args:
        path (str): path to a git repository
    """
    # Check for a valid git repository by running a git command rev-parse and
    # checking the error output
    repo = subprocess.Popen(['git', '-C', path, 'rev-parse'], stderr=PIPE)
    if repo.stderr.read():
        print("Not a valid git repository")
        exit()

    print("Commits for:%s \n\n" % path)
    gitlog = subprocess.Popen(['git', '-C', path, 'shortlog', '-s'],
                           stdout=PIPE)
    distribution = subprocess.Popen(['distribution', '--graph', 'vk',
                                     '--color', '--char=ba', '--size=large'],
                                    stdin=gitlog.stdout)
    gitlog.stdout.close()
    distribution.communicate()


cli.add_command(word_frequency)
cli.add_command(space_usage)
cli.add_command(commits)

if __name__ == '__main__':
    cli()
