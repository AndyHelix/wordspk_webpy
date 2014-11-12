#!/usr/bin/env python
# encoding: utf-8
# author: andyhelix
# email: alayasix@foxmail.com

import web
import sqlite3, hashlib

# import model

### Urls

urls = (
        '/', 'Index',
        '/people/(.*)', 'People',
        '/login', 'Login',
        '/pkwords/(.*)', 'Pkwords',
        '/reset', 'reset',
        )

app = web.application(urls, globals())
# web.config.debug = False

### Templates

render = web.template.render('templates',base='base')

# session
# 1. 避免关闭debug模式 2. 各文件内session可用
pkround = 0
word1 = [12,[13,14,15,12]]
#pkwords = {1:word1,2:word2,3:word3}
if web.config.get("_session") is None:
    from web import utils
    store = web.session.DiskStore('sessions')
    pkwords_page={'round':0,'wordid':0}
    web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
    web.config.session_parameters['timeout'] = 60*60
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username': 0,'loggedin': False, 'pkwords_pages':pkwords_page})
    web.config._session = session
else:
    session = web.config._session

# #is_login
def is_login(*username):
    if len(username) == 0:
        #print 'get no name'
        pass
    else:
        #print str(session.loggedin)
        #print session.username,'*'*20
        #print username, session.username
        if session.loggedin and username[0] == session.username:
            print "login state"
        else:
            raise web.seeother("/login")

#
def connectdb(dbname):
    handdb = sqlite3.connect(dbname)
    handc = handdb.cursor()
    return (handdb, handc)

# TODO @#is_login():
class Index:
    #is_login(session)
    def GET(self):
        is_login()
        raise web.seeother("/login")

class People:
    #is_login(session)
    def GET(self, name):
        is_login(name)
        #return "<b>Hello, "+"what a wonderful day!\n"+name
        return render.people(name)
    def POST(self):
# insert to pkings
        return 'done'

class Login:
    #is_login(session)
    form = web.form.Form(
            web.form.Textbox('username', web.form.notnull, description="Username"),
            web.form.Textbox('password', web.form.notnull, description="Password"),
            web.form.Button('Login'),
            )

    def GET(self):
        """Show loginpage"""
        form = self.form()
        if session.loggedin:
            raise web.seeother("/people/"+session.username)
        else:
            return render.login(form)
            
    def POST(self):
        form = self.form()

        if not form.validates():
            return render.login(form)
        else:
            auth = sqlite3.connect('users.db')
            c = auth.cursor()
            #pwdhash = hashlib.md5(i.password).hexdigest()
            pwdhash = form.d.password
            query = 'select * from users where username="%s" and password="%s"' % (form.d.username,pwdhash)

            checkit = c.execute(query)
            check = checkit.fetchall()
            if len(check) != 0:
                session.loggedin = True
                #print str(session.loggedin)
                session.username = form.d.username
                #print "***"+str(session.username)+"***"
                raise web.seeother("/people/"+form.d.username)
            else:
                session.username = 'no user'
                #print "***"+str(session.username)+"***"
                #print "form has data "+form.d.username
                return render.base("Those login details don't work,goto <a href='/login'>try again</a>")


class Pkwords:
    #is_login(session)
    def GET(self, pklistraw):
        # is_login()
        # pklist andy_vs_ariel_round1
        if pklistraw:
            pklist = pklistraw.split('_')
            is_login(pklist[0])
# home games away games
            homeuser = pklist[0]
            awayuser = pklist[2]
            roundname = pklist[3]
            roundid = int(roundname[5:])
### get words_list
# cookie 是否存在
# 是-> 下一题
# 否-> 根据round找到第一题设置cookie
            dbname = 'users.db'
            (handdb, handc) = connectdb(dbname)
            urlstr = web.setcookie('urlstr',pklistraw,3600)
            #web.setcookie('wordid', 101, 3600)
            wordid = web.cookies().get('wordid')
            roundwide = 100*(roundid-1)+20
            print wordid,'*'*20,roundwide

            if wordid:
                if int(wordid) == roundwide:
                    getword=False
                    return render.pkwords(homeuser, awayuser, getword)
                else:
                    query = "select * from rounds where roundname='%s' and wordid=%d" % (roundname, int(wordid)+1)
                    print query
                    getwordall = handc.execute(query)
                    getwordfetch = getwordall.fetchall()
                    getword = getwordfetch[0]
                    web.setcookie('wordid', str(int(wordid)+1), 3600)
                    return render.pkwords(homeuser, awayuser, getword)
            else:
                query = "select * from rounds where roundname='%s' and id=%d" % (roundname, 20*(int(roundname[5:])-1)+1)
                print query
                getwordall = handc.execute(query)
                #print getwordall.fetchall()
                getword = getwordall.fetchall()[0]
                
                web.setcookie('wordid', getword[2], 3600)
                print getword
                return render.pkwords(homeuser, awayuser, getword)
        else:
            return 'not valid input'
    
    def POST(self,var):
#判断对错
        #user_data = web.input(id="no data")
        #return "<h1>" + user_data.id + "</h1>"
        i = web.input(choice='no data')
        print i.choice,'*'*20
        pklist = web.cookies().get('urlstr')
        roundname = pklist.split('_')[3]
        roundid = int(roundname[5:])
        wordid = web.cookies().get('wordid')
        print wordid,'*'*20

        query = "select * from rounds where roundname='%s' and wordid=%d" % (roundname, int(roundname[5:]))
        #print pklist ,'*'*20
        raise web.seeother('/pkwords/'+pklist)
        

class reset:
    def GET(self):
        session.kill()
        web.header('Content-Type', 'text/html')
        return "session was reset\n<a href='http://localhost:8080/'>GO HOMEPAGE</a>"
# 页面跳转 仿照 php

if __name__ == '__main__':
    #app = web.application(urls, globals())
    app.run()
