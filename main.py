import csv
import ipaddress
import asyncio
import time


async def ip_ping(ip_addr):
    global num_ip
    num_ip = [[] * i for i in range(4)]
    try:
        result = await asyncio.open_connection(ip_addr, 80)
        if result:
            num_ip[0].append(ip_addr)
            print("ip адрес %s доступен" % ip_addr)
    except ConnectionError:
        num_ip[1].append(ip_addr)
        print("Задынный порт недоступен у адреса %s" % ip_addr)
    except OSError:
        num_ip[2].append(ip_addr)
        print("Превышен лимит ожиданий у %s" % ip_addr)
    except:
        num_ip[3].append(ip_addr)
        print("Неясно что тут у %s" % ip_addr)


start = time.monotonic()

addr = []
with open('ipaddr.csv', newline='') as csvfile:
    string = csv.reader(csvfile)
    for row in string:
        if row:
            if '/' in row[0]:
                try:
                    for ip in ipaddress.IPv4Network(row[0]):
                        addr.append(ip.exploded)
                except:
                    pass
            else:
                addr.append(row[0])
loop = asyncio.get_event_loop()
task_list = [loop.create_task(ip_ping(ip_ad)) for ip_ad in addr]
loop.run_until_complete(asyncio.wait(task_list))
result = time.monotonic() - start
print("Program time: {:>.3f}".format(result) + " seconds.")
print('Количество опрошенных адресов: %i' % (len(addr)))
print('Доступные    |    Недоступные    |    Состояние не установленно  |   Ошибка с сокетами')
print("{:<20} {:<20} {:<30} {:<20}".format(len(num_ip[0]), len(num_ip[1]),
                                           len(num_ip[2]), len(num_ip[3])))

