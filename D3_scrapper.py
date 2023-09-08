from datetime import datetime, timezone
import smtplib, ssl
import requests
import os
import psycopg2

conn = psycopg2.connect(
        host="psql-service",
        database="flask_db",
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))
cur = conn.cursor()
cur.execute('SELECT * FROM currency;')
db_result = cur.fetchall()

#get exchange rate from api

date = datetime.now(timezone.utc)
utct=date.replace(tzinfo=timezone.utc)
utctimes=utct.timestamp()

for data in db_result:
    curr=data[1]
    lastcurr=data[2]
    id=data[0]
    response = requests.get("https://api.exchangerate.host/latest?base="+curr+"&symbols=USD")
    res= response.json()
    res = res['rates']['USD']
    if lastcurr != res:
                
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "atharsiddiqui12345@gmail.com"
        receiver_email = ['atharshah9305@gmail.com','info@pivony.com']
        to = ", ".join(receiver_email)
        password = os.environ.get('EMAIL_PASS')
        message = """\
        Subject: Hi there

        The USD rates of """+curr+ "changes to "+str(res)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, to, message)

    try:
         cur.execute("UPDATE currency SET usd_ex= %s, timestamp = %s WHERE id= %s;",(res, utctimes, id))
         conn.commit()
         cur.close()
         conn.close()

    except psycopg2.InterfaceError as e:
         conn= psycopg2.connect(
                host="psql-service",
                database="flask_db",
                user=os.environ.get('DB_USERNAME'),
                password=os.environ.get('DB_PASSWORD'))
         cur = conn.cursor()
         cur.execute("UPDATE currency SET usd_ex= %s, timestamp = %s WHERE id= %s;",(res, utctimes, id))
         conn.commit()
         cur.close()
         conn.close()
         