"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class criu(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches) 
		#                                    - Returns True if any lines in output match any of 
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		# 
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of 
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#                                    - Get input from user and return output
		# shutit.fail(msg)                   - Fail the program and exit with status 1
		# 
		shutit.send('rm -rf /tmp/vg-1')
		box = shutit.send_and_get_output('vagrant box list 2>/dev/null | grep kimh/criu')
		if box == '':
			shutit.send('vagrant box add https://atlas.hashicorp.com/kimh/boxes/criu',note='Download the criu vagrant box')
		shutit.send('mkdir /tmp/vg-1')
		shutit.send('cd /tmp/vg-1')
		shutit.send('vagrant init kimh/criu')
		shutit.send('vagrant up',note='Set up the criu VM')
		shutit.login(command='vagrant ssh',note='Log into the criu VM')
		shutit.send('docker run -d --name criu busybox sleep 999d',note='Start a container which runs for 999 days, and get its id')
		shutit.send('docker ps',note='Confirm it is now running')
		shutit.send('docker checkpoint criu',note='Now we checkpoint that container, which stops it (use --leave-running=true) to leave it running.')
		shutit.send('docker ps',note='Confirm it is NOT running')
		shutit.send('docker restore criu',note='Restore the container with the process running')
		shutit.send('docker ps',note='It is running again!')
		shutit.send('docker rm -f criu',note='Now a more sophisticated example, where we stop a process with state and restore it.')
		shutit.send('''docker run --name np --rm busybox:latest /bin/sh -c 'i=0; while true; do echo -n "$i "; i=$(expr $i + 1); sleep 1; done' &''',note='Start a container that outputs an incrementing number per second')
		shutit.send('sleep 10',note='wait 10 seconds')
		shutit.send('docker checkpoint np',note='Stop the container and save its state.')
		shutit.send('sleep 10',note='wait 10 seconds')
		shutit.send('docker restore np',note='Restore the state where we were')
		shutit.pause_point('play with criu')
		# TODO: container migration: http://blog.circleci.com/checkpoint-and-restore-docker-container-with-criu/
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is 
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return criu(
		'shutit.criu.criu.criu', 1183039072.00,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['tk.shutit.vagrant.vagrant.vagrant']
	)

