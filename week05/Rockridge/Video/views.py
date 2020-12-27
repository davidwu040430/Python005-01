from django.shortcuts import render
from django_redis import get_redis_connection

# Create your views here.

def video_list(request):
    vlist = [1001, 1002, 1003, 1004, 1005]
    conn = get_redis_connection("default")
    vid = request.GET.get('vid')
    # 如果有参数vid，就vid所在的计数器加1
    if vid:
        conn.incr(vid)
    # 遍历列表，取出所有的视频的vid和计数器
    counts = []
    for v in vlist:
        count = conn.get(v)
        if count:
            counts.append(count.decode())
        else:
            conn.set(v, 0)
            counts.append(0)
    vcount = zip(vlist, counts)
        
    return render(request, 'index.html', locals())
    

