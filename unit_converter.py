# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-21 13:40:21
# @Last Modified by:   lorenzo
# @Last Modified time: 2017-08-23 17:35:22

_conv_factors = { 
    # 80 meteres -> 800 pix
    'meters_pix' : 800/80
}

for desc, factor in _conv_factors.items():
    units = desc.split('_')
    globals()['_to_'.join(units)] = lambda unit_1: unit_1 * factor
    globals()['_to_'.join(reversed(units))] = lambda unit_2: unit_2 / factor
