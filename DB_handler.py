import pyrebase
import json
from datetime import datetime

class DBModule:
    def __init__(self) :
        with open("./auth/firebaseAuth.json") as f:
            config= json.load(f)

        firebase=pyrebase.initialize_app(config)
        self.db=firebase.database()
        
        



    def login(self,uid,pwd):
        users=self.db.child("users").get().val()
        print(users)
        if uid in users:
        # uid로 접근하면 또 다른 딕셔너리가 있고, 그 안에 pwd 필드가 있음
            user_entries = users[uid]
        # user_entries 예: {'-OEJlCmGv2Hktpg1tRZB': {'Id': 'asdf', 'email': '...', 'pwd': 'asdf', 'uname': 'asdf'}}

            for key, user_info in user_entries.items():
                # user_info 안에 pwd가 있을 경우 pwd 비교
                if 'pwd' in user_info and user_info['pwd'] == pwd:
                    print(1)
                    return True
            # uid는 있지만 적절한 pwd를 못 찾은 경우
                print(2)
                return False
            else:
            # uid 자체가 없을 경우
                print(3)
                return False
        
        

    def signin_verification(self,uid) :
        users=self.db.child("users").get().val()
        if users is None :
            users={}
        
        users=list(users.keys())
        for i in users :
            if uid==i:
                return False
        
        return True
       
        
    

    def signin(self,_id_,pwd,name,email):
        information={"Id" : _id_,"pwd":pwd,"uname":name,"email":email}
        if self.signin_verification(_id_) :
            
            self.db.child("users").child(_id_).push(information)
            return True
        else :
            return False
        
        
    
    def add_task(self, uid, task_data):
        """
        Task를 Firebase에 저장
        uid: 사용자 ID
        task_data: 저장할 데이터(dict)
        """
        self.db.child("tasks").child(uid).push(task_data)

    def get_tasks(self, uid):
        """
        Firebase에서 사용자의 모든 Task 데이터를 가져옵니다.
        """
        tasks = self.db.child("tasks").child(uid).get().val()
        if tasks:
            task_list = [{"id": key, **value} for key, value in tasks.items()]
            # 날짜를 기준으로 정렬
            sorted_tasks = sorted(
                task_list,
                key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d')  # 'date' 필드 기준 정렬
            )
            return sorted_tasks
        return []