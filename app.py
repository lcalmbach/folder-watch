import pandas
from datetime import datetime
import logging
import os.path, time

import db
import const as cn

__author__ = 'lukas calmbach'
__author_email__ = 'lukas.calmbach@bs.ch'
__version__ = '0.0.1'
LOGGING_LEVEL = logging.INFO
logger = {}
my_name = 'folder-watch'

SQL_CMD = """
EXEC msdb.dbo.sp_send_dbmail 
@profile_name    = 'default', 
@recipients = '{}',
@subject         = 'folder-watch',
@body            = '{}',
@body_format     = 'HTML' 
"""

def get_fileno_diff_info(orig, new):
    """
    returns weather number of files has changed between 2 dict of files.
    """
    result = ''
    if len(orig) > len(new): # files were deleted
        result = 'deleted files: '
        for x in orig:
            if not x in new:
                result += f'{x}<br>'
    else:
        result = 'new files: '
        for x in new:
            if not x in orig:
                result += f'{x}<br>'
    logger.debug('Anzahl Files Differenzen Info erstellt')
    return result

def get_file_creation_time_diff_info(orig, new):
    """
    returns wether timestamps have changed between 2 dict of files.
    """
    msg = ''
    diffs = 0
    for x in orig:
        try:
            if orig[x] != new[x]:
                msg += f"{x} ts changed from: {time.ctime(orig[x])} to {time.ctime(new[x])}<br>"
                diffs += 1
        except Exception as ex:
            logger.warning(tools.error_message(ex))
    logger.debug('Creation Dates Differenzen Info erstellt')        
    return diffs, msg

def get_files_dic(files)->dict:
    """
    übernimmt eine Liste von Filenamen und erstellt ein dict, wobei jeder Eintrag
    filename: creation_time
    """

    files_dic = {}
    try:
        for f in files:
            files_dic[f] = os.path.getmtime(os.path.join(cn.PATH, f))
    except Exception as ex:
            logger.warning(tools.error_message(ex))
    
    logger.debug(f'File dict erstellt:{files_dic}')
    return files_dic

def check_files(file_dic):
    msg = ''
    has_changes = False
    curr_files_dic = get_files_dic(os.listdir(cn.PATH))

    has_changes = len(file_dic) != len(curr_files_dic)
    if has_changes:
        msg = get_fileno_diff_info(file_dic, curr_files_dic)
    else:
        diffs, msg = get_file_creation_time_diff_info(file_dic, curr_files_dic)
        has_changes = diffs > 0

    logger.debug('Files überprüft nach Differenzen')
    return has_changes, curr_files_dic, msg

def main():
    conn = db.get_connection(srv=cn.SERVER, db_name=cn.DATABASE)
    info = f"Du wirst über Änderungen in Dateien des Verzeichnis zeitnah informiert (Intervall={cn.INTERVAL}s)"
    msg = f"folder-watch gestartet: {cn.PATH}<br>{info}"
    cmd = SQL_CMD.format(cn.VERTEILER, msg) #first 500 chars
    db.exec_non_query(conn,cmd)
    files_dic = get_files_dic(os.listdir(cn.PATH))
    
    while True:
        has_changes, curr_files_dic, msg = check_files(files_dic)
        if has_changes:
            logger.INFO(msg)
            cmd = SQL_CMD.format(cn.VERTEILER, msg[:500]) #first 500 chars
            db.exec_non_query(conn,cmd)
            files_dic = curr_files_dic
        else:
            logger.debug('Files überprüft')
        time.sleep(cn.INTERVAL)

def init_logger():
    """
    Initialisiert das Logger Objekt
    """
    global logger

    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M")
    file_handler = logging.FileHandler(f"{my_name}.log", "a", encoding = "UTF-8")
    file_handler.setFormatter(formatter)
    logger = logging.getLogger(f'{my_name}-logger')
    logger.addHandler(file_handler)
    logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    init_logger()
    logger.info(f"Folder-Watch-Prozess gestartet, Verzeichnis ist: {cn.PATH}, Verteiler: {cn.VERTEILER}, Intervall: {cn.INTERVAL}")
    logger.debug(f"Dateien: {os.listdir(cn.PATH)}")
    main()


