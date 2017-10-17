################################
#     PYTHON VERNAM CIPHER     #
#         BY EDUARDO           #
################################

import random     #   Required modules   #
import time       # used in this program #

ALPHABET = [" ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
# Set the ALPHABET array (containing a space on position 0) and the OTP array to empty
OTP = []

def generateOTP():
    '''Generate the One-Time Pad, it acts as a key'''
    
    ranInst = random.SystemRandom() # Random System Instance, harder to reverse and therefore to decrypt
    for i in range(336):# range 336 because it is 48x8
        OTP.append(ALPHABET[ranInst.randint(1,26)]) # Random letter from list (1 to 26 because 0 is a space)
    cd = 0 # Counting the letters
    cl = 0 # Counting each group of 6 letters
    stringOTP = ""
    for i in range(336):
        cd += 1
        stringOTP += OTP[i]
        if cd == 6:
            stringOTP += " " # Each 6 letters have spaces (for asthetics lol)
            cd = 0 # Set letter counting variable to 0
            cl += 1 # Set group variabled to plus 1
            if cl == 8:
                stringOTP += "\n" # New line/row
                cl = 0 # Set group variabled to 0
    with open("OTP.txt","w+") as wr: # Open OTP.txt as wr
        wr.write(stringOTP) # Write the One-Time Pad to the file
    
def encryptMessage(message,openExtOTP):
    '''Encrypt the message using a string message and a string key (OTP.txt, one-time pad)'''
    
    messagePosition = [] # Set variable to empty Array
    cipherPosition = [] # Set variable to empty Array
    
    for i in message:
        try:
            messagePosition.append(ALPHABET.index(i)) # Try to get position of the letter in the local ALPHABET list
        except:
            print("Unsupported Character used! Returning....") # If error occurs, display error message
            init() # And return to init function 
    if openExtOTP == True: # If openExtOTP is True
        while 1:
            try: # Try to open file 
                cFile = open(input("Enter the OTP filename: ") + ".txt","r")
                break
            except: # Otherwise, print error and carry on loop until it gets valid file
                print("Error! File doesn't exist.")
                pass
    else: # If openExtOTP is None, or False       
        cFile = open("OTP.txt","r") # Open OTp.txt
        cipher = "" # Set cipher variable to empty string
    for i in cFile.readlines():
        cipher = cipher + i # Add the character to file
        cipher = cipher.replace(" ","") # Replace all spaces to nothing
        cipher = cipher.replace("\n","") # Replace all new lines to nothing

    for s in cipher:
        cipherPosition.append(ALPHABET.index(s)) # Add the position of the character on OTP in the ALPHABET to the list cipherPosition
    cipherText = "" # Set cipherText variable to empty string
    a = -1 # Set a variable to -1 (python indexing start as zero)
    for po in messagePosition:
        a += 1 # Add 1 to a variable
        add = int(po) + int(cipherPosition[a]) # Set add variable to integer value of po and cipherPosition position a added together
        cipherText = cipherText + " " + str(add)  # Set cipherText to it's own value plus a space and the position
        
        ##** TODO: save the cipherText as letters instead of numbers **##
    fn = str(random.randint(1,999)) # Gets a random value 
    with open("CT_" + fn + ".txt", "w+") as opned: # Make a file with this random value
        opned.write(cipherText) # Write cipherText to the file 
    init() # and  return to init function
    
def decryptMessage(cipherText, OTP):
    '''Basically almost the same as encrypt function however it takes away the position to get the plain text that has been encrypted '''
    
    messagePosition = [] # Set variable to empty Array
    cipherPosition = [] # Set variable to empty Array
    
    with open(OTP,"r") as fileOpen:
        cleanOTP = "" # Set cleanOTP to empty string
        for i in fileOpen.readlines():
            cleanOTP = cleanOTP + i # Add the character to file
            cleanOTP = cleanOTP.replace(" ","") # Replace all spaces to nothing
            cleanOTP = cleanOTP.replace("\n","") # Replace all new lines to nothing
        for z in cleanOTP:
            cipherPosition.append(ALPHABET.index(z)) # Add the position of the letter z to the list cipherPosition  
              
    with open(cipherText,"r") as fileOpen: # Open cipherText as fileOpen
        cleanCiphertxt = "" # Set cleanCiphertxt to empty string
        for i in fileOpen.readlines()[0].split():
            messagePosition.append(i) # Add the position of the i to the list
        
    plainTextP = [] # Set variable to empty Array
    for i in range(len(messagePosition)):
        add = int(messagePosition[i]) - int(cipherPosition[i]) # Same process as encrypt, but this time is subtracting the positions
        plainTextP.append(add) # Add the position of letter to the plainTextP array
    plainText = "" # Set variable to empty string
    with open("plainText.txt","w+") as f:
        for i in plainTextP:
            plainText = plainText + str(ALPHABET[int(i)]) # Add the character ALPHABET position i to the plainText variable
        f.write(plainText) # Write the plainText to the file
    init() # Return to init function
    
def init():
    goTo = input("""
        VERNAM CIPHER PY (EN/DE)CRYPTER
    
        1- Encrypt
        2- Decrypt
        3- Quit
        
    
    """).lower()
    if goTo in ["1","encrypt","e"]:
        while 1:
            choice = input("Do you want to load an external OTP key? (Y/N)").lower()
            if choice == "y":
                extOTP = True
                break
            if choice == "n":
                extOTP = False
                break
            else:
                print("Enter a command!")
        message = input("Enter the message: ").upper()
        print("Generating OTP...")
        generateOTP()
        time.sleep(2)
        print("Encrypting message...")
        encryptMessage(message,extOTP)
    if goTo in ["2","decrypt","d"]:
        print("Make sure your OTP file is in this directory!!")
        try:
            decryptMessage(input("Enter the ciphertext filename (w/o '.txt.'): ") + ".txt","OTP.txt")
        except:
            print("Check the filename and try again!")
            init()
    if goTo in ["3","quit","q"]:
        print("Goodbye!")
        quit()
    else:
        print("Could not recognise command! Try again.")
        init()
    
    
if __name__ == "__main__":
    
    init()
    input("press enter to coninue...")
