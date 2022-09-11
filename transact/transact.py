import pika, sys, os
import psycopg2
import json

con = psycopg2.connect(
    database="tranzaction",
    user="postgres",
    password="741852963",
    host="127.0.0.1",
    port="5432"
)

rmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rmq_channel = rmq_connection.channel()

def read():
    rmq_channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print(body.decode('utf-8'))
        dict_data = json.loads(body)
        print(dict_data)
        print(type(dict_data))

        #вытаскиваем текущие балансы людей
        cur = con.cursor()
        cur.execute("SELECT id, username, balance FROM public.pay WHERE id = %s",
                    [int(dict_data['id'])])
        raw1 = cur.fetchone()
        print(raw1)


        cur2 = con.cursor()
        cur2.execute("SELECT id, username, balance FROM public.pay WHERE id = %s",
                    [int(dict_data['id_to'])])
        raw2 = cur2.fetchone()


        #считаем какими они должны стать
        new_balance1 = raw1[-1] - float(dict_data['amount'])
        new_balance2 = raw2[-1] + float(dict_data['amount'])

        #делаем update
        cur = con.cursor()
        cur.execute(
            "UPDATE public.pay SET balance=%s WHERE id = %s;",
            [new_balance1, dict_data['id']]
        )
        cur.execute(
            "UPDATE public.pay SET balance=%s WHERE id = %s;",
            [new_balance2, dict_data['id_to']]
        )
        cur.execute(
            "INSERT INTO public.history(id_from, id_to, amount) VALUES (%s, %s, %s);",
            [dict_data['id'], dict_data['id_to'], dict_data['amount']]
        )


        con.commit()
        print("Records inserted successfully")





    rmq_channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    rmq_channel.start_consuming()


if __name__ == '__main__':
    try:
        read()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)