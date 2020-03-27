'''
测试目的：我需要写一个装饰器，需要在主方法执行到被装饰函数时执行，接收的参数和返回参数与被装饰的方法相同，
'''


# 装饰器
# def decorate(func):
#     print("decorate foo..")
#     return func

# def decorate(func):
#     print("decorate...")
#     def new_func(a, b, c):
#         print("decorate new_func..")
#         if a == 1:
#             a = 2
#         return func(a, b, c)
#     return new_func

def decorate(func):
    print("decorate...")
    def new_func(a, b, c):
        print("decorate new_func..")
        if a == 1:
            return 8888
        return func(a, b, c)
    return new_func

# 被装饰函数
@decorate
def foo(a, b, c):
    print("foo...")
    return a+b+c



# 调用foo的主方法
def invokeFoo():
    print("invokeFoo...")
    a, b, c = 1, 2, 3
    ret = foo(a, b, c)
    print("foo ret...", ret)


if __name__ == '__main__':
    invokeFoo()
    '''
    执行结果
    decorate... // 装饰器外层函数最先执行
    invokeFoo... // 调用被装饰方法的主方法执行
    decorate new_func.. // 装饰器内层方法执行
    foo... // 被装饰方法执行
    foo ret... 8888 // 被装饰方法执行完毕
    '''
