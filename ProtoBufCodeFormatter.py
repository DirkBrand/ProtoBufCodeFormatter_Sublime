import sublime
import sublime_plugin
import subprocess
import os
import re
from sys import platform as _platform
import sys
import functools

PLUGIN_NAME = "ProtoBufCodeFormatter"


def Proto(name):
    return bool(re.search('.proto$', name))


class AutoformatOnSave(sublime_plugin.EventListener):

    def on_post_save(self, view):

        # if is_enabled_in_view(view) and
        # get_setting_for_active_view('autoformat_on_save', default=False)

        print os.path.basename(view.file_name())
        if Proto(view.file_name()):
            if sublime.load_settings("CodeFormatter.sublime-settings").get('enabled', True):
                if view.file_name():
                    self.process(view)

                    sublime.set_timeout(
                        functools.partial(view.run_command, 'revert'), 50)
                    regions = view.sel()
                    view.show(regions[0].begin(), True)

    def process(self, view):
        self.view = view
        self.startupinfo = None
        plugPath = sublime.packages_path()
        # Get gopath and format for stdin
        self.getenv()
        self.gobin = self._env.get('GOBIN', '')
        self.protopath = self._env.get('PROTOPATH', '')

        # Check OS and build the executable path
        if _platform == "win32":
                    # Startup info stuff, to block cmd window flash
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # Windows
            processPath = os.path.join(
                plugPath, "ProtoBufCodeFormatter", "bin", "ProtoBufCodeFormatter.exe")
        else:
            # linux and OS X
            processPath = os.path.join(
                plugPath, "ProtoBufCodeFormatter", "bin", "ProtoBufCodeFormatter")

        buildpath = os.path.join(
            plugPath, "ProtoBufCodeFormatter", "src", "ProtoBufCodeFormatter")


        # Check exe build
        if not os.path.isfile(processPath):
            sublime.status_message('Installing CodeFormatter dependencies...')
            print "building binary"
            try:
                os.makedirs(os.path.dirname(processPath))
            except:
                pass
            gocmd = os.path.join(self.gobin, 'go')

            subprocess.call([gocmd, 'build', '-o', processPath],
                env={'GOPATH': str(os.path.join(plugPath, "ProtoBufCodeFormatter"))},
                cwd=buildpath)

        # Open subprocess
        fileDir = os.path.dirname(view.file_name())
        self.protopath = os.pathsep.join(
            ['./', fileDir + '/', self.protopath, os.path.dirname(fileDir) + '/'])

        self.p = subprocess.Popen('"' + processPath + '" ' + view.file_name() + ' ' + self.protopath,
            startupinfo=self.startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=True)

        issues = self.p.communicate()[0]
        if len(issues) > 1:
            print issues
        

        # Create popup
        if len(issues) > 1:
            sublime.error_message(issues)

        print view.file_name(), "was formatted"

    def getenv(self):
        binflag = False
        s = sublime.load_settings("CodeFormatter.sublime-settings")
        _env = {}
        vars = [
            'GOPATH',
            'GOROOT',
            'PROTOBIN',
        ]

        cmdl = []
        for k in vars:
            cmdl.append('[[[$' + k + ']]' + k + '[[%' + k + '%]]]')
        cmd_str = ' '.join(cmdl)
        p = subprocess.Popen(['echo', cmd_str],
                             startupinfo=self.startupinfo,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             shell=True)
        out, err = p.communicate()
        if err:
            print "Popen Error:" + err

        mats = re.findall(
            r'\[\[\[(.*?)\]\](%s)\[\[(.*?)\]\]\]' % '|'.join(vars), out)
        for m in mats:
            a, k, b = m
            v = ''
            if a != '$' + k:
                v = a
            elif b != '%' + k + '%':
                v = b

            if v:
                _env[k] = v

        if s.get('GOPATH'):
            _env['GOPATH'] = os.pathsep.join(s.get('GOPATH'))
        else:
            print "GOPATH could not be set"

        if s.get('GOBIN'):
            bpath = s.get('GOBIN')
            for b in bpath:
                if os.path.exists(b):
                    _env['GOBIN'] = os.path.normcase(b)
                    binflag = True
                    break
        if not binflag:
            print "CodeFormatter: GOBIN could not be set!"
            sublime.status_message("CodeFormatter: GOBIN could not be set!")

        if s.get('PROTOPATH'):
            _env['PROTOPATH'] = os.pathsep.join(s.get('PROTOPATH'))
        else:
            print "CodeFormatter: PROTOPATH could not be set!"

        if s.get('PROTOBIN'):
            _env['PROTOBIN'] = os.pathsep.join(s.get('PROTOBIN'))
        else:
            print "PROTOBIN could not be set"

        self._env = _env
