__author__ = 'gan'
#coding=UTF-8

import tempfile
import win32api
import win32print
import mysqlutil
import sched,time
import ConfigParser

config=ConfigParser.ConfigParser()
with open("config.properties","r") as cfgfile:
    config.readfp(cfgfile)

dbPool = mysqlutil.initDBPool(
    config.get('db','db_user'),
    config.get('db','db_passwd'),
    config.get('db','db_ip'),
    config.getint('db','db_port'),
    config.get('db','db_name')
);

#打印格式相关常量
FD_NAME = config.get('info','fd_name')
TOTAL_WIDTH = config.getint('info','total_width')
TMP_FOLDER = config.get('info','tmp_folder')

DISH_TPL = open("dish.tpl","r").read()

def genblank(blankNum):
    _nblank = ""
    for i in range(1,blankNum):
        _nblank += " "
    return _nblank

def printfile(filename):
    win32api.ShellExecute (
        0,
        "print",
        filename,
        # If this is None, the default printer will
        # be used anyway.
        #
        '/d:"%s"' % win32print.GetDefaultPrinter (),
        ".",
        0
    )

    win32print.

if __name__=="__main__":
    while True:
        bills = mysqlutil.query(dbPool,"select * from bill where status = 0")

        if len(bills) == 0:
            print("There are no available bills.")

        for bill in bills:
            filename = tempfile.mktemp (".txt","print_%d_%d_%s_" % (bill[0],bill[2],time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))),TMP_FOLDER)
            billDetails = mysqlutil.query(dbPool,"select * from bill_detail where bill_id  = %d " % bill[0])

            billOperator = bill[16].encode("utf-8","ignore")
            billPrintContent = []

            billPrintContent.append(FD_NAME.center(42,' ') + "\n")

            billPrintContent.append("%s%s\n" % ("(核对单)",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())).rjust(26)))
            billPrintContent.append("台号:%d" % bill[2] + "\n");
            billPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")
            billPrintContent.append("\n")

            for billDetail in billDetails:

                dishfilename =  tempfile.mktemp (".html","dish_%d_" % (billDetail[0]),TMP_FOLDER)


                dishName = billDetail[3].encode("utf-8","ignore")
                dishAmount = billDetail[4]
                dishPrice = billDetail[5]

                part1BlankLen = 12 - len(dishName) / 3 - len(("%d" % dishAmount)) / 2;
                part1Blank = ""
                for i in range(1,part1BlankLen):
                    part1Blank += "  ";

                part2BlankLen = 12 - len(('%.2f' % dishPrice))
                part2Blank = ""
                for i in range(1,part2BlankLen):
                    part2Blank += " ";

                billPrintContent.append("%s%s%d%s%.2f \n" % (dishName,part1Blank,dishAmount,part2Blank,dishPrice))

                dishPrintContent = DISH_TPL % (bill[2],0,billOperator,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),dishAmount,dishName,dishPrice,bill[2],bill[2])

                open(dishfilename,'w').write(dishPrintContent)
                #printfile(dishfilename)

            billPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")
            billPrintContent.append("\n")

            billPrintContent.append("%s食品价" % genblank(16) + ("%.2f" % bill[4]).rjust(13) + "\n")
            billPrintContent.append("%s总价" % genblank(18) + ("%.2f" % bill[4]).rjust(13) + "\n")
            billPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")

            billPrintContent.append("欢  迎  惠  顾  ".center(TOTAL_WIDTH) + "\n")
            billPrintContent.append("电话:0898-66989888".center(TOTAL_WIDTH))

            open(filename,'w').writelines(billPrintContent)

            #更新bill的状态为已打印
            mysqlutil.saveOrUpdate(dbPool,"update bill set status = 3 where id = %d " % bill[0])
            #printfile(filename)


        time.sleep(1)





