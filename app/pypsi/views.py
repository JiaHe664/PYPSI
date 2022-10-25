from django.http import HttpResponse, FileResponse, JsonResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from intersect.models import ClientTask, ClientTable, ClientResult
from django.core import serializers
import time
import json
from intersect.psi.client import start_client
from intersect.psi.server import start_server
import os
from intersect.psi.psi.cuckoo import CuckooHashTable
import shelve
import time
import math


def client_home(request):
    
    from django.shortcuts import render
    
    return render(request, 'client_home.html')
@csrf_exempt
def client_upload(request):
    if request.method == 'POST':
        obj = request.FILES['file']
        filename = os.path.join(settings.MEDIA_ROOT, obj.name)
        with open(filename, 'wb') as f:
            data = obj.file.read()
            f.write(data)
        # max_lines = 100000
        # lines = 0
        # with open(filename, mode="r", encoding="utf-8") as f:
        #     words = []
        #     for line in f:
        #         if lines >= max_lines:
        #             break
        #         else:
        #             words.append(line.rstrip().encode("utf-8"))
        #         lines += 1
        # 将数据存储数据库
        # for word in words:
        #     SimpleHash(data=word).save()
        # for i in range(3):
        #     for word in words:
        #         h = sm3.digest(bytes([i+1]) + word)
        #         if i == 0:
        #             item = SimpleHash.objects.get(data = word)
        #             item.h1 = h
        #             # SimpleHash.objects.filter(data = word).update(h1=h)
        #         elif i == 1:
        #             item = SimpleHash.objects.get(data = word)
        #             item.h2 = h
        #             # SimpleHash.objects.filter(data = word).update(h2=h)
        #         else:
        #             item = SimpleHash.objects.get(data = word)
        #             item.h3 = h
        #             # SimpleHash.objects.filter(data = word).update(h3=h)
        #         item.save()
            
        # 预计算哈希
        with open(filename, mode="r", encoding="utf-8") as f:
            words = []
            lines = 0
            for val in f:
                lines += 1
                words.append(val.rstrip().encode("utf-8"))
        
        n = int(1.2 * len(words))
        s = 5
        cuckoo = CuckooHashTable(n, s)
        for word in words:
            cuckoo.update(word)
        # 写入文件
        # 使用shelve打开文件
        filename = obj.name.split('.')[0] + '_cuckoo'
        filename = os.path.join(settings.MEDIA_ROOT, filename)
        file = shelve.open(filename)

        file['table'] = cuckoo.table
        file['stash'] = cuckoo.stash
        file['table_hash_index'] = cuckoo.table_hash_index
        
        # 关闭文件
        file.close()
            
        res = {}
        res['name'] = obj.name
        res['date'] = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        res['records'] = lines
           
        table = ClientTable(
            name = res['name'],
            records = res['records'],
            date = res['date']
        )
        table.save()
        
        return JsonResponse(res)


@csrf_exempt    
def client_download(request, filename, *args, **kwargs):
    file_name = filename
    # 拼接文件路径
    filepath = os.path.join(settings.MEDIA_ROOT, file_name)
    file = open(filepath, 'rb')
    response = FileResponse(file)  # 生成文件对象application/msword  application/octet-stream
    response['Content-Type'] = 'text/plain'
    #name.split('.')[0] + '.docx'，
    name = file_name
    response['Content-Disposition'] = 'attachment;filename ="%s"' % (
        name.encode('utf-8').decode('ISO-8859-1'))
    return response

def client_deleteTable(request, filename, *args, **kwargs):
    file_name = filename
    # 拼接文件路径
    filepath = os.path.join(settings.MEDIA_ROOT, file_name)
    os.remove(filepath)
    
    table = ClientTable.objects.get(name=filename)
    table.delete()
    
    # 删除预计算存储的cucoo哈希文件
    file_name = filename.split('.')[0] + '_cuckoo'
    filepath = os.path.join(settings.MEDIA_ROOT, file_name)
    os.remove(filepath + '.bak')
    os.remove(filepath + '.dat')
    os.remove(filepath + '.dir')
    
    
    return HttpResponse('delete OK')

def client_deleteResult(request, filename, *args, **kwargs):
    file_name = filename
    # 拼接文件路径
    filepath = os.path.join(settings.MEDIA_ROOT, file_name)
    os.remove(filepath)

    table = ClientResult.objects.get(name=filename)
    table.delete()
    
    return HttpResponse('delete OK')

def client_loadTable(request):
    client = {}
    table = serializers.serialize("json", ClientTable.objects.all())
    client['table'] = table
    
    return JsonResponse(client)

def client_loadTask(request):
    client = {}
    task = serializers.serialize("json", ClientTask.objects.all())
    client['task'] = task
    
    return JsonResponse(client)

def client_loadResult(request):
    client = {}
    result = serializers.serialize("json", ClientResult.objects.all())
    client['result'] = result
    
    return JsonResponse(client)

@csrf_exempt    
def client_createTask(request):
    data = json.loads(request.body)
    task = ClientTask(
        label = data['id'],
        table = data['table'],
        results = data['results'],
        date = data['date'],
        runtime = data['runtime'],
        status = data['status'],
        host = data['host'],
        port = data['port'],
    )
    task.save()
    ClientTable.objects.filter(name=data['table']).update(task_id=data['id'])
    
    return HttpResponse('create task ok')

@csrf_exempt    
def client_startTask(request):
    data = json.loads(request.body)
    ClientTask.objects.filter(label=data['id']).update(status=1)
    # 求交
    client_data_path = os.path.join(settings.MEDIA_ROOT, data['table'])
    client_result_path = os.path.join(settings.MEDIA_ROOT, data['table'].split('.')[0] + '_result.txt')
    ip_port = data['host'] + ':' + str(data['port'])
    start_time = time.time()
    res_strs = start_client(ip_port, '127.0.0.1:1234', client_data_path)
    results = len(res_strs)
    end_time = time.time()
    runtime = math.floor(end_time - start_time)
    with open(client_result_path, mode="w", encoding="utf-8") as f:
        for line in res_strs:
            f.write(line)
            f.write("\n")
    ClientTask.objects.filter(label=data['id']).update(runtime=runtime)
    ClientTask.objects.filter(label=data['id']).update(results=results)
    
    ClientResult(
        date = time.strftime("%Y-%m-%d",time.localtime(time.time())),
        name = data['table'].split('.')[0] + '_result.txt',
        records = results,
        task_id = data['id']
    ).save()
    return HttpResponse('the task is finished!')
        
@csrf_exempt    
def server_startTask(request):
    data = json.loads(request.body)
    # 求交
    ip_port = data['host'] + ':' + str(data['port'])
    server_data_path = os.path.join(settings.MEDIA_ROOT, 'server_data.txt')
    start_server('127.0.0.1:1234', ip_port, server_data_path)
    
    return HttpResponse(' the task is finished')  

def login(request):
    from django.shortcuts import render
    
    return render(request, 'login.html')    

@csrf_exempt    
def showDetails(request):
    data = json.loads(request.body)
    table_name = ClientTask.objects.get(label=data['id']).table
    # 求交
    client_data_path = os.path.join(settings.MEDIA_ROOT, table_name)
    client_result_path = os.path.join(settings.MEDIA_ROOT, data['table'])
    with open(client_result_path, mode="r", encoding="utf-8") as f:
        res_strs = [line.rstrip() for line in f]
    _intersections = []
    intersections = []
    differences = []
    for item in res_strs:
        _intersections.append(item)
    with open(client_data_path, mode="r", encoding="utf-8") as f:
        data = [line.rstrip() for line in f]
    for item in data:
        dic = {}
        dic['pwd'] = item
        if item not in _intersections:
            differences.append(dic)
        else:
            intersections.append(dic)
    return JsonResponse({'intersections':intersections, 'differences':differences})
        