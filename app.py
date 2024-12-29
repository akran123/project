from flask import Flask,redirect,render_template,url_for, request,flash,session
from DB_handler import DBModule
from datetime import datetime,timedelta

app = Flask(__name__)
app.secret_key="qewrqwerqwerqw"
DB = DBModule()

@app.route("/")
def index():
    if "uid" in session :
        user=session["uid"]
    else :
        user="login"
    return render_template("base.html",user=user)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "uid" not in session:
        return redirect(url_for("login"))

    user = session["uid"]
    show_details = session.pop("show_details", False)  # session에서 show_details 가져오기
    current_task = None

    if request.method == "POST":
        if request.form.get("show_details"):
            show_details = True
            session["show_details"] = True  # show_details 상태를 session에 저장
        else:
            task_title = request.form.get("task_title")
            task_date = request.form.get("task_date")
            subtasks = request.form.get("subtasks")

            if task_title and task_date:
                task_data = {
                    "title": task_title,
                    "date": task_date,
                    "subtasks": subtasks,
                    "created_at": str(datetime.now())
                }
                DB.add_task(user, task_data)
                show_details = False

        # POST 요청 처리 후 GET 요청으로 리다이렉트
        return redirect(url_for("dashboard"))

    # GET 요청 처리
    filter_date = request.args.get("filter_date")
    page = int(request.args.get("page", 1))  # 현재 페이지 (기본값: 1)
    per_page = 7  # 페이지당 일정 개수

    tasks = DB.get_tasks(user)

    today = datetime.now().strftime("%Y-%m-%d")
    if filter_date == "today":
        tasks = [task for task in tasks if task["date"] == today]
    elif filter_date == "tomorrow":
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        tasks = [task for task in tasks if task["date"] == tomorrow]
    elif filter_date == "past":
        tasks = [task for task in tasks if task["date"] < today]

    # 페이징 처리
    total_tasks = len(tasks)
    total_pages = (total_tasks + per_page - 1) // per_page  # 전체 페이지 수
    start = (page - 1) * per_page
    end = start + per_page
    tasks_on_page = tasks[start:end]

    return render_template(
        "todo_dashboard.html",
        user=user,
        tasks=tasks_on_page,
        show_details=show_details,
        current_task=current_task,
        current_page=page,
        total_pages=total_pages,
    )


   

@app.route("/login")
def login():
    if "uid" in session :
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('uid', None)
    return redirect(url_for('index'))


@app.route("/login_done", methods=["GET"])
def login_done():
    
    uid=request.args.get("id")
    pwd=request.args.get("pwd")
    print(uid, pwd)
    if DB.login(uid,pwd):
        session["uid"]=uid
        return redirect(url_for("index"))
    else :
        flash("아이디가 없거나 비밀번호가 틀립니다.")
        return redirect(url_for("login"))


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/signin_done", methods=["GET"])
def signin_done():
    email=request.args.get("email")
    uid=request.args.get("id")
    pwd=request.args.get("pwd")
    name=request.args.get("name")
    
    if DB.signin(email=email,_id_=uid,pwd=pwd,name=name) :
        return redirect(url_for("login"))
    else :
        flash("이미 존재하는 계정입니다.")
        print("확인완료")
        return redirect(url_for("signin"))
    


@app.route("/user/<uid>")
def user(uid):
    pass


if __name__=="__main__" :
    app.run(host="0.0.0.0", debug=True)