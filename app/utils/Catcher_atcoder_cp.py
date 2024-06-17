import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
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
def parseHTMLText_contest_foreach(htmlText):
    try:
        soup = BeautifulSoup(htmlText, 'html.parser')
        # DEBUG('DEBUG_atcoder_content_soup.txt', str(soup))

        tr_elements = soup.find_all('tr')

        # contest -> tr_elements [4]~[14] [16]~[25]
        tr_elements = tr_elements[4:15] + tr_elements[16:26]

        # print(len(tr_elements))

        return tr_elements
    except:
        print("Error occurred when parsing HTML content - id!")


# 提取指定比赛中的题目信息
def parseHTMLText_contest(htmlText):
    try:
        soup = BeautifulSoup(htmlText, 'html.parser')

        # 提取时间部分
        time_element = soup.find('time', class_='fixtime fixtime-short')
        time_text = time_element.text  # 原始时间文本

        # 解析时间并添加时差
        time_format = "%Y-%m-%d %H:%M:%S%z"
        time = datetime.strptime(time_text, time_format) + timedelta(hours=-1)
        formatted_time = time.strftime(time_format)
        start_time = formatted_time.split('+')[0]

        # 提取后缀链接部分
        link_element = soup.find_all('a', href=True)[-1]
        contest_url = link_element['href']
        contest_url = start_url + contest_url

        # 提取比赛名称部分
        name_element = soup.find_all('a')[-1]
        contest_name = name_element.text

        # 提取比赛编号部分
        contest_id = contest_url.split('/')[-1]

        # print("时间部分（已计入时差）:", start_time)
        # print("后缀链接部分:", contest_url)
        # print("比赛名称部分:", contest_name)
        # print("比赛编号部分:", contest_id)
        # print("")

        infoDict = {
            "contest_id": contest_id,
            "contest_name": contest_name,
            "contest_start_time": start_time,
            "contest_url": contest_url
        }
        return infoDict
    except:
        print("Error occurred when parsing HTML content! - ?")


# 将爬取到的数据存储到MySQL数据库中
def db_dataMemory(pInfoDict, tableName='app_atcodercontestinfo'):
    try:
        txtNumber = pInfoDict['contest_id'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeTitle = pInfoDict['contest_name'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeStartTime = pInfoDict['contest_start_time'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeUrl = pInfoDict['contest_url'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")

        sql_insertData = f"""
            INSERT INTO {tableName}(`contest_id`, `name`, `start_time`, `url`)
            VALUES ('{txtNumber}', '{escapeTitle}', '{escapeStartTime}', '{escapeUrl}')
        """

        cursor.execute(sql_insertData)
        connection.commit()
        print(f"序号为 {txtNumber} 的比赛已存储成功")
    except:
        print("Error occurred when storing data in the database!")


def main():
    global start_url
    start_url = "https://atcoder.jp"

    # 提取最近比赛信息
    htmlText_content = getHTMLText(start_url)
    htmlText_content_set = parseHTMLText_contest_foreach(htmlText_content)

    realAmount = 0
    maxAmount = 30 # 爬取最近的共 maxAmount 场比赛
    request_max_times = 2

    for htmlText in htmlText_content_set:
        retry_times = 1
        if realAmount >= maxAmount:
            break
        while retry_times <= request_max_times:
            complete_html = f'''
                    <!DOCTYPE html>
                    <html>
                    <head>
                      <title>HTML Code Example</title>
                    </head>
                    <body>
                      <table>
                        {htmlText}
                      </table>
                    </body>
                    </html>
                    '''
            cInfoDict = parseHTMLText_contest(complete_html)
            if cInfoDict is not None:
                print(f"Tried {retry_times} times, get " + str(cInfoDict))
                db_dataMemory(cInfoDict)
                # print(cInfoDict)
                realAmount += 1
                break
            retry_times += 1
        else:
            print("Request out!")

    print("--*---*---*---*---*--")
    print(f"爬取得共 {realAmount} 场比赛")

if __name__ == '__main__':
    # tableName = 'Atcoder'

    # 创建数据库表
    # sql_createTable = f"""
    #             CREATE TABLE {tableName}(
    #                 contest_id VARCHAR(20) PRIMARY KEY,
    #                 contest_name VARCHAR(100),
    #                 contest_start_time TEXT,
    #                 contest_url TEXT
    #             )
    #         """

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