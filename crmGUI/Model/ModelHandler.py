from crmGUI.Model import ChairModel, UserModel


def modelHandler(tableName: str) -> type:
    if tableName == ChairModel.Chair.__tablename__:
        return ChairModel.Chair
    if tableName == UserModel.User.__tablename__:
        return UserModel.User
