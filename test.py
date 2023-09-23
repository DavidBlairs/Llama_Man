import os, time

def printDateTimes():
    for file in os.listdir("."):
        if not os.path.isdir(file):
            print("File \"" + str(file) + " contains the following time attributes: ")
            fileStatistics = os.stat(file)

            print("\t Date Created:\t", time.ctime(fileStatistics.st_ctime))
            print("\t Date Accessed:\t", time.ctime(fileStatistics.st_atime))
            print("\t Date Modified:\t", time.ctime(fileStatistics.st_mtime))

printDateTimes()
decision = input("Are you sure you wish to update the modification and accessed time? (Y or N): ")
for file in os.listdir("."):
    if decision.startswith("N"):
        pass
    elif decision.startswith("Y"):
        os.utime(file, None)
printDateTimes()
input("All dates have been updated. Press enter to continue...")