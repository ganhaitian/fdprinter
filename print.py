__author__ = 'gan'
#coding=gb2312

import tempfile
import win32api
import win32print
import win32ui
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

#厨房出菜单打印数据对象
class BillDetailPrint:

    def __init__(self,printContent,font,spacing):
        self.printContent = printContent
        self.font = font
        self.spacing = spacing

    def getPrintContent(self):
        return self.printContent

    def getFont(self):
        return self.font

    def getSpacing(self):
        return self.spacing



#打印格式相关常量
FD_NAME = config.get('info','fd_name')
FD_NAME = "石山乳羊第一家"
TOTAL_WIDTH = config.getint('info','total_width')
TMP_FOLDER = config.get('info','tmp_folder')
scale_factor = config.getfloat('info','scale_factor')
line_interval_height = config.getint('info','line_interval_height')

DISH_TPL = open("dish.tpl","r").read()

X=0; Y=50

hDC = win32ui.CreateDC ()
hDC.CreatePrinterDC (win32print.GetDefaultPrinter())

#设置字体的样式及大小
font = win32ui.CreateFont({
    "name": "宋体",
    "height": int(10 * scale_factor),
    "weight": 400
})

#大号字体
big_font = win32ui.CreateFont({
    "name": "宋体",
    "height": int(13 * scale_factor),
    "weight": 400
})

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

if __name__=="__main__":
    while True:
        time.sleep(3)
        bills = mysqlutil.query(dbPool,"select * from bill where status = 0")

        if len(bills) == 0:
            print("There are no available bills.")

        for bill in bills:

            #filename = tempfile.mktemp (".txt","print_%d_%d_%s_" % (bill[0],bill[2],time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))),TMP_FOLDER)
            billDetails = mysqlutil.query(dbPool,"select * from bill_detail where bill_id  = %d " % bill[0])

            if bill[16] is None:
                billOperator = "微信用户"
            else:
                 billOperator = bill[16].encode("gb2312","ignore")

            billTableNo = bill[2].encode("gb2312","ignore")
            billPrintContent = []

            billPrintContent.append(FD_NAME.center(28,' ') + "\n")

            billPrintContent.append("%s%s\n" % ("(核对单)",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())).rjust(18)))
            billPrintContent.append("台号:%s%s%s" % (billTableNo,genblank(13),billOperator) + "\n");
            billPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")
            #billPrintContent.append("\n")

            for billDetail in billDetails:

                dishfilename =  tempfile.mktemp (".html","dish_%d_" % (billDetail[0]),TMP_FOLDER)

                dishName = billDetail[3].encode("gb2312","ignore")
                dishAmount = billDetail[4]
                dishPrice = billDetail[5]

                billDetailPrintContent = []

                Y = 0
                hDC.StartDoc("fd_detail receipe")
                hDC.StartPage()

                # hDC.SelectObject(font)
                # hDC.TextOut(X,Y,"小炒" + ("台号:%d" % billTableNo).rjust(23) + "\n")
                # Y += line_interval_height
                #
                # #billDetailPrintContent.append("小炒" + ("台号:%d" % billTableNo).rjust(17) + "\n")
                # billDetailPrintContent.append("出品单".center(22,' ') + "\n")
                # billDetailPrintContent.append(time.strftime('%H:%M:%S',time.localtime(time.time())).rjust(21) + "\n");
                # billDetailPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")
                # billDetailPrintContent.append("%d  %s   %.2f" % (dishAmount,dishName,dishPrice))
                # billDetailPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")

                billDetailPrintContent.append(BillDetailPrint("小炒" + ("台号:%s" % billTableNo).rjust(23) + "\n",font,50))
                billDetailPrintContent.append(BillDetailPrint("出品单".center(22,' ') + "\n",big_font,50))
                billDetailPrintContent.append(BillDetailPrint(time.strftime('%m.%d %H:%M:%S',time.localtime(time.time())).rjust(21) + "\n",font,50))
                billDetailPrintContent.append(BillDetailPrint("_".center(TOTAL_WIDTH,"_") + "\n",big_font,50))
                billDetailPrintContent.append(BillDetailPrint("%d  %s   %.2f" % (dishAmount,dishName,dishPrice),big_font,50))
                billDetailPrintContent.append(BillDetailPrint("_".center(TOTAL_WIDTH,"_") + "\n",big_font,50))


                #hDC.SelectObject(big_font)

                # #open(filename,'w').writelines(billPrintContent)
                for billDetailPrint in billDetailPrintContent:
                    hDC.SelectObject(billDetailPrint.getFont())
                    hDC.TextOut(X,Y,billDetailPrint.getPrintContent())
                    Y += billDetailPrint.getSpacing()

                hDC.EndPage ()
                hDC.EndDoc ()

                part1BlankLen = 10 - len(dishName) / 2 - len(("%d" % dishAmount)) / 2;
                part1Blank = ""
                for i in range(1,part1BlankLen):
                    part1Blank += "  ";

                part2BlankLen = 9 - len(('%.2f' % dishPrice))
                part2Blank = ""
                for i in range(1,part2BlankLen):
                    part2Blank += " ";

                billPrintContent.append("%s%s%d%s%.2f \n" % (dishName,part1Blank,dishAmount,part2Blank,dishPrice))

                dishPrintContent = DISH_TPL % (billTableNo,0,billOperator,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),dishAmount,dishName,dishPrice,billTableNo,billTableNo)

                #open(dishfilename,'w').write(dishPrintContent)
                #printfile(dishfilename)

            billPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")
            #billPrintContent.append("\n")

            billPrintContent.append("%s食品价" % genblank(11) + ("%.2f" % bill[4]).rjust(11) + "\n")
            billPrintContent.append("%s总价" % genblank(13) + ("%.2f" % bill[4]).rjust(11) + "\n")
            billPrintContent.append("_".center(TOTAL_WIDTH,"_") + "\n")

            billPrintContent.append("欢  迎  惠  顾  ".center(TOTAL_WIDTH) + "\n")
            billPrintContent.append("电话:0898-66989888".center(TOTAL_WIDTH))

            Y = 0
            hDC.SelectObject(font)
            hDC.StartDoc("fd receipe")
            hDC.StartPage()
            # #open(filename,'w').writelines(billPrintContent)
            for line in billPrintContent:
                hDC.TextOut(X,Y,line)
                Y += line_interval_height

            hDC.EndPage ()
            hDC.EndDoc ()

            #更新bill的状态为已打印
            mysqlutil.saveOrUpdate(dbPool,"update bill set status = 3 where id = %d " % bill[0])
            #printfile(filename)







