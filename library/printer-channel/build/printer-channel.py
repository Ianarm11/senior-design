import sys
import argparse
import win32api
import win32print

################################################
# Driver function that either sends or receives.
################################################
def main(argv):
    args = parser()
    if args.action == True:
        Sender()
    else:
        Receiver()

##########################
# Parser function for CLI.
##########################
def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    # Arguments for whether the user wants to send or receive
    # Defaults as sender
    parser.add_argument('--sender', dest='action', action='store_true')
    parser.add_argument('--receiver', dest='action', action='store_false')
    parser.set_defaults(action=True)

    args = parser.parse_args()

    return args

############################################
# Main functionality for the Sender process.
############################################
def Sender():
    print("Sending..")
    # Grab the name of the default printer that Windows sets
    default_printer = win32print.GetDefaultPrinter()
    print("Default Printer Below: ")
    print(default_printer)

    # Open a handler for the default printer we are working with
    hprinter = win32print.OpenPrinter(default_printer)

    # Creation of the FORM_INFO_1 Struct to encapsulate our covert form
        # FORM_INFO_1 is a dictionary of Flags (int), Name (unicode), Size (dict), and ImageableArea (dict)
        # Size is a dictionary of the paper size. cx (int) and cy (int)
        # ImageableArea is a dictionary of the paper as a rectangle. left (int), top(int), right (int), bottom (int)
    size = {'cx':215900, 'cy':279400}
    image_area = {'left':0, 'top':0, 'right':215900, 'bottom':279400}
    form = {'Flags':1, 'Name': "Snow: Secret Covert Message", 'Size':size, 'ImageableArea':image_area}
    # Add the Form to the printer using the handler
    win32print.AddForm(hprinter, form)
    # Close the printer's handler
    win32print.ClosePrinter(hprinter)

def Receiver():
    print("Receiving..")
    # Grab the name of the default printer that Windows sets
    default_printer = win32print.GetDefaultPrinter()
    # Open a handler for the default printer we are working with
    hprinter = win32print.OpenPrinter(default_printer)
    # Grab the form from the printer using the name
        #TODO need to find a way to find the Form without knowing the full name.
    covert_form = win32print.GetForm(hprinter, "Snow: secret Covert Message")
    print("Covert Message: " + covert_form["Name"])
    # TODO: NEED TO DELETE THE FORM
    # Close the printer's handler
    win32print.ClosePrinter(hprinter)

main(sys.argv)
