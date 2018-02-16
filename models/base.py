import json


class Model:
    @classmethod
    def get_db_path(cls):
        return 'db/' + cls.__name__ + '.txt'

    @classmethod
    def create_obj(cls, save=True, **kwargs):
        if save:
            obj = cls(**kwargs)
            obj.save()
            return obj
        else:
            return cls(**kwargs)

    def save(self):
        """
        TODO:当用户信息修改了之后需要回写数据
        """
        with open(self.get_db_path(), 'a') as f:
            data_str = json.dumps(self.__dict__)
            f.write(data_str + '\n')

    @classmethod
    def all(cls):
        obj_list = []
        with open(cls.get_db_path()) as f:
            for line in f:
                obj_dict = json.loads(line)
                obj = cls.create_obj(save=False, **obj_dict)
                obj_list.append(obj)
        return obj_list

    @classmethod
    def get_by(cls, **kwargs):
        objs = cls.all()
        for k, v in kwargs.items():
            for obj in objs:
                if getattr(obj, k) == v:
                    return obj

    @classmethod
    def filter_by(cls, **kwargs):
        objs = cls.all()
        target_objs = []
        for k, v in kwargs.items():
            for obj in objs:
                if getattr(obj, k) == v:
                    target_objs.append(obj)
        return target_objs
