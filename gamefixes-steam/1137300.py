""" Sherlock Holmes Chapter One
UW support: RoseTheFlower/SherlockHolmesCOUltrawide
UW support: PhantomGamers/shco-wsf
"""

import os
import sys
import glob
import zipfile
import tarfile
import subprocess
import threading
import signal
import urllib.request
import hashlib
from time import sleep
from protonfixes import util

def _get_pid(procname: str) -> int:
    procpid = None
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit() and int(pid) > os.getpid()]
    for pid in pids:
        try:
            with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as proc_cmd:
                cmdline = proc_cmd.read().decode()
                if procname in cmdline and 'Z:\\' in cmdline:
                    procpid = int(pid)
        except IOError:
            continue
    return procpid

def get_pid(procname: str, untilfound: bool=False) -> int:
    """Get pid for processes launched afer the game that run in Proton (checks for Windows path)"""
    while True:
        pid = _get_pid(procname)
        if pid is not None or not untilfound:
            return pid

def install_xdotool(path_to_exe: str):
    """Copy xdotool (and libxdo.so.3) to executable's directory"""
    if not os.path.isfile(os.path.join(path_to_exe, 'busybox_AR')):
        url = 'https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox_AR'
        hashsum = '49061d5037e33742e90d2eb94aa3d8e12305ac5df5d380a3d31d50d7c026a40b'
        file = os.path.join(path_to_exe, os.path.basename(url))
        urllib.request.urlretrieve(url, file)
        os.chmod(file, 0o775)
        with open(file, "rb") as f:
            file_sum = hashlib.sha256(f.read()).hexdigest()
        if hashsum != file_sum:
            os.remove(file)
    url = 'http://ftp.us.debian.org/debian/pool/main/x/xdotool/xdotool_3.20160805.1-5_amd64.deb'
    hashsum = 'baf0f340e8272e9313848f820ec962aaf843f17ee5737fe256c970f8f5f152b5'
    file = os.path.join(path_to_exe, os.path.basename(url))
    urllib.request.urlretrieve(url, file)
    with open(file, "rb") as f:
        file_sum = hashlib.sha256(f.read()).hexdigest()
    if hashsum == file_sum:
        os.chdir(path_to_exe)
        subprocess.call(['./busybox_AR', 'x', file, 'data.tar.xz'])
        os.chdir('../../..')
        with tarfile.open(f'{path_to_exe}/data.tar.xz', 'r') as zip_ref:
            for member in zip_ref.getmembers():
                if member.name == './usr/bin/xdotool':
                    member.name = os.path.basename(member.name)
                    zip_ref.extract(member, path_to_exe)
                    break
    os.remove(f'{path_to_exe}/data.tar.xz')
    os.remove(file)
    url = 'http://ftp.us.debian.org/debian/pool/main/x/xdotool/libxdo3_3.20160805.1-5_amd64.deb'
    hashsum = 'c47096b186fc848d8677b1f307c2e76cd1490b2470b30b3bde6f31ed4a64297a'
    file = os.path.join(path_to_exe, os.path.basename(url))
    urllib.request.urlretrieve(url, file)
    with open(file, "rb") as f:
        file_sum = hashlib.sha256(f.read()).hexdigest()
    if hashsum == file_sum:
        os.chdir(path_to_exe)
        subprocess.call(['./busybox_AR', 'x', file, 'data.tar.xz'])
        os.chdir('../../..')
        with tarfile.open(f'{path_to_exe}/data.tar.xz', 'r') as zip_ref:
            for member in zip_ref.getmembers():
                if member.name == './usr/lib/x86_64-linux-gnu/libxdo.so.3':
                    member.name = os.path.basename(member.name)
                    zip_ref.extract(member, path_to_exe)
                    break
    os.remove(f'{path_to_exe}/data.tar.xz')
    os.remove(file)

def load_trainer(trainer: str):
    """Load trainer after game launches, minimizes it, and kills it when game closes"""
    path_to_exe = os.path.dirname(trainer)
    if not os.path.isfile(os.path.join(path_to_exe, 'xdotool')):
        install_xdotool(path_to_exe)
    #Wait for game to launch before launching trainer
    pid = get_pid(os.path.basename(sys.argv[2]), True)
    #Launch trainer
    with subprocess.Popen([sys.argv[0], 'runinprefix', trainer]):
        #Get trainer window
        window=None
        while True:
            #Wait for trainer to launch and get pid
            pid = get_pid(os.path.basename(trainer), True)
            try:
                #Get window from pid from trainer
                window = subprocess.check_output(f'LD_LIBRARY_PATH="{path_to_exe}" "{path_to_exe}"/xdotool search --pid {pid} --onlyvisible', shell=True, universal_newlines=True)
            except subprocess.CalledProcessError:
                continue
            #Trainer launches many processes check if the pid found has window
            if window is not None:
                break
        #Minimize trainer
        subprocess.call(f'LD_LIBRARY_PATH="{path_to_exe}" "{path_to_exe}"/xdotool windowminimize {window}', shell=True)
        #Wait for game to finish and then kill trainer process
        while True:
            sleep(5)
            pid = get_pid(os.path.basename(sys.argv[2]))
            if pid is None:
                pid = get_pid(os.path.basename(trainer))
                os.kill(pid, signal.SIGKILL)
                break

def main():
    """Only applies fix for UW display. Checks for UW fix zip or extracted files, if none found download one"""
    screen_width,screen_height = util.get_resolution()
    #Checks for UW in case there's an UW fix present but display is not.
    #eg. the monitor changed or the files were moved from a PC to a SteamDeck
    if screen_width/(screen_height/9) > 21:
        install_dir = glob.escape(util.get_game_install_path())
        bin_path = 'SH9/Binaries/Win64'
        path_to_exe = os.path.join(install_dir, bin_path)
        uw_file = os.path.join(path_to_exe, 'Sherlock Holmes CO Ultrawide.exe')
        uw_zip = os.path.join(install_dir,'Sherlock.Holmes.CO.Ultrawide.zip')
        uw2_file = os.path.join(path_to_exe, 'SUWSF.asi')
        uw2_zip = os.path.join(install_dir, 'SHCO-WSF.zip')
        #Previously it didn't download anything, only checked if an UW fix was present.
        #added download since now it checks for UW display.
        if not ((os.path.isfile(uw_zip) or os.path.isfile(uw_file)) or (os.path.isfile(uw2_zip) or os.path.isfile(uw2_file))):
            url = 'https://github.com/RoseTheFlower/SherlockHolmesCOUltrawide/releases/download/v1.0/Sherlock.Holmes.CO.Ultrawide.zip'
            hashsum = '9142cfb7e64b95243e9f5df9f3aae19304128c5def51d9c1b292d23c02321eee'
            file = os.path.join(path_to_exe, os.path.basename(url))
            urllib.request.urlretrieve(url, file)
            with open(file, "rb") as f:
                file_sum = hashlib.sha256(f.read()).hexdigest()
            if hashsum != file_sum:
                os.remove(file)
        if os.path.isfile(uw_zip) or os.path.isfile(uw_file):
            if not os.path.isfile(uw_file):
                with zipfile.ZipFile(uw_zip, 'r') as zip_ref:
                    zip_ref.extract(os.path.basename(uw_file), path_to_exe)
            threading.Thread(target=load_trainer, args=[uw_file]).start()
        elif os.path.isfile(uw2_zip) or os.path.isfile(uw2_file):
            if not os.path.isfile(uw2_file):
                with zipfile.ZipFile(uw2_zip, 'r') as zip_ref:
                    zip_ref.extractall()
            util.winedll_override('dsound', 'n')
