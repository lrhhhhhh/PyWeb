# PyWeb

一个面向python web初学者的web框架，代码简洁，结构清晰，方便初学者理解web框架是如何工作的。底层基于`werkzeug`和`jinja2`。

## 快速开始
### 创建一个新的应用
```python
from PyWeb import PyWeb
app = PyWeb()
```
### 创建一个视图函数
使用如下语句定义一个视图函数，此函数将会接受`http`请求`request`并返回一个简单的`hello world`字符串:
```python
from PyWeb.response import TextPlainResponse

def hello(request):
    return TextPlainResponse('hello world')
```

### 路由映射
对于上面的视图函数`hello`，创建路由如下
```python
app.router.register([
    ('/', hello, 'hello'),
])
```

### 启动服务器
执行如下语句启动服务器，`PyWeb`会帮助我们启动底层的`WSGI`服务器，默认地址是`127.0.0.1`，端口号是`23333`：
```python
app.run(debug=True)
```
`PyWeb`为`run()`接口提供了一个`debug`参数，默认值是`False`，若置为`True`则会启动`debug`模式。
在`debug`模式中，任何对源代码的修改都将自动重启服务器，且一旦发生了错误将会在浏览器上以页面的形式显示出错误栈信息。

### 查看运行情况
打开浏览器并访问`http://127.0.0.1:23333/`，你将会看到视图函数`hello`返回的`hello world`字符串。

(ps: 可以直接运行`example/example.py`中的代码)

---

## 各个功能的详细介绍和使用
下面是`PyWeb`框架目前支持的功能详细介绍和使用说明。

### 路由系统
#### 定义路由表

路由系统是`web`框架核心的功能之一，`PyWeb`实现了Router类，并将其组合到每一个application中。
用户手动编写路由规则，并调用Router类的register()方法将路由规则绑定到application中。

每条路由由`3`个参数组成：`url, view_func, endpoint`，其中url已经不需要介绍，
view_func代表处理该url的视图函数，endpoint唯一标识一个view_func。

请求被Router处理的过程为：  
通过请求的url查找对应endpoint，再通过endpoint查找对应view_func。


支持反向查询，通过endpoint查找url：
```python
from PyWeb import PyWeb

app = PyWeb()

url_map = [
    ('/', index_view, 'index'),   
    ('/about', about_view, 'about'),  
    ('/article', article_view, 'article'),    
]

app.router.register(url_map)
url = app.router.reverse('index')  
print(url)   # url的值为'/'
```

#### 动态路由
`PyWeb`支持带参数的url
```python
from PyWeb.app import PyWeb
from PyWeb.response import TextPlainResponse

app = PyWeb()

def user_info_by_uid(request, uid):
    return TextPlainResponse(uid)

def user_info_by_username(request, username):
    return TextPlainResponse(username)

url_map = [
    ('user/<int:uid>', user_info_by_uid, 'user_info_by_uid'),
    ('user/<username>', user_info_by_username, 'user_info_by_username')
]

app.router.register(url_map)
app.run()

```

#### 多级路由
`PyWeb`的路由系统还支持多级路由，多级路由使用SubRouter实现:
```python
from PyWeb.router import Router, SubRouter

routes = [
    ('/index/something', SubRouter(url='/people', view_func=lambda: 'fake view func1', endpoint='people'), 'index'),
    ('/blog', SubRouter(url='/article1', view_func=lambda: 'fake view func2', endpoint='article'), 'blog'),
    ('/about', lambda: 'fake view func3', 'about'),
]
router = Router()
router.register(routes)
print(router.rules)
print(router.map)
```
输出：
```python
{('index.people',): {'view_func': <function <lambda> at 0x7f8383bba1f0>, 'url': '/index/something/people'}, ('blog.article',): {'view_func': <function <lambda> at 0x7f838316a1f0>, 'url': '/blog/article1'}, 'about': {'view_func': <function <lambda> at 0x7f838316a280>, 'url': '/about'}}
Map([<Rule '/index/something/people' -> ('index.people',)>,
 <Rule '/blog/article1' -> ('blog.article',)>,
 <Rule '/about' -> about>])
```



### 视图系统
#### 视图传参
视图系统是处理`http`请求并返回`http`响应的地方。
在`PyWeb`中，所有的视图函数的第一个参数固定为`request`，代表当前的请求对象，用户可以通过此对象访问有关request的相关数据。如
表单数据和url参数。视图函数的其他参数为url中对应的参数。



### 响应对象

#### 纯文本响应对象`TextPlainResponse`
`PyWeb`使用`TextPlainResponse`来实现`mimetype=text/plain`的响应 ，所以它不会被浏览器当做`html`页面渲染，而是直接打印字符串。
像这样使用视图系统：
```python
from PyWeb.response import TextPlainResponse

def hello(request, username):
    return TextPlainResponse(username)
```

#### HTML响应对象`TextHTMLResponse`
`PyWeb`为用户提供了一个`TextHtmlResponse`来实现`mimetype=text/html`的响应对象，
其底层调用了`jinja2`的渲染接口，会将模板中的变量进行替换。 
浏览器会将TextHTMLResponse返回的结果当做`html`页面渲染并展示。
```python
from PyWeb.response import TextHTMLResponse

def user_info(request, username):
    return TextHTMLResponse(username=username, template_path='template', template_name='welcome.html')
```



### 中间件系统
`PyWeb`提供了中间件系统，让用户可以在视图函数处理前和视图函数处理后对请求(或响应)对象完成必要的中间操作。

#### 定义中间件
实现了`MiddleWareInterface`接口类，自定义中间件需要实现指定接口。  
通过以下方式自定义一个中间件：
```python
from PyWeb.middlewares import MiddleWareInterface, BEFORE_REQUEST


class MyMiddleware(MiddleWareInterface):
    type = BEFORE_REQUEST

    def apply_before(self, request, **kwargs):
        print('middleware apply before', request)

    def apply_after(self, response, **kwargs):
        pass
```

#### 注册中间件
实现了中间件管理器`MiddlewareManager`，并将其组合到application中，然后通过中间件管理器的register()方法进行注册以使其生效：
```python
app.middleware_manager.register([MyMiddleware(), ])
```


#### 多个中间件的执行顺序
按照list中中间件顺序。


## 拓展阅读——web框架工作原理
python web框架需要实现pep333和pep3333中指定的相关协议（WSGI协议），具体来说只需要实现一个指定名称，指定参数的方法即可。
这个项目中实现的是`__call__(environ, start_response)`，需要明确连参数`envrion`和`start_response`都是web服务器传递给web框架的，
web框架只需要专注于request和response的内容处理。

web框架通常做法如下：
1. 将http请求封装为web框架实现的request类
2. 使用路由器获得当前处理请求的url所对应的视图函数
3. 视图函数对request进行对应逻辑处理，然后返回web框架实现的response对象
4. response中调用web服务器传递的`start_response()`函数，将响应处理为一个可迭代对象
5. web服务器将这个可迭代对象封装为http响应返回给请求的用户

