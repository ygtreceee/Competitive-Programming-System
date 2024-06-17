import requests
from bs4 import BeautifulSoup
import datetime
import pymysql

def DEBUG(FileName, Content):
    with open(FileName, 'w') as file:
        file.write(Content)


# 请求网页内容
def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error occurred when getting HTML content!")


# 提取比赛信息
def parseHTMLText_contest_id(htmlText):
    try:
        soup = BeautifulSoup(htmlText, 'html.parser')
        # DEBUG('DEBUG_cf_content_soup.txt', str(soup))

        contest_ids = [tr['data-contestid'] for tr in soup.select('tr[data-contestid]')]
        print(contest_ids)

        return contest_ids
    except:
        print("Error occurred when parsing HTML content - id!")


# 提取指定比赛中的题目信息
def parseHTMLText_contest(htmlText, contest_id, contest_url):
    try:
        soup = BeautifulSoup(htmlText, 'html.parser')

        # 信息总集合
        infoset = soup.find_all('td')

        # 提取比赛名称
        contest_name = infoset[0].text.strip()
        contest_name = contest_name[:contest_name.index(')') + 1]
        # print("比赛名称:", contest_name)

        # 提取作者名字
        contest_writers = infoset[1].text.strip()
        # print("作者:", contest_writers)

        # 提取比赛时间
        start_time_origin = infoset[2].text.strip()
        datetime_obj = datetime.datetime.strptime(start_time_origin, '%b/%d/%Y %H:%M')
        updated_datetime = datetime_obj + datetime.timedelta(hours=4, minutes=50)
        start_time = updated_datetime.strftime('%b/%d/%Y %H:%M')
        # print("比赛时间:", start_time)

        # 提取比赛时长
        length = infoset[3].text.strip()
        # print("比赛时长:", length)

        infoDict = {
            "contest_id": contest_id,
            "contest_name": contest_name,
            "contest_writers": contest_writers, # 每个作者以 '\' 隔开
            "contest_start_time": start_time,
            "contest_length": length,
            "contest_url": contest_url
        }
        return infoDict
    except:
        print("Error occurred when parsing HTML content!")


# 将爬取到的数据存储到MySQL数据库中
def db_dataMemory(pInfoDict, tableName='app_codeforcescontestinfo'):
    try:
        txtNumber = int(pInfoDict['contest_id'])
        escapeTitle = pInfoDict['contest_name'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        # escapeWriters = pInfoDict['contest_writers'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeStartTime = pInfoDict['contest_start_time'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeLength = pInfoDict['contest_length'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeUrl = pInfoDict['contest_url'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")

        sql_insertData = f"""
            INSERT INTO {tableName} (`contest_id`, `name`, `start_time`, `length`, `url`)
            VALUES ({txtNumber}, '{escapeTitle}', '{escapeStartTime}', '{escapeLength}', '{escapeUrl}')
        """

        cursor.execute(sql_insertData)
        connection.commit()
        print(f"序号为 {txtNumber} 的比赛已存储成功")
    except:
        print("Error occurred when storing data in the database!")

def main():
    # 注意：开启vpn可大幅加速爬取速度
    contest_url = "https://codeforces.com/contests?complete=true"
    start_url = "https://codeforces.com/contests/"

    # 提取最近比赛信息
    htmlText_content = getHTMLText(contest_url)
    contest_ids = parseHTMLText_contest_id(htmlText_content)

    realAmount = 0
    maxAmount = 20 # 爬取最近的共 maxAmount 场比赛
    request_max_times = 2
    for contest_id in contest_ids:
        retry_times = 1
        if realAmount >= maxAmount:
            break
        while retry_times <= request_max_times:
            url = start_url + str(contest_id)
            htmlText = getHTMLText(url)
            cInfoDict = parseHTMLText_contest(htmlText, contest_id, url)
            if cInfoDict is not None:
                print(f"Tried {retry_times} times, get " + str(cInfoDict))
                db_dataMemory(cInfoDict)
                realAmount += 1
                break
            retry_times += 1
        else:
            print("Request out!")

    print("--*---*---*---*---*--")
    print(f"爬取得共 {realAmount} 场比赛")

if __name__ == '__main__':
    # tableName = 'Codeforces'

    # 创建数据库表
    # sql_createTable = f"""
    #         CREATE TABLE {tableName}(
    #             contest_id INTEGER PRIMARY KEY,
    #             contest_name VARCHAR(100),
    #             contest_writers TEXT,
    #             contest_start_time TEXT,
    #             contest_length TEXT,
    #             contest_url TEXT
    #         )
    #     """

    connection = pymysql.connect(
        host='localhost',  # 数据库主机名
        user='root',  # 用户名
        password='12345678',  # 密码
        database='ProblemSetSystem'  # 数据库名称
    )
    cursor = connection.cursor()
    # conn.commit()

    main()

    cursor.close()
    connection.close()