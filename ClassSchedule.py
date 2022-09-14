import datetime
from hashlib import md5

uid_generate = lambda key1, key2: md5(f"{key1}{key2}".encode("utf-8")).hexdigest()

def getclassesStr(path="./class.txt"):
    classesStr = []
    with open(path, 'r') as f:
        line = f.readline()
        while(line and line!="\n"):
            line = f.readline()
            classesStr.append(line)
        classesStr.pop()
    return classesStr

if __name__ == "__main__":
    classesStr = getclassesStr()
    
    iCal = """
BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:我的课表
X-WR-TIMEZONE:Asia/Shanghai
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
END:VTIMEZONE
    """
    
    
    
    firstDay = input("请输入第一周开始日期（2022/01/01）：\n")
    firstDay = [ int(i) for i in firstDay.split("/") ]
    firstDay = datetime.datetime( firstDay[0], firstDay[1], firstDay[2] )
    print()
    
    # classesStr = [] # 保存输入的内容，每一行表示一个课程
    # strLine = "1"
    # strLine = input("请输入课程，输入回车结束，格式为\n课程名 上课周数区间(用,隔开) 周几 开始时间-结束时间 课程位置\n课程A 1-2,4,6,9 2 09:00-15:20 A教学楼101室\n")
    # while(strLine != ""):
    #     # strLine = input("请输入课程，输入回车结束，格式为\n课程名 上课周数区间(用,隔开) 周几 开始时间-结束时间 课程位置\n课程A 1-2,4,6,9 2 14:00-15:20 A教学楼101室\n")
    #     classesStr.append(strLine)
    #     strLine = input()
    
    before = input("课程开始前多少分钟提醒（分钟）：")
    print()
    
    print("请检查输入内容")
    print("开始前{}分钟提醒".format(before))
    for t in classesStr:
        print(t)
    flag = input("y or n : ")
    if(flag=="n"):
        print("退出")
        exit()
    
    # 开始转换输入内容
    for strLine in classesStr:
        info = strLine.split(" ")
        infoName = { 
                    "title": info[0], 
                    "weeks": info[1], 
                    "day": info[2], 
                    "start-end": info[3], 
                    "location": info[4],
                    "discrption": ""
                    }
        
        # 备注
        if(len(info) > 5): infoName["discrption"] = info[5]
        
        # 上课时间
        startTime = infoName["start-end"].split("-")
        endTime = startTime[1].split(":")
        startTime = startTime[0].split(":")
        
        startHour, startMin = int(startTime[0]), int(startTime[1])
        endHour, endMin = int(endTime[0]), int(endTime[1])
        
        inWeeks = [] # 所有上课的周数
        weeks = infoName["weeks"].split(",")
        for week in weeks:
            week = week.split("-")
            if(len(week)==1): week = [int(week[0])]
            else: week = list(range( int(week[0]), int(week[1])+1 ))
            inWeeks = inWeeks + week
            
        # 计算上课时期
        for w in inWeeks:
            daysBias = 7*(w-1) + int(infoName["day"]) - 1 # 日期
            STARTTIME = (firstDay + datetime.timedelta(days=daysBias, hours=startHour, minutes=startMin)).strftime("%Y%m%dT%H%M%S")
            ENDTIME = (firstDay + datetime.timedelta(days=daysBias, hours=endHour, minutes=endMin)).strftime("%Y%m%dT%H%M%S")
            TITLE = infoName["title"]
            LOCATION = infoName["location"]
            DESCRPTION = infoName["discrption"]
            BEFORE = before # 多长时间前提醒（单位为分钟）
            
            singleEvent = f"""
BEGIN:VEVENT
DTEND;TZID=Asia/Shanghai:{ENDTIME}
DESCRIPTION:{DESCRPTION}
UID:{uid_generate(TITLE, STARTTIME)}
URL;VALUE=URI:
SUMMARY:{TITLE} - {LOCATION}
DTSTART;TZID=Asia/Shanghai:{STARTTIME}
BEGIN:VALARM
UID:{uid_generate(TITLE, ENDTIME)}
TRIGGER:-PT{BEFORE}M
ATTACH;VALUE=URI:Chord
ACTION:AUDIO
END:VALARM
END:VEVENT
"""
            
            
            iCal += singleEvent
            
    iCal += "END:VCALENDAR"
    
    with open("class.ics", "w", encoding = "utf-8") as w:
	    w.write(iCal)
            
        
    