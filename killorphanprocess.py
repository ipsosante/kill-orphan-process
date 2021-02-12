import logging
import click
import psutil
import os
import signal

from dataclasses import dataclass


@dataclass
class KillProcessCommand:

    process_name: str
    terminate_father_process: bool
    force: bool
    dry_run: bool
    logger: logging.Logger
    process_killed_count: int = 0


    def process_iter(self):
        """iterator that return process that name is sudo"""
        for proc in psutil.process_iter():
            self.logger.debug(f"iter on {proc}")
            if proc.name() == self.process_name and proc.ppid() == 1:
                yield proc

    def on_terminate(self, proc):
        self.process_killed_count += 1
        self.logger.info(f"process {proc} terminated")

    def kill_process_tree(self, pid, sig=signal.SIGTERM, timeout=2):
        """Kill a process tree (including grandchildren) with signal
        "sig" and return a (gone, still_alive) tuple.
        "on_terminate", if specified, is a callback function which is
        called as soon as a child terminates.
        """
        assert pid != os.getpid(), "won't kill myself"
        father_process = psutil.Process(pid)
        processes_to_kill = father_process.children(recursive=True)
        if not self.force:

            answer = input(
                f"kill all processes tree for #{father_process.pid} [{' '.join(father_process.cmdline())}] y/N ? "
            )
            if answer not in ("y", "Y", "yes", "Yes"):
                return ((), ())
        if self.terminate_father_process:
            processes_to_kill.append(father_process)
        for process_to_kill in processes_to_kill:
            try:
                if self.dry_run:
                    self.logger.warning(f"skip kill process {process_to_kill}")
                else:
                    process_to_kill.send_signal(sig)
            except psutil.NoSuchProcess:
                pass


        gone, alive = psutil.wait_procs(
            processes_to_kill, timeout=timeout, callback=self.on_terminate
        )
        return (gone, alive)

    def __call__(self):
        self.logger.info("-- begin --")
        for (i, proc) in enumerate(self.process_iter()):
            self.logger.info(f"#{i} - {proc}")
            self.kill_process_tree(proc.pid)
        self.logger.info(f'{self.process_killed_count} processes killed')
        self.logger.info("-- end --")

@click.command(help="An utility command for killing all orphan processes on unix/linux system")
@click.option( '--process-name', default='sudo',
              help="all child processes for <process-name> will be killed")
@click.option( '--terminate-father-process',  is_flag=True,
              help="is father process name must be also kill ?")
@click.option( '-f', '--force', is_flag=True,
              help="never prompt before removal")
@click.option( '--dry-run', is_flag=True,
              help="do not kill anything but log the list of process to kill")
@click.option( '--debug', is_flag=True,
              help="debug mode")
def cli(process_name, terminate_father_process, force, dry_run,
        debug):
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=log_level)
    logger = logging.getLogger(__name__)
    command = KillProcessCommand(process_name=process_name,
                                 terminate_father_process=terminate_father_process,
                                 force=force,
                                 dry_run=dry_run,
                                 logger=logger)
    command()


