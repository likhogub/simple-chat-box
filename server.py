import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('',11719))

def send(msg, target, sender="SERVER"):
	try:
		msg = (sender, msg)
		msg = json.dumps(msg).encode('utf-8')
		s.sendto(msg, target)
	except:
		pass
	return True

accounts = {"admin":"qwerty"}
address_by_user = {}
user_by_address = {}
clients = []

while True:
	try:
		while True:
			try:
				message, address = s.recvfrom(1024)
			except:
				continue
			else:
				
				msg = message.decode('utf-8')

				if address not in clients:

					if msg.startswith("/login"):
						try:
							_, user, pwd = msg.split(" ")

							if user in accounts.keys():
								if accounts[user] == pwd:
									clients.append(address)
									try:
										if address_by_user[user] != address:
											clients.remove(address_by_user[user])
									except:
										pass
									user_by_address[address] = user
									address_by_user[user] = address
									send("Login successful.", address)
								else:
									send("Wrong password.", address)
							else:
								send("User not found.", address)
						except:
							send("Login failed.", address)


					elif msg.startswith("/reg"):
						try:
							_, user, pwd = msg.split(" ")

							if user not in accounts.keys():
								if len(user) > 2:
									if len(pwd) > 2:
										accounts[user] = pwd
										send("Register successful.", address)
									else:
										send("Password must be at least 3 symbols.", address)
								else:
									send("Username must be at least 3 symbols.", address)
							else:
								send("Username is already taken.", address)
						except:
							send("Register failed.", address)
					
					elif msg.startswith("/pass"):
						try:
							_, user, old_pass, new_pass = msg.split(" ")

							if user in accounts.keys():
								if accounts[user] == old_pass:
									if len(new_pass) > 2:
										accounts[user] = new_pass
										send("Password successfully changed.", address)
									else:
										send("New password must be at least 3 symbols.", address)
								else:
									send("Incorrect password.", address)
							else:
								send("User not found.", address)
						except:
							send("Password change failed.", address)

					elif msg.startswith("/help"):
						send("Commands: \n/login [user] [pass] \n/reg [user] [pass] \n/pass [user] [old_pwd] [new_pwd]", address)

					
					else:
						send("Please sign-in. Use /help.", address)
					
					continue
				
				if msg.startswith("/msg"):
					try:
						_, user, text = msg.split(maxsplit=2)
						if user != user_by_address[address]:
							send(text, address_by_user[user], sender=(user_by_address[address] + " PM"))
							send("Message sent", address)
						else:
							send("Sending failed", address)
					except:
						send("Sending failed", address)
					continue

				elif msg.startswith("/exit"):
					clients.remove(address)
					send("You was disconnected from the server.", address)
					continue

				elif msg.startswith("/"):
					send("Unknown command", address)
					continue

				for client in clients:
					if (client != address):
						try:
							msg = (user_by_address[address], msg)
							msg = json.dumps(msg).encode('utf-8')
							s.sendto(msg, client)
						except:
							pass
	except:
		print("Server was exterminated, but he rose from the ashes")
