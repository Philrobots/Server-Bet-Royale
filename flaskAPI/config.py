class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "VitAo;wH7noT2y2c!}yN'?o=X1|:[T]l!RS3;<s_?rW^a-S>+zQ9fItgn>T5{lguuid.uu"
    ADMIN_KEY = "Nq[nn#/uIT$AVYS`{H;:V=,OM[LR8sr!^?B<}u[5jy-]K+^nTLf87Fmil[cMq?k"
    ODDS_API_KEY = "87c963d43e0c21a33f7d029816a95f77"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "cestunsecret"


class TestingConfig(Config):
    TESTING = True
