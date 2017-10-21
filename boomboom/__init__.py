class AbstractModel(object):
    def step(self, crank_degree, time_step):
        raise NotImplementedError()