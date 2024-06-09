try:
    import json
    from loguru import logger
    import threading
    import subprocess 
    from sys import argv
    from requests import get
    Head_repo = []
    Base_repo = []
    name = []
    commits = []
    failed = []
    need_update = []
    pass_list = []
    logger.info("[Start] Sync 开始")
    logger.info("[Config] 任务状态改变:Free ----> Initializing")
    f = open(__file__.replace("Sync.py","")+"sync-config.json","r+")
    logger.info("[Config] 任务状态改变:Initializing ----> Working")
    # 解析 JSON 字符串为 Python 字典  
    data = json.loads(f.read())
    
    
    # 遍历 Configs 数组中的每个配置对象  
    for config in data["Configs"]:  
        # 提取每个配置对象的 name 属性  
        Head_repo.append(config["Sync-Url"])
        Base_repo.append(config["Repo"])
        name.append(config["name"])
        commits.append(config["Latest-Commit"])
    num = len(Head_repo)
    
    logger.info("[Config] 任务状态改变:Working ----> Done")
    logger.info("[Config] 总计获取有效的配置总量:"+str(num))
    logger.info("[Event] 任务状态改变:Free ----> Working")

    
    try:
        api_Key = argv[1].replace("--api-key=","")
    except Exception as e:
        logger.warning("[Sync] 解析 API Key 失败，同步速率受到限制")
    try:
        user = argv[2].replace("--username=","")
        email = argv[3].replace("--email=","")
    except Exception as e:
        logger.warning("[Sync] 未配置用户名和密码，将使用 Action 账户提交,请确保 Action 拥有写入权限")
        user = "GitHub Actions"
        email = "actions@github.com"
    
    for x in range(num):
        url = "https://api.github.com/repos/"
        url = url + Head_repo[x].replace("https://github.com/","").replace(".git","") + "/commits"
        response = get(url)
        if response.status_code > 399:
            failed.append(name[x])
        else:
            commit = json.loads(response.text)
            commit = commit[0]["sha"]
            if commits[x] != commit:
                need_update.append(name[x])
            else:
                pass_list.append(name[x])
    logger.info("[Event] 任务状态改变:Working ----> Done")
    logger.info("[Sync] 共计解析了"+str(num)+"个配置，失败:"+str(len(failed))+",无需更新:"+str(len(pass_list))+",需要更新:"+str(len(need_update)))
    logger.info("[Sync] 任务已就绪，同步工作开始")
    try:
        command = "git config --global user.name" + "" + user
        subprocess.run(command, capture_output=True, text=True, check=False)
        command = "git config --global user.email" + "" + email
        subprocess.run(command="git config --global user.email"+""+email, capture_output=True, text=True, check=False)
    except Exception as e:
        logger.error("[Sync] 初始化用户信息失败，详细信息: \n"+str(e))

     
    '''
    def run_command_in_thread(command, callback):  
         
        result = subprocess.run(command, capture_output=True, text=True, check=False)  
        callback(result.returncode, result.stdout, result.stderr)  

    def handle_result(returncode,stderr,logger):  
    # 处理结果  
        if {returncode} !=0: 
            logger.error("已收到进程报告：失败，返回码："+returncode+" \n 错误信息"+{stderr}) 

        else:
            logger.error("已收到进程报告：成功，返回码："+returncode) 
    # 创建一个线程来运行命令
    for x in range(num):  
        thread = threading.Thread(target=run_command_in_thread, args=(['git clone'+str(Base_repo[num])], handle_result))  
      
    thread.start()  
      
    thread.join()  
    '''
    


    
    
        
except Exception as e:
    logger.error("[Sync] 出现未知错误，详细信息: \n" + e)