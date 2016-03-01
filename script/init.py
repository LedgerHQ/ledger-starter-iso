#!/usr/bin/env python
# -*- coding: utf-8 -*-
# USES :
# https://github.com/LedgerHQ/btchip-python
# https://code.google.com/p/prettytable/
#https://github.com/erikrose/blessings

from binascii import hexlify, unhexlify
from mnemonic import Mnemonic
from btchip.btchip import *
from prettytable import PrettyTable
from blessings import Terminal
import getpass
import sys
import os

def print_logo_line(line, leftMargin):
    print term.move_x(leftMargin),
    print line

def print_logo():
    os.system('clear')
    leftMargin = term.width/2 - 37
    print term.cyan,
    print term.move_y(term.height/2 - 7),
    print_logo_line("    ████   ██████████████      █                  █                     ", leftMargin)
    print_logo_line("  ██████   ████████████████    █       ████   █████  █████  ████  █ ███ ", leftMargin)
    print_logo_line(" ███████   █████████████████   █      █    █ █    █ █  ██  █    █ ██    ", leftMargin)
    print_logo_line(" ███████   █████████████████   █      ██████ █    █  ██    ██████ █     ", leftMargin)
    print_logo_line("           █████████████████   █      █      █   ██  ████  █      █     ", leftMargin)
    print_logo_line(" ███████   █████████████████   ██████  ████   ███ █ █    █  ████  █     ", leftMargin)
    print_logo_line(" ███████   █████████████████                         ████               ", leftMargin)
    print_logo_line(" ███████   █████████████████                                            ", leftMargin)
    print_logo_line(" ███████   █████████████████     █      █     █       █ █        █      ", leftMargin)
    print_logo_line("                                  █    ███   █  ████  █ █  ████ █████   ", leftMargin)
    print_logo_line(" ███████   ███████   ███████       █  ██ █  ██      █ █ █ █    █ █      ", leftMargin)
    print_logo_line(" ███████   ███████   ███████       ████  ████   ███ █ █ █ ██████ █      ", leftMargin)
    print_logo_line("  ██████   ███████   ██████         ██    ██   █   ██ █ █ █      █      ", leftMargin)
    print_logo_line("    ████   ███████   ████            █     █    ███ █ █ █  ████   ███   ", leftMargin)
    print term.normal


def print_screen_title(title):
    os.system('clear')
    print  "-------------------------" + "".join(["-" for num in range(len(title))]) + "-----"
    print  "=   " + term.cyan("LEDGER STARTER") + "   =    " + term.cyan(title) +  "   ="
    print  "-------------------------" + "".join(["-" for num in range(len(title))]) + "-----"
    print ""

def progress_dots(plusMinus):
    global dotsCount
    dotsCount += plusMinus
    dots = "".ljust(dotsCount, ".")
    print term.move_up + "                                          "
    print term.move_up + dots
    if (dotsCount > 30):
        dotsCount = 0
    time.sleep(1)

def get_ledger_wallet():
    app = False
    try:
        dongle = getDongle(False)
        app = btchip(dongle)
    except Exception:
        app = False

    return app

def wait_plugged_dongle():
    global dotsCount
    print "Please " + term.bold("plug") + " your " + term.bold("Ledger Wallet") + " dongle in an USB port.\n\n"
    app = False
    dotsCount = 0
    while app == False:
        app = get_ledger_wallet()
        progress_dots(3)
    print ""
    return app

def wait_unplugged_dongle():
    global dotsCount
    print ("Please " + term.bold("unplug") + " your " + term.bold("Ledger Wallet") + " dongle from the USB port.\n\n")
    dotsCount = 0
    app = True
    while app != False:
        app = get_ledger_wallet()
        progress_dots(3)
    print ""

def yes_or_no_question(question):
    while True:
        answer = raw_input(question + " (Yes/No) ")
        if(answer.lower() == "yes"):
            return True
        if(answer.lower() == "no"):
            return False

def generate_new_wordlist():
    mnemo = Mnemonic('english')
    words = mnemo.generate(256)
    return words

def print_wordlist(words):
    wordlist = words.split(' ')

    x = PrettyTable(["Left", "Right"])
    x.align["Left"] = "l"
    x.align["Right"] = "l"
    x.header = False
    x.padding_width = 2
    x.add_row([" 1: " + term.bold(wordlist[0]),  " 2: " + term.bold(wordlist[1])  ])
    x.add_row([" 3: " + term.bold(wordlist[2]),  " 4: " + term.bold(wordlist[3])  ])
    x.add_row([" 5: " + term.bold(wordlist[4]),  " 6: " + term.bold(wordlist[5])  ])
    x.add_row([" 7: " + term.bold(wordlist[6]),  " 8: " + term.bold(wordlist[7])  ])
    x.add_row([" 9: " + term.bold(wordlist[8]),  "10: " + term.bold(wordlist[9])  ])
    x.add_row(["11: " + term.bold(wordlist[10]), "12: " + term.bold(wordlist[11]) ])
    x.add_row(["13: " + term.bold(wordlist[12]), "14: " + term.bold(wordlist[13]) ])
    x.add_row(["15: " + term.bold(wordlist[14]), "16: " + term.bold(wordlist[15]) ])
    x.add_row(["17: " + term.bold(wordlist[16]), "18: " + term.bold(wordlist[17]) ])
    x.add_row(["19: " + term.bold(wordlist[18]), "20: " + term.bold(wordlist[19]) ])
    x.add_row(["21: " + term.bold(wordlist[20]), "22: " + term.bold(wordlist[21]) ])
    x.add_row(["23: " + term.bold(wordlist[22]), "24: " + term.bold(wordlist[23]) ])

    print x

def BIP39_to_seed(words):
    seed = hexlify(Mnemonic.to_seed(words))
    return seed

def show_main_menu():
    print_screen_title("MAIN MENU")
    print "[1] Create a new wallet"
    print "[2] Restore an existing wallet from your 24 words backup"
    print "[3] Reset your Ledger Wallet"
    print "[9] Halt"
    print "\n"

    choice = raw_input("Please enter your choice (1, 2, 3 or 9) and validate with Enter: ")

    if (str(choice) == "1"):
        create_new_wallet()
    elif (str(choice) == "2"):
        restore_wallet("")
    elif (str(choice) == "3"):
        delete_wallet()
    elif (str(choice) == "9"):
        os.system("/sbin/halt")
    else:
        show_main_menu()

def choose_PIN_code():
    pinOK = False
    PIN = ""
    error = ""

    while pinOK == False:
        print_screen_title("PIN SELECTION (step 1/3)")
        if len(error) > 0 :
            print "An " + term.bold("error occurred") + "."
            print error + "\n"
        error = ""
        PIN  = ""
        PIN2 = ""

        try:
            PIN = getpass.getpass("Please type a 4-digit PIN code of your choice: ")

            if(PIN.isdigit()):
                if(len(str(PIN)) == 4):
                    print_screen_title("PIN SELECTION (step 1/3)")
                    PIN2 = getpass.getpass("Please confirm your PIN code by typing it again: ")

                    if(PIN == PIN2):
                        pinOK = True
                    else:
                        error = "Both PIN codes didn't match. Please try again."
                else:
                    error = "Invalid PIN code length. Please provide exactly 4 characters."

            else:
                error = "Invalid PIN code: only digits are accepted."
        except Exception:
            error = "Invalid PIN code. ¨Please provide 4 digits (no special characters)."

    return PIN

def create_new_wallet():
    PIN = choose_PIN_code()
    words = generate_new_wordlist()

    print_screen_title("YOUR WALLET'S PAPER BACKUP (step 2/3)")
    print "Please " + term.bold("write down those 24 words") + " and keep them in a " + term.bold("safe place") +"."
    print term.bold("Be careful") + " and double-check your written copy before going on to the next step."
    print "You won't be able to get them back once it's done!\n"
    print_wordlist(words)

    if yes_or_no_question("\nGo on to the next step? "):
        start_flashing(PIN, words)

def restore_wallet(PIN):
    if(len(PIN) == 0):
        PIN = choose_PIN_code()

    retry = True
    while retry:
        userWords = []

        print_screen_title("RESTORE AN EXISTING WALLET (step 2/3)")
        print "Please type in your 24 words backup phrase."
        print "Warning: BIP39 is "+ term.bold("case-sensitive!")+"\n"

        for i in range(1, 25):
            validWord = False
            while not validWord:
                typedWord = raw_input("Word #"+str(i)+"? ")
                typedWord = typedWord.lower()
                if(len(typedWord) > 0):
                    if(typedWord in english_wordlist):
                        userWords.append(typedWord)
                        validWord = True
                    else:
                        print "This word is not in the official BIP39 english wordlist."
                else:
                    print "Type a word a please."

        bip39Seed = " ".join(userWords)
        mnemo = Mnemonic('english')

        if mnemo.check(bip39Seed) == False:
            print ""
            print "An " + term.bold("error occurred") + "."
            print "Your BIP39 seed is invalid !\n"
            question = "Try again to type the seed?"
            retry = yes_or_no_question(question)
        else:
            retry = False

            print "\nWe're almost done!"
            print "Here is your BIP39 seed:\n"
            print_wordlist(bip39Seed)
            print "\nPlease check that it is correct."

            question = "Continue and restore your wallet from this seed?"
            choice = yes_or_no_question(question)

            if choice == True:
                start_flashing(PIN, bip39Seed)
            else:
                restore_wallet(PIN)

def delete_warning():
    print_screen_title("DELETING AN EXISTING WALLET")

    print "Your " + term.bold("Ledger Wallet") + " will be " + term.bold("erased")+"!"
    print "Ledger is not responsible in case of misuse of this software."
    print "Make sure you still have your "+ term.bold("24 words backup") + " (BIP39)."
    print ""
    print "This script will attempt to reset your Ledger Wallet."
    print "You will have to unplug and plug your wallet back multiple times.\n"

    return yes_or_no_question("Proceed and erase your Ledger Wallet?")

def delete_wallet():
    global dotsCount

    confirmDelete = delete_warning()
    if confirmDelete:
        print_screen_title("DELETING AN EXISTING WALLET")

        remainingAttempts = 999
        while remainingAttempts > 0:

            app = wait_plugged_dongle()

            # Got the dongle!
            print "Trying to delete the wallet...\n"
            try:
                app.verifyPin("999999")
            except BTChipException, e:
                print ""
                if ((e.sw & 0xfff0) == 0x63c0):
                    remainingAttempts = int(e.sw - 0x63c0)

                    if remainingAttempts != 0:
                        print "OK! ("+str(remainingAttempts)+" remaining steps)"

                if(e.sw == 0x6985 or  remainingAttempts == 0):
                    print term.green("Success!") +" Your wallet has been safely erased."
                    remainingAttempts = 0

                if(e.sw == 0x6faa):
                    print "No wallet to erase."
                    remainingAttempts = 0

            print ""
            wait_unplugged_dongle()

def start_flashing(PIN, words):

    print_screen_title("Provisioning your wallet (step 3/3)")
    app = wait_plugged_dongle()

    print "Found your Ledger Wallet!\n"
    print "Trying to provision your wallet..."
    print "--------------------------------------------------------"
    print "Please wait while your data is written to the chip."
    print "Do not disconnect the wallet nor turn off your computer!"
    print "--------------------------------------------------------\n"

    # SETTING UP THE DONGLE
    returnToMenu = True
    try:
        app.setup(btchip.OPERATION_MODE_WALLET,
                  btchip.FEATURE_RFC6979,
                  0x00,
                  0x05,
                  PIN,
                  None,
                  btchip.QWERTY_KEYMAP,
                  BIP39_to_seed(words).decode('hex'))

        print "\n----------------------------\n"
        print term.green("Success!") +" Your Ledger Wallet is ready!"

    except BTChipException, e:
        if e.sw == 0x6985:
            print "\n--------------------------------------------------------\n"
            print "An " + term.bold("error occurred") + " while performing setup."
            print "This Ledger device already contains a wallet!\n"
            print "If you want " + term.bold("to continue") + ", please " + term.bold("delete it") + "."
            print "To do this, you can use the third option on the main menu or type 3 wrong PIN codes on any supported Ledger Wallet client application."
        else:
            print "\n-----------------------------------------------------------------\n"
            print "An " + term.bold("error occurred") + " while performing setup. Please contact support."
            print e
            returnToMenu = False

    except Exception, e:
        print "\n-----------------------------------------------------------------\n"
        print "An " + term.bold("error occurred") + " while performing setup. Please contact support."
        print e
        returnToMenu = False

    print ""
    if(returnToMenu == True):
        raw_input("Press ENTER to go back to the main menu.")
    else:
        if yes_or_no_question("Do you want to try again?"):
            start_flashing(PIN, words)

def main():
    global term
    term = Terminal()

    global english_wordlist
    english_wordlist = []
    f = open('/etc/ledger/english.txt', 'r')
    for line in f:
        english_wordlist.append(line.strip())

    print_logo()
    time.sleep(2)
    while True:
        show_main_menu()

if __name__ == "__main__":
    main()
