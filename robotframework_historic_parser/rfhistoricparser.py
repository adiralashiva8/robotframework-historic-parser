import os
import mysql.connector
import logging
from robot.api import ExecutionResult, ResultVisitor
import datetime
from datetime import timedelta

def generate_report(opts):

    path = os.path.abspath(os.path.expanduser(opts.path))

    # output.xml files
    output_names = []
    # support "*.xml" of output files
    if ( opts.output == "*.xml" ):
        for item in os.listdir(path): 
            if os.path.isfile(item) and item.endswith('.xml'):
                output_names.append(item)
    else:
        for curr_name in opts.output.split(","):
            curr_path = os.path.join(path, curr_name)
            output_names.append(curr_path)
    
    required_files = list(output_names) 
    missing_files = [filename for filename in required_files if not os.path.exists(filename)]
    if missing_files:
        # We have files missing.
        exit("output.xml file is missing: {}".format(", ".join(missing_files)))
    
    # Read output.xml file
    result = ExecutionResult(*output_names)
    result.configure(stat_config={'suite_stat_level': 2,
                                  'tag_stat_combine': 'tagANDanother'})

    logging.info("Capturing execution results, This may take few minutes...")

    # connect to database
    mydb = connect_to_mysql_db(opts.host, opts.username, opts.password, opts.projectname)
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stats = result.statistics
    total = stats.total.all.total
    passed = stats.total.all.passed
    failed = stats.total.all.failed

    elapsedtime = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=result.suite.elapsedtime)
    elapsedtime = get_min(elapsedtime.strftime("%X"))

    # insert test results info into db
    result_id = insert_into_results_mysql_table(mydb, date_now, opts.executionname, total, passed, failed, elapsedtime)
    
    logging.info("INFO: Capturing test cases results, This may take few minutes...")
    result.visit(TestMetrics(mydb, result_id))

    logging.info("INFO: Writing execution results")
    commit_and_close_db(mydb)

# other useful methods

class TestMetrics(ResultVisitor):

    def __init__(self, db, id):
        self.db = db
        self.id = id

    def visit_test(self, test):
        name = str(test.parent) + " - " + str(test)
        time = str(test.elapsedtime / float(60000))
        error = str(test.message)
        insert_into_test_results_mysql_table(self.db, self.id, str(name), str(test.status), time, error)

def get_current_date_time(format,trim):
    t = datetime.datetime.now()
    if t.microsecond % 1000 >= 500:  # check if there will be rounding up
        t = t + datetime.timedelta(milliseconds=1)  # manually round up
    if trim:
        return t.strftime(format)[:-3]
    else:
        return t.strftime(format)

def get_min(time_str):
    h, m, s = time_str.split(':')
    ctime = int(h) * 3600 + int(m) * 60 + int(s)
    crtime = "%.2f" % (ctime/60)
    return crtime

def connect_to_mysql_db(host, user, pwd, db):
    try: 
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception:
        print(Exception)

def insert_into_results_mysql_table(con, cdate, name, total, passed, failed, ctime):
    cursorObj = con.cursor()
    sql = "INSERT INTO results (ID, DATE, NAME, TOTAL, PASSED, FAILED, TIME) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (0, cdate, name, total, passed, failed, ctime)
    cursorObj.execute(sql, val)
    con.commit()
    cursorObj.execute("select count(*) from results")
    rows = cursorObj.fetchone()
    return str(rows[0])

def insert_into_test_results_mysql_table(con, eid, test, status, duration, msg):
    cursorObj = con.cursor()
    sql = "INSERT INTO test_results (ID, UID, TESTCASE, STATUS, TIME, MESSAGE) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (eid, 0, test, status, duration, msg)
    cursorObj.execute(sql, val)
    # Skip commit to avoid load on db (commit once execution is done as part of close)
    # con.commit()

def commit_and_close_db(db):
    cursorObj = db.cursor()
    db.commit()
    # cursorObj.close()
    # db.close()