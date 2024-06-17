import requests
import re
from bs4 import BeautifulSoup
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
        return None

# 提取网页内容
def parseHTMLText(htmlText, problem_url):
    try:
        soup = BeautifulSoup(htmlText, 'html.parser')
        pNumber = re.findall(r'[\d]{4}', str(soup.title.string))[0]
        pTitle = str(soup.h1.string)
        set_pOutput = soup.find_all('div', 'panel_content')
        pContent = set_pOutput[0].text
        pInput = set_pOutput[1].text
        pOutput = set_pOutput[2].text
        pSampleInput = set_pOutput[3].text
        pSampleOutput = set_pOutput[4].text

        infoDict = {
            "problem_id": pNumber,
            "problem_name": pTitle,
            "problem_content": pContent,
            "problem_input": pInput,
            "problem_output": pOutput,
            "problem_sample_input": pSampleInput,
            "problem_sample_output": pSampleOutput,
            "problem_url": problem_url
        }

        return infoDict
    except:
        print("Error occurred when parsing HTML content!")
        return None

# 将爬取到的数据存储到MySQL数据库中
def db_dataMemory(pInfoDict, tableName='app_problemset'):
    try:
        txtNumber = int(pInfoDict['problem_id'])
        escapeTitle = pInfoDict['problem_name'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeContent = pInfoDict['problem_content'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        # escapeInput = pInfoDict['problem_input'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        # escapeOutput = pInfoDict['problem_output'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        # escapeSampleInut = pInfoDict['problem_sample_input'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        # escapeSampleOnut = pInfoDict['problem_sample_output'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        escapeUrl = pInfoDict['problem_url'].replace("'", "\\'").replace("\\\\'", "\\\\\\'")
        # print(txtNumber, escapeTitle, escapeContent, escapeUrl)
        sql_insertData = f"""
            INSERT INTO {tableName} (`index`, `title`, `content`, `url`)
            VALUES ({txtNumber}, '{escapeTitle}', '{escapeContent}', '{escapeUrl}')
        """

        cursor.execute(sql_insertData)
        connection.commit()
        print(f"题目序号为 {txtNumber} 的题目已存储成功")
    except:
        print("Error occurred when storing data in the database!")

def main():
    start_url = "http://acm.hdu.edu.cn/showproblem.php?pid="
    realAmount = 0
    # id -> [1000, 7423]
    problem_id_begin = 1000
    problem_id_end = 1099
    request_max_times = 10
    for offset in range(problem_id_begin, problem_id_end + 1):
        retry_times = 1
        while retry_times <= request_max_times:
            url = start_url + str(offset)
            htmlText = getHTMLText(url)
            pInfoDict = parseHTMLText(htmlText, url)
            if pInfoDict is not None:
                # print(f"Tried {retry_times} times, get " + str(pInfoDict))
                db_dataMemory(pInfoDict)
                realAmount += 1
                break
            retry_times += 1
        else:
            print("Request out!")

    print("--*---*---*---*---*--")
    print(f"实际上一共有 {realAmount} 道习题")

if __name__ == '__main__':
    # tableName = 'HDU'

    # 创建数据库表
    # sql_createTable = f"""
    #     CREATE TABLE {tableName}(
    #         pNumber INTEGER PRIMARY KEY,
    #         pTitle VARCHAR(100),
    #         pContent TEXT,
    #         pInput TEXT,
    #         pOutput TEXT,
    #         pSampleInput TEXT,
    #         pSampleOutput TEXT,
    #         pUrl TEXT
    #     )
    # """
    #
    # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='ProblemSet', charset='utf8mb4')
    # cursor = conn.cursor()
    # cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
    # cursor.execute(sql_createTable)
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