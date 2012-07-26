# -*- coding: utf-8 -*-

import rbac

def main():
    korus_db = rbac.Manage.connect(
        engine_str='mysql://tmis:q1w2e3r4t5@spb-med-mysql.korusdomain/RBAC?charset=utf8',
        engine_args = {'echo':True})

    korus_db.Groups.add(u'Администраторы')
    korus_db.Groups.add(u'Гости')
    korus_db.Users.add(u'root',          '', '', 'root',  'root',  u'Администраторы')
    korus_db.Users.add(u'Администратор', '', '', 'admin', 'admin', u'Администраторы')
    korus_db.Users.add(u'Гость',         '', '', 'guest', 'guest', u'Гости')

if __name__ == '__main__':
    main()
