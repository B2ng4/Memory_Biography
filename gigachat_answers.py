import config
from gigachat import GigaChat

def answer1(text: str):
    giga = GigaChat(credentials="NmQ1OTVhZTEtNmQ5Yy00ZmNlLWJkNWMtMTAxYmY4MTU3MWJmOmE2OWRjOGNjLTllYjktNGM1Yi1iM2UyLWY5NDcyNTIyNjQxNg==", verify_ssl_certs=False, model="GigaChat-Pro")
    response = giga.chat(f"{text } ->  Выдумай  биографию этого человека исходя из этого набора ответов  ")
    return response.choices[0].message.content


def answer2(text1: str,text2:str):
    giga = GigaChat(credentials="NmQ1OTVhZTEtNmQ5Yy00ZmNlLWJkNWMtMTAxYmY4MTU3MWJmOmE2OWRjOGNjLTllYjktNGM1Yi1iM2UyLWY5NDcyNTIyNjQxNg==", verify_ssl_certs=False, model="GigaChat-Pro")
    response = giga.chat(f"Объедини эти два текста: {text1} и {text2} в связную и обширную биографию этого человека. (примерно 300 слов)")
    return response.choices[0].message.content


def answer3(text1: str):
    giga = GigaChat(credentials="NmQ1OTVhZTEtNmQ5Yy00ZmNlLWJkNWMtMTAxYmY4MTU3MWJmOmE2OWRjOGNjLTllYjktNGM1Yi1iM2UyLWY5NDcyNTIyNjQxNg==", verify_ssl_certs=False, model="GigaChat-Pro")
    response = giga.chat(f"{text1}/Измени текст, перефразируй, что-то добавь, что-то удали, но текст должен быть другим")
    return response.choices[0].message.content

def answer4(text1: str):
    giga = GigaChat(credentials="Y2Q3MDIzMGItZDY3OS00MjcwLWI1NWEtMGExNTMyMDUzYTAwOjY2YjBiZWM4LTAwOTEtNDEyZi04YWJlLTY3NmU1NTNiNTA5Ng==", verify_ssl_certs=False)
    response = giga.chat(f"{text1}/Напиши эпитафию, стихотворное изречение. Строго краткое и в рифму. Строго 1 строфа. (1 четверостишье). Ничего лишнего, буквально 30-40 слов")
    return response.choices[0].message.content