from TPLinkController import TP_Link_Controller

controller = TP_Link_Controller("your email", "your password", DEBUG_MODE=True)

# Login before doing anything
controller.login()

# Do what ever you want
controller.turn_on_2G()

# Close the session
controller.close()