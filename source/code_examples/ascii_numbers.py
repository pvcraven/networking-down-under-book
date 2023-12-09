"""
This program takes an input string, and prints it out in a banner
format.
"""

# Height of our characters
line_height = 7

# List of characters
characters = []

character = """
 ### 
#   #
#   #
#   #
#   #
#   #
 ### 
"""
characters.append(character.split("\n"))

character = """
 # 
## 
 # 
 # 
 # 
 # 
###
"""
characters.append(character.split("\n"))

character = """
 ### 
#   #
    #
   # 
  #  
 #   
#####
"""
characters.append(character.split("\n"))

character = """
 ### 
#   #
    #
  ## 
    #
#   #
 ### 
"""
characters.append(character.split("\n"))

character = """
#   # 
#   # 
#   # 
######
    # 
    # 
    # 
"""
characters.append(character.split("\n"))

character = """
#####
#    
#    
#### 
    #
    #
#### 
"""
characters.append(character.split("\n"))

character = """
 ### 
#   #
#    
#### 
#   #
#   #
 ### 
"""
characters.append(character.split("\n"))

character = """
#####
    #
    #
   # 
  #  
 #   
#    
"""
characters.append(character.split("\n"))

character = """
 ### 
#   #
#   #
 ### 
#   #
#   #
 ### 
"""
characters.append(character.split("\n"))

character = """
 ### 
#   #
#   #
#####
    #
#   #
 ### 
"""
characters.append(character.split("\n"))

character = """
  
  
  
  
  
##
##
"""
characters.append(character.split("\n"))

# Create a mapping of character letters, to letters in our list
mapping_characters = "0123456789."


def print_string(input_string: str):
    """
    Print out the string in a banner format.

    :param input_string: Input string
    """

    # Create a list that, instead of the string, has the index locations
    # of our banner characters. So instead of "1.2" we have [1, 10, 2]
    index_locations = [mapping_characters.index(character) for character in input_string]

    # Now loop through each line
    for line_no in range(1, line_height + 1):
        # Loop though each index location to print
        for index_location in index_locations:
            # Print that line of the character
            print(characters[index_location][line_no], end="  ")
        # Go to the next line
        print()

print_string("3.141592653")
print()
print_string("1.41421")