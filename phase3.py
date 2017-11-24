#Phase 3: Data Retrieval

def main():
    print("========|Data Retrieval|========")
    print("\nInput options:\ni) Q to quit\nii) output=full for full output format\niii) output=key for key output format")
    quit = False
    #This var indicates the output mode.
    # 1 => full; 0 => key
    outputMode = 1
    while(quit == False):
        #Indicating the current output format.
        if(outputMode == 1):
            print("\nOutput Format: Full")
        else:
            print("\nOutput Format: Key")
            
        query = input("\nEnter query: ")
        query = str(query).strip().replace(" ","")
        #may need a for loop to go through and any alpha char call .lower()
        #Decision making with input.
        if(query == 'Q') or (query == 'q'):
            quit = True
            break
        elif(query == "output=full"):
            outputMode = 1
            print("\n========|Output Format Changed|========")
            
        elif(query == "output=key"):
            outputMode = 0
            print("\n========|Output Format Changed|========")
        #Handle Query
        else:
            pass
        
    print("\n========|Program Closed|========")
    return 0


main()