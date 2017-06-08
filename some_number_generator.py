def gen_dn(digits:int, no_zero_flag=False: bool):
    if digits == 1:
        return list(range(1,10))
    concat = lambda x,y: x*10+y
    return list(filter(lambda x:x%digits == 0,
                       [x*10+y
                        for x in gen_dn(digits-1, no_zero_flag)
                        for y in range(no_zero_flag, 10)]))


print(sum(gen_dn(8, True)))

import timeit

tList = [timeit.timeit('gen_dn({})'.format(i), 'from __main__ import gen_dn', number=1000)
         for i in range(1,10)]
print(tList)
L1 = [
    0.0008114368097267288,
    0.0321953158809265,
    0.1600611122353257,
    0.5452999403346439,
    1.2822106803650968,
    2.040643221317623,
    3.152493783785758,
    4.586025745753432,
    6.014233273838727,
    7.512849830094638,
    7.52538116723963,
    7.523769496890054,
    7.5000717009252185,
]

L2 = [
    0.0007807078416135482,
    0.035914161188884464,
    0.2121633577544344,
    0.797374785857528,
    2.2296116498637275,
    5.105684602994643,
    9.669456174089873,
    16.14487844132418,
    25.135323012668096,
    34.47158370698912,
    44.67498482757219,
    53.91441790372096,
    62.245920089318815,
]
