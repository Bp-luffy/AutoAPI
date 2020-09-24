from interface.kfk_ponint.point import KafkaPython


def choose_userid_from():
    while True:
        print('''
             =========== start ============
                 1、手机号启动
                 2、配置文件启动
                 q、退出
             ============ end =============''')
        choose = input('选择获取方式:').strip()

        if choose == 'q':
            break

        if not choose.isdigit():
            print("请输入数字")
            continue

        choose = int(choose)
        if choose == 1:
            while True:
                print('''
                     =========== start ============
                         1、手机号启动
                         2、配置文件启动
                         q、退出
                     ============ end =============''')
                phone = input('请输入11位手机号：').strip()
                if phone == 'q':
                    break
                if len(phone) != 11:
                    print('输入的手机号不是11位手机号')
                    continue
                if not phone.isdigit():
                    print('请输入11位数字的手机号')
                    continue
                kp = KafkaPython(phone)
                kp.main()
        else:
            kp = KafkaPython()
            kp.main()


if __name__ == '__main__':
    choose_userid_from()
