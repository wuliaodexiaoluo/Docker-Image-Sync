try:
    import os
    import sys
    
    for x in range(len(sys.argv)):
        if sys.argv[x] == "--username=":
            user = sys.argv[x].replace("--username=","")
        elif sys.argv[x] == "--passwd=":
            password =  sys.argv[x].replace("--passwd=","")
        elif sys.argv[x] == "--reponame=":
            reponame = sys.argv[x].replace("--reponame=","")
        elif sys.argv[x] == "--image=":
            imagelist = sys.argv[x].replace("--image=","")
            imagelist = imagelist.split(",","")
    try:
        os.system("systemctl restart docker-daemon")
    except Exception as e:
        loger.error("重启 Docker 服务失败")
    for x in range(len(imagelist)):
        os.system("docker save -o "+imagelist[x]+" "+imagelist[x].lsplit("/",1)+".tar")
        
