class UserInfo(BaseTable):
    """
    用户注册信息表
    """

    class Meta:
        verbose_name = "用户信息"
        db_table = "UserInfo"

    username = models.CharField('用户名', max_length=20, unique=True, null=False)
    password = models.CharField('登陆密码', max_length=100, null=False)
    email = models.EmailField('用户邮箱', unique=True, null=False)
