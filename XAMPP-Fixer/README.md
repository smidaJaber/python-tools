## **XAMPP Service Recovery Script**

**Purpose:**

Resolve issues with XAMPP Apache and MySQL services that may fail to start after unexpected system shutdowns or power outages (as I experienced). It addresses a common problem where these services fail to run/become unresponsive due to corrupted or locked files.

**How it works:**

1. **Stops XAMPP Services:** The script attempts to gracefully stop the Apache and MySQL services using their respective batch files.
2. **Kills Processes:** If the services are not stopped successfully, the script forcefully terminates any remaining `httpd.exe` and `mysqld.exe` processes using the `taskkill` command.
3. **Removes Corrupted Files:** The script scans the MySQL data directory (`C:/xampp/mysql/data`) for files with the pattern `aria_log.*`. These files are often associated with corrupted data and can prevent the MySQL service from starting. The script attempts to delete these files.

**Usage:**

1. **Save the script:** Save the provided Python code as a `.py` file (e.g., `xampp_fixer.py`).
2. **Run the script:** 

   ```bash
   python xampp_fixer.py
   ```

**Note:**

- Ensure that you have Python installed on your system.
- Adjust the paths in the script if your XAMPP installation is located in a different directory.
- If the script encounters errors deleting files, manually check the listed files and try to delete them using a file explorer.
