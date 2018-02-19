import json

next_id = 1


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
        新建数据或修改数据
        """
        if self.id == -1:
            # 数据是新数据
            global next_id
            self.id = next_id
            next_id += 1
            with open(self.get_db_path(), 'a') as f:
                data_str = json.dumps(self.__dict__)
                f.write(data_str + '\n')
        else:
            obj_list = self.all()
            with open(self.get_db_path(), 'w') as f:
                for obj in obj_list:
                    if obj.id == self.id:
                        data_str = json.dumps(self.__dict__)
                    else:
                        data_str = json.dumps(obj.__dict__)
                    f.write(data_str + '\n')

    @classmethod
    def delete(cls, id):
        obj_list = cls.all()
        with open(cls.get_db_path(), 'w') as f:
            for obj in obj_list:
                if obj.id == id:
                    continue
                else:
                    data_str = json.dumps(obj.__dict__)
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
