import sys
import json
from time import sleep
from selenium import webdriver

URL = 'https://dailyvocab.ca/vocab/838/quiz'


def setup_dict():
    global terms
    terms = {}
    cnt = 0
    try:
        with open("terms.txt") as f:

            for line in f:
                cnt += 1
                print cnt
                (key, val) = line.split("\t")
                if key not in terms:
                    terms[key] = val
    except:
        print('Reached end of terms file')
    for i in terms:
        cnt += 1


def login():
    with open('info.json') as f:
        data = json.load(f)
    email = driver.find_element_by_id("person_email")
    email.send_keys(data['email'])

    passw = driver.find_element_by_id("person_password")
    passw.send_keys(data['pass'])

    cont = driver.find_element_by_name("commit")
    cont.send_keys(webdriver.common.keys.Keys.RETURN)


def getQuestion():
    global question
    if "question" in globals():
        prevQ = question
    else:
        prevQ = None
    question = driver.find_element_by_id("question_prompt").text
    if question[-1] == '-':
        question = question.replace('-', '')
    if question == prevQ:
        raise Exception("Wrong Answer")


def setAnswer():
    answer = driver.find_element_by_id("question_answer")
    ans = [value for key, value in terms.items() if question.lower()
           in key.lower()]
    answer.send_keys(ans)
    answer.send_keys(webdriver.common.keys.Keys.RETURN)


if __name__ == '__main__':
    setup_dict()
    # setting the site and driver
    driver = webdriver.Firefox()
    # load the site
    driver.get(URL)
    login()
    sleep(1)
    count = 0
    while count < 25:
        getQuestion()
        setAnswer()
        sleep(2)
        count += 1
