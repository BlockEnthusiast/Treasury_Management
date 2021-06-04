
from models import AMM, AMM_Record


balancer = AMM()
balancer.seed(784,2434855)
balancer.set_weight_x(.20)



def setup(_x, _y, _name, _name_x, _name_y, _weight = None):
    lp = AMM(name = _name,
            name_x = _name_x,
            name_y = _name_y)
    lp.seed(x, y)
    if _weight:
        lp.set_weight_x(_weight)


def add_liquidity(_x):
