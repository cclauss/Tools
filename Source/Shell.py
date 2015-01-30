# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 19:44:38 2014

@author: Misha
"""

_DEBUG = False


class ParserError(Exception):
    pass


class ShellError(Exception):
    pass


class Shell(object):
    """More documentation coming soon."""  # TODO: shell docstring
    _inputchar = ">"
    prompt = "\n" + _inputchar + " "
    postprompt = _inputchar

    helpstr = """
Type "help [cmd]" for cmd specific help.

helloworld exit       ungzip     quit       history
getcwd     stop       mkdir      rmdir      copy
cat        run        help

To execute a line using standard Python syntax, prefix it with '?'. For
example:  to set x to 5, type "?x = 5"."""

    invalid_arg_str = "Invalid arguments specified for {}"
    invalid_cmd_str = "Invalid command: {}"

    __all__ = ['run', 'do_q', 'do_quit', 'do_exit', 'do_stop', 'do_helloworld',
               'do_argtest', 'do_history', 'do_getcwd', 'do_mkdir', 'do_rmdir',
               'do_cat', 'do_ungzip', 'do_copy', 'do_help']

    def __init__(self):
        self._lastcmd = ''
        self._numcmds = 0
        self._history = []
        self.___running = False

    # helper function to get a module and save a namespace
    def _getmodule(self, name):
        """Given a module name as a string, eg 'os', return module os."""
        ret = __import__(name)
        return ret

    def _dbg(self, *msgs):
        """Print some debug messages."""
        if _DEBUG:
            print "### ",
            for msg in msgs:
                print msg,
            print

    def _onecmdupd(self, line):
        """Update history etc. for one command."""
        self._lastcmd = line
        self._numcmds += 1
        self._history.append(line)

    def _error(self, exc):
        """_error message."""
        print "Exception: ",
        print str(exc)

    def _input(self):
        """Take a single line of _input."""
        line = raw_input(self.prompt)
        print self.postprompt + line
        self._onecmdupd(line)
        try:
            cmd = self._parseline(line)
            self._onecmd(cmd[0], cmd[1])
        except Exception as e:
            self._error(e)

    def run(self):
        """Set the shell _running in a loop."""
        self._running = True
        while self._running:
            self._input()

    def _parseline(self, line):
        """Parse a command line."""
        if line[0] == '?':
            exec line[1:]

        if " " in line:
            firstspaceindex = line.index(' ')
            cmd = line[0:firstspaceindex]
            singletons = line[firstspaceindex:]
            singletons = singletons.split(' ')[1:]  # for some reason list
                                                    # includes ['', 1, 2],
                                                    # remove first ''
            args = tuple(singletons)
            running = "self.do_" + cmd + "(*{})".format(args)
        else:  # single word as command with no arguments
            running = "self.do_" + line + "()"
            args = ()
            cmd = line
            singletons = ''

        self._dbg(cmd, singletons)
        self._dbg(args)
        self._dbg(running)

        return (running, cmd)

    def _onecmd(self, line, cmd):
        """Execute a parsed command."""
        try:
            exec line
        except AttributeError:
            self._error(ParserError(self.invalid_cmd_str.format(cmd)))

    def do_q(self, *args):
        """Exit the shell."""
        self._running = False

    def do_quit(self, *args):
        """Exit the shell."""
        self.do_q()

    def do_exit(self, *args):
        """Exit the shell."""
        self.do_q()

    def do_stop(self, *args):
        """Exit the shell."""
        self.do_q()

    def do_helloworld(self, *args):
        """Hello World!  (just a test command)"""
        print "Hello World!"

    def do_argtest(self, *args):
        """Print any given args.  No use other than parser testing."""
        print args

    def do_history(self, *args):
        """Print shell history.\nusage: 'history'"""
        for command in self._history:
            print command

    def do_getcwd(self, *args):
        """Print the current working directory.\nusage: 'getcwd'"""
        os = self._getmodule('os')
        print os.getcwd()

    def do_mkdir(self, *args):
        """Make a directory.\nusage: 'mkdir [path]'"""
        making = args[0]
        os = self._getmodule('os')
        os.mkdir(making)
        print "Done"

    def do_rmdir(self, *args):
        """Remove a directory.\nusage: 'rmdir [path]'"""
        removing = args[0]
        os = self._getmodule('os')
        os.rmdir(removing)
        print "Done"

    def do_cat(self, *args):
        """Read a file and print the contents.\nusage: 'cat [filename]'"""
        filename = args[0]
        with open(filename, 'r') as fr:
            GET_TEXT = fr.read()
        print GET_TEXT

    def do_ungzip(self, *args):
        """Ungzip a file.\nusage: 'ungzip [filename] [?outfile]'"""
        gzip = self._getmodule('gzip')
        try:
            zipped = args[0]
        except IndexError:
            raise TypeError('ungzip: usage "ungzip [file] [?outfile]"')
        if len(args) == 2:
            location = args[1]
        else:
            location = zipped + "_copy"
        with open(location, 'wb') as fw:
            with gzip.open(zipped, 'rb') as fr:
                fw.write(fr.read())
        print location

    def do_copy(self, *args):
        """Copy a single file.\nusage: 'copy [filename] [?extension]'"""
        try:
            completed_name = args[0]
        except IndexError:
            raise TypeError('copy: usage "copy [filename] [?keepext]"')

        dotindex = completed_name.rindex('.')
        extension = completed_name[dotindex:]
        name = completed_name[:dotindex]
        outname = name + "_copy"

        if len(args) == 2:
            ext = args[1]
        else:
            ext = extension

        completed_out = outname + ext

        with open(completed_out, 'wb') as fw:
            with open(completed_name, 'rb') as fr:
                fw.write(fr.read())
        print completed_out
        self._dbg(name, dotindex, extension)
        self._dbg(outname, ext)

    def do_run(self, *args):
        """Run"""  # TODO: docstring
        self._dbg(args[0])
        try:
            execfile(args[0])
        except Exception as e:
            self._error(e)

    def do_tarify(self, *args):
        """Make a tar file from a directory."""
        os = self._getmodule('os')
        tarfile = self._getmodule('tarfile')
        gzip = self._getmodule('gzip')
        cwd = os.getcwd()
        target = args[0]
        tarname = target + "-compressed.tar.gz"
        os.chdir(target)

        self._dbg(target)
        self._dbg(tarname)

        with tarfile.open(tarname, 'w:gz') as tar:
            for name in os.listdir(target):
                tar

        os.chdir(cwd)
        return tar

    def do_help(self, *args):
        """Show a help string.\nusage: 'help [?func]'"""
        if len(args) == 0:
            print self.helpstr
        else:
            func = eval('self.do_' + args[0])
            print func.__doc__


if __name__ == '__main__':
    _DEBUG = True

shell = Shell()
