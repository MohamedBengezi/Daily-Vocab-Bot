import sys
import json
from time import sleep
from selenium import webdriver

URL = 'https://dailyvocab.ca/vocab/838/quiz'
terms = {}
question = None


def setup_dict():
    global terms
    try:
        with open("terms.txt") as f:

            for line in f:
                (key, val) = line.split("\t")
                if key not in terms:
                    terms[key] = val
    except:
        print('Reached end of terms file')


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
        setAnswer("idk")


def setAnswer(ans):
    answer = driver.find_element_by_id("question_answer")
    # check for exact match, and if not get closest
    if terms.has_key(question):
        ans = terms[question]
    else:
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
    while count < 50:
        getQuestion()
        setAnswer(None)
        sleep(2)
        count += 1
