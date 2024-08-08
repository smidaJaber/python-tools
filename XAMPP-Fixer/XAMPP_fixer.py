import subprocess
import fnmatch
import os
import psutil

#XAMPP_path= "C:/xampp/"
#APACHE_stop = os.path.join(XAMPP_path, "apache_stop.bat")
APACHE_process = "httpd.exe"
MYSQL_process = "mysqld.exe"

print("########################################################")
print("############        XAMPP FIXER             ############")
print("########################################################")
print("")
print("Trying to stop xaampp services : Apache + MySQL..")
subprocess.Popen([r'C:/xampp/apache_stop.bat'])
subprocess.Popen([r'C:/xampp/mysql_stop.bat'])


print("Killing process..")
os.system("""taskkill /f /im httpd.exe""")
os.system("""taskkill /f /im mysqld.exe""")


def removeFilesByMatchingPattern(dirPath, pattern):
    listOfFilesWithError = []
    for parentDir, dirnames, filenames in os.walk(dirPath):
        for filename in fnmatch.filter(filenames, pattern):
            try:
                os.remove(os.path.join(parentDir, filename))
                print(filename + " was deleeeeeeted")
            except:
                print("Error while deleting file : ",
                      os.path.join(parentDir, filename))
                listOfFilesWithError.append(os.path.join(parentDir, filename))
    return listOfFilesWithError


listOfErrors = removeFilesByMatchingPattern(
    'C:/xampp/mysql/data', 'aria_log.*')
print('Files that can not be deleted : ' + str(len(listOfErrors)))
for filePath in listOfErrors:
    print(filePath)

print('Done clean up!')
