from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db import connection
import pika
import json
from .serializers import Serializers_data, Serializers_history


rmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rmq_channel = rmq_connection.channel()


class Transact(APIView):
    def post(self, request):
        tranzact_data = Serializers_data(data=request.data)
        if tranzact_data.is_valid():
            if tranzact_data.data['amount'] <= 0:
                return HttpResponse('transfer to a negative amount of money is not possible')
            with connection.cursor() as cursor1:
                cursor1.execute(
                    'SELECT * FROM public.pay WHERE id = %s;',
                    [str(tranzact_data.data['id'])])
                raw = cursor1.fetchone()
                print(raw)

            if raw[-1] - float(tranzact_data.data['amount']) >= 0:
                print('перевод возможен')
                data_json = json.dumps(tranzact_data.data)
                rmq_channel.queue_declare(queue='hello')
                rmq_channel.basic_publish(exchange='',
                routing_key = 'hello', body = data_json)
            else:
                return HttpResponse('Недостаточно средств для перевода')

            return HttpResponse('Транзакция принята!')
        else:
            return HttpResponse(tranzact_data.errors)


class ShowBalance(APIView):
    def post(self, request):
        data = request.data
        with connection.cursor() as cursor1:
            cursor1.execute(
                'SELECT * FROM public.pay WHERE id = %s;',
                [data['id']])
            raw = cursor1.fetchone()
            print(raw)
            if raw != None:
                return HttpResponse('{}, Ваш баланс = {}'.format(raw[1], raw[-1]))
            else:
                HttpResponse('error')


class HistorySuccesfullTransact(APIView):
    def post(self, request):
        data = request.data
        resp = []
        with connection.cursor() as cursor1:
            cursor1.execute(
                'SELECT * FROM public.history WHERE id_to = %s or id_from = %s;',
                [data['id'], data['id']])
            raws = cursor1.fetchall()
            if raws != None:
                for raw in raws:
                    print(raw)
                    print(type(raw))
                    raw_dict = {
                        "id": raw[0],
                        "id_from": raw[1],
                        "id_to": raw[2],
                        "amount": raw[-1]
                    }
                    resp.append(raw_dict)
            else:
                resp = {
                    'error': 'истопия пуста'
                }
        return JsonResponse(resp, safe=False)

