import queue
import threading


from itops.settings import ldap3RESTARTABLE

def repeace(message):
    promessage=message.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a')
    return promessage



alluservaluelist = list()
class TestThread(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que

    def run(self):
        while True: # 需要通过循环来不断的运行任务
            item = self.queue.get()
            member = item[0]
            disName = repeace(member)
            with ldap3RESTARTABLE as conn:
                conn.search(search_base=disName,
                                        search_filter="(objectClass=*)",
                                        search_scope='BASE',
                                        attributes=['displayName', 'wWWHomePage', 'physicalDeliveryOfficeName','sAMAccountName', 'mail'])
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = response_id[0].get('attributes', '')
                    alluservaluelist.append(message)
            self.queue.task_done()

def start_thread():
    for thread in threads:
        thread.start()

q = queue.Queue(1500)

def Usermessage(members):
    del alluservaluelist[:]
    # 开启线程
    for i in range(1500):
        t = TestThread(q)
        t.daemon = True
        t.start()

    for member in members:
        listvalue = [member]
        q.put(listvalue)
    q.join()
    return alluservaluelist
