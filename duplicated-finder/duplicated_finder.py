import argparse
import mysql.connector

# 🚨 Note: The database name (DB variable) is hardcoded to 'Bj_db' as it was set up for my personal use. 
# Please adjust it to suit your needs. 

def parseArgs():
    """Parses command-line arguments"""
    argp = argparse.ArgumentParser("duplicate finder")
    argp.add_argument("-e", "--except", nargs="*",
                      help="match all columns except those", required=False)
    argp.add_argument("-i", "--include", nargs="*",
                      help="match all those cols", required=False)
    minus = argp.parse_args()
    print(minus)


def getdbInfo():
    HOST, DB, PORT, USER, PASS = input(
        "Type host,db name,port, user, password(separer par virgule):").split(",")
    checkConnection(HOST, DB, PORT, USER, PASS)


def paramsGenerator(params):
    resultSel = ""
    resultGrp = ""
    resultHav = ""
    i = 0
    for p in params:
        if(i < len(params)-1):
            resultSel += p + ", "+" COUNT("+p+"), "
            resultGrp += p + ", "
            resultHav += " a."+p+" =b."+p+" And "
        else:
            resultSel += p + ", "+" COUNT("+p+") "
            resultGrp += p
            resultHav += " a."+p+" =b."+p+" "
        i += 1

    return [resultSel, resultGrp, resultHav]


def buildReq(params, table, act):
    """Builds the SQL query for finding duplicates"""
    para = paramsGenerator(params)

    rq = '''
    SELECT a.* 
     FROM {} a 
     join (SELECT {}, COUNT(*) FROM {} 
     GROUP BY {} 
     HAVING count(*) > 1 ) b on  {}
    '''.format(table, para[1], table, para[1], para[2])
    # print(rq)
    return rq


def closecnx(cnx):
    cnx.close()
    print("Connection closed. done.")


def executeSQL(HST, DTB, USR, passwd, sqlreq):
    try:
        conn = mysql.connector.connect(
            host=HST, database=DTB, user=USR, password=passwd)

        cursor = conn.cursor(buffered=True)

        cursor.execute(sqlreq)
        results = cursor.fetchall()
        countall = cursor.rowcount
        cursor.close()
        conn.close()
        strresult = ""
        k = 0
        for x in results:
            k += 1
            strresult += "Row {}: {} \n".format(str(k).zfill(2), x)
        return "Total duplicate: {}\n details :\n{}".format(countall, strresult)
    except (mysql.connector.Error)as err:
        return err.msg


def listalldb():
    conn = mysql.connector.connect(user='root', password='',
                                   host='localhost', buffered=True)
    cursor = conn.cursor()
    databases = ("show databases")
    cursor.execute(databases)
    results = []
    for (databases) in cursor:
        results.append(databases[0])
    format_row = "{:<8}" * (len(results) + 1)
    return format_row.format("", *results)


def decider(decision, currInfocnx):
    if(decision == "1"):
        checkConnection(currInfocnx["hst"], currInfocnx["dtb"],
                        "", currInfocnx["usr"], currInfocnx["pwd"])

    elif(decision == "2"):
        getdbInfo()
    elif(decision == "3"):
        print(listalldb())
        decider("99", currInfocnx)
    elif(decision == "4"):
        exit()
    elif(decision == "99"):
        redecision = input(
            " done listing db. whats next ? \n 1: retry \n 2: change connection info\n 3: Re-List all DB \n 4:exit\n")
        decider(redecision, currInfocnx)
    else:
        redecision = input(decision, " not recognized, type 1,2,3 or 4 !")
        decider(redecision, currInfocnx)


def getTables(HST="localhost", DTB="Bj_db", PRT="", USR="root", passwd=""):
    try:
        conn = mysql.connector.connect(
            host=HST, database=DTB, user=USR, password=passwd)

        cursor = conn.cursor(buffered=True)

        cursor.execute("SHOW tables")
        tables = cursor.fetchall()
        nbrTot = cursor.rowcount
        cursor.close()
        conn.close()
        format_row = "{:<8}" * (nbrTot + 1)
        tb = ""
        for x in tables:
            tb += " {} ".format(x)
        # + format_row.format("", *tb) +"\n"
        return "Found {}".format(nbrTot)+" tables: \n"+tb
    except (mysql.connector.Error)as err:
        print(err.msg)
        print("Failed to request : ", "host=", HST, "database=",
              DTB, "user=", USR, "password=", passwd)
        if(err.msg == "Unknown database '"+DTB+"'"):
            whattodo = input(
                "DB not Conencted, what to do ? \n 1: retry \n 2: change connection info\n 3: List all DB \n 4:exit\n")
        else:
            whattodo = input(
                "DB not Conencted, what to do ? \n 1: retry \n 2: change connection info\n 3:exit\n")

        currCnx = {}
        currCnx["hst"] = HST
        currCnx["dtb"] = DTB
        currCnx["usr"] = USR
        currCnx["pwd"] = passwd
        decider(whattodo, currCnx)


def getfields(HST="localhost", DTB="Bj_db", PRT="", USR="root", passwd="", table="*"):
    try:
        conn = mysql.connector.connect(
            host=HST, database=DTB, user=USR, password=passwd)

        cursor = conn.cursor(buffered=True)

        cursor.execute("select * from " + table)
        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description]
        cursor.close()
        conn.close()
        cols = ""
        cnt = 0
        for x in field_names:
            if(cnt < len(field_names) - 1):
                cols += "{},".format(x)
            else:
                cols += "{}".format(x)
            cnt += 1
        return cols
    except (mysql.connector.Error)as err:
        print(err.msg)
        print("Failed to connect using : ", "host=", HST,
              "database=", DTB, "user=", USR, "password=", passwd)
        if(err.msg == "Unknown database '"+DTB+"'"):
            whattodo = input(
                "DB not Conencted, what to do ? \n 1: retry \n 2: change connection info\n 3: List all DB \n 4:exit\n")
        else:
            whattodo = input(
                "DB not Conencted, what to do ? \n 1: retry \n 2: change connection info\n 3:exit\n")

        currCnx = {}
        currCnx["hst"] = HST
        currCnx["dtb"] = DTB
        currCnx["usr"] = USR
        currCnx["pwd"] = passwd
        decider(whattodo, currCnx)


def afterCnxDecider(decision, HST, DTB, USR, passwd):
    """Handles user input after a successful connection and decides on the next action."""
    tabs = getTables(HST, DTB, "", USR, passwd)
    print("Available tables:\n", tabs)
    tablename = input("what table to work on ?\n")
    fields = getfields(HST, DTB, "", USR, passwd, tablename)
    allf = fields.split(",")
    stableT = allf
    allf = len(allf)
    print("Available cols {}: \n".format(allf), fields)
    leschamps = input(
        "type champs separated by (,) exmpl: ID,numero,nom_f :\n").split(",")

    if(decision == "1"):
        print("Executing FIND_DUPLICATE in :\n -Database= {} \n -Table= {} \n INCLUDE: {}".format(DTB, tablename, leschamps))
        rq = buildReq(leschamps, tablename, "I")
    if(decision == "2"):
        print("Executing FIND_DUPLICATE in :\n -Database= {} \n -Table= {} \n EXCLUDE: {}".format(DTB, tablename, leschamps))
        currFields = leschamps
        rest = []
        c = 0
        for x in stableT:
            if(x != currFields[c]):
                rest.append(x)
        c += 1
        rq = buildReq(rest, tablename, "E")
    if(decision == "3"):
        print("Executing FIND_DUPLICATE in :\n -Database= {} \n -Table= {} \n MATCH-ALL: {}".format(DTB, tablename, fields))
        rq = buildReq(leschamps, tablename, "*")

    oppResult = executeSQL(HST, DTB, USR, passwd, rq)
    print("Result: \n", oppResult)
    afterTrueCnx(HST, DTB, USR, passwd)


def afterTrueCnx(HST, DTB, USR, passwd):
    print("Find duplicate will execute on DB=" + DTB)
    after = input("Search by Include(specify champs to match) or exclude(specify chmps to except) ?\n 1: Search by Include \n 2: Search by Exclude \n 3: Match all champs \n")
    afterCnxDecider(after, HST, DTB, USR, passwd)


def checkConnection(HST="localhost", DTB="Bj_db", PRT="", USR="root", passwd=""):
    try:
        conn = mysql.connector.connect(
            host=HST, database=DTB, user=USR, password=passwd)

        conn.close()
        print("DB connected sucessfully!")
        afterTrueCnx(HST, DTB, USR, passwd)
        return True
    except (mysql.connector.Error)as err:
        print(err.msg)
        print("Failed to connect using : ", "host=", HST,
              "database=", DTB, "user=", USR, "password=", passwd)
        if(err.msg == "Unknown database '"+DTB+"'"):
            whattodo = input(
                "DB not Conencted, what to do ? \n 1: retry \n 2: change connection info\n 3: List all DB \n 4:exit\n")
        else:
            whattodo = input(
                "DB not Conencted, what to do ? \n 1: retry \n 2: change connection info\n 3:exit\n")

        currCnx = {}
        currCnx["hst"] = HST
        currCnx["dtb"] = DTB
        currCnx["usr"] = USR
        currCnx["pwd"] = passwd
        decider(whattodo, currCnx)


def previewData():
    return True


def prepareFinderParams():
    return True


def showResults():
    return True


print("Duplicate finder:")
print("Connecting to main database: Bj_db ...")
chkdb = checkConnection()
print(chkdb)
