from setuptools import setup, find_packages
from pkg_resources import Requirement, resource_filename
import sys, os, shutil

PATH = "/etc/sire/"
DB = PATH + "db.sqlite"
CONF = PATH + "sire.conf"
SAMPLE = resource_filename(Requirement.parse("sire"), "share/sire.conf.sample")
MODE = 0660

def fperm(fname, mode = MODE):
    st = os.stat(SAMPLE)
    os.chown(fname, st.st_uid, st.st_gid)
    os.chmod(fname, mode)
    return

def print_info(string):
    print "\033[32m\033[1m" + string + "\033[0m"
    return

def print_error(string):
    print "\033[31m\033[1m" + string + "\033[0m"
    return

def copy_config():
    print
    print_info("* Trying to copy sample config file to '%s'." % CONF)
    try:
        if not os.path.exists(PATH):
            print "  * '%s' does not exists, creating it." % PATH
            os.mkdir(PATH)
            print "  * Setting permissions on '%s' to the same as the sample configuration." % PATH
            fperm(PATH, 0770)
        else:
            print "  * Directory '%s' already exists, not creating it." % PATH

        if not os.path.exists(CONF):
            print "  * Copying sample configuration to '%s'." % CONF
            shutil.copyfile(SAMPLE, CONF)
            print "  * Setting permissions on the config file to the same as the sample configuration."
            fperm(CONF)
        else:
            print "  * Config file already exists, not copying."
    except IOError:
        print_error("* Either unable to copy configuration file to '%s' or set it's permissions." % CONF)
    return

def create_database():
    print
    from pysqlite2 import dbapi2 as sqlite3

    print_info("* Trying to create sqlite database at '%s'." % DB)
    if os.path.exists(DB):
        print "  * Database exists, not creating."
        return
    print "  * Database does not exists, creating it."
    con = sqlite3.connect(DB)
    c = con.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS item(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
            title VARCHAR NOT NULL, 
            date VARCHAR DEFAULT (strftime('%s')),
            cat VARCHAR NOT NULL, 
            score INTEGER DEFAULT 0)
        """
    print "  * Going to execute the following query:\n" + query
    c.execute(query)
    con.commit()
    c.close()

    print "  * Setting permissions on the database file to the same as the sample configuration."
    fperm(DB)
    return


version = '0.3.0'

setup(name='sire',
    version=version,
    description="Simple Reminder",
    long_description="""\
""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='lists',
    author='Oscar Eriksson',
    author_email='oscar.eriks@gmail.com',
    url='sire.eldslott.org',
    license='GPLv3',
    package_data={'': ['sire.conf']},
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'mysql-python',
        'pysqlite>=2.6.0',
    ],
    entry_points={
        'console_scripts': [
            'sire = sire:entrypoint',
        ],
    }
)

copy_config()
create_database()
