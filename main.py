import csv
import ipaddress
import asyncio
import time


async def ip_ping(ip_addr):
    global num_ip
    try:
        result = await asyncio.open_connection(ip_addr, 80)
        if result:
            print("ip адрес %s доступен" % ip_addr)
    # except ConnectionError:
    #     print("Задынный порт недоступен у адреса %s" % ip_addr)
    # except OSError:
    #     print("Превышен лимит ожиданий у %s" % ip_addr)
    # except (asyncio.LimitOverrunError, asyncio.IncompleteReadError):
    #     print("Неясно что тут у %s" % ip_addr)
    except:
        pass
    num_ip = num_ip + 1


num_ip = 0
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
print(f"started at {time.strftime('%X')}")
task_list = [loop.create_task(ip_ping(ip_ad)) for ip_ad in addr]
loop.run_until_complete(asyncio.wait(task_list))
print(loop.time())
print(f"finished at {time.strftime('%X')}")
print(
    'Количество опрошенных адресов: %i и количество прошедших %i' % (len(addr),
                                                                     num_ip))
