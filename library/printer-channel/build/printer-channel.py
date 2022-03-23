import sys
import argparse
# Get these installed using pip
# import win32api
# import win32print

def main(argv):
    args = parser()
    if args.action == True:
        Sender()
    else:
        Receiver()

def parser():
    parser = argparse.ArgumentParser(description='Process the inputs..')

    # Arguments for whether the user wants to send or receive
    # Defaults as sender
    parser.add_argument('--sender', dest='action', action='store_true')
    parser.add_argument('--receiver', dest='action', action='store_false')
    parser.set_defaults(action=True)

    args = parser.parse_args()

    return args

def Sender():
    # Get Message from txt file in /data

    # Connect to printer using win32print.OpenPrinter(name_of_printer)

    # Create a printer form object

    # Add the form to the printer using win32.AddForm()

    # Close the printer using win32print.ClosePrinter(name_of_printer)

def Receiver():
    # Connect to the printer using win32print.OpenPrinter(name_of_printer)

    # Grab the the form we need using win32api.GetForm(form_id)

    # Grab the data from the form dictionary

    # Close the printer 

    # Print message


main(sys.argv)
